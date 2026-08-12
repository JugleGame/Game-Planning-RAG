#!/usr/bin/env python3
"""Embed RAG cards and sections into the mirror database.

Rows whose content fingerprint has not changed are skipped. The selected model
is part of that fingerprint, so a model switch forces a complete, consistent
re-embedding rather than mixing vector spaces. Embeddings run locally through
sentence-transformers and require no API key.

``card_sections.embedding`` (card title + section title + section body) drives
retrieval. ``cards.embedding`` (title + summary + tags) supports card-level
similarity checks. The prior 128-token ko-sroberta default truncated all card
inputs; bge-m3 supports the current section chunks without that loss.

Examples:
  python tools/embed_cards.py [--dsn postgresql://...] [--model BAAI/bge-m3]
  python tools/embed_cards.py --scope sections

When --dsn is omitted, DATABASE_URL or the local .env value is used.
"""
import argparse
import hashlib
import pathlib
import re
import sys

import psycopg2
import psycopg2.extras
from sentence_transformers import SentenceTransformer

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(BASE))
from _db import resolve_dsn, vec_literal
from card_schema import SOURCE_TAG_RE

# 임베딩 텍스트에서 걷어낼 것들.
#
# [출처: ...] 는 전체 문자의 11.1%(실측 38,854자)를 차지하는데, 검색 신호로는
# 거의 쓸모가 없다. 매체명이 의미 유사도를 흐리고 입력 창만 잡아먹는다.
# 원본 md는 건드리지 않는다 - 출처 규율은 카드의 핵심 자산이다. 여기서 빼는 건
# '좌표를 계산할 때만'이다. [해석] 표시는 남긴다(주장의 성격이 신호가 된다).
SOURCE_TAG = SOURCE_TAG_RE
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)

CARD_SELECT = "SELECT card_id, title, summary, array_to_string(tags,' ') AS tags, body_hash FROM cards"
SECTION_SELECT = ("SELECT s.card_id, s.ord, c.title, s.section_title, s.body, s.body_hash "
                  "FROM card_sections s JOIN cards c ON c.card_id = s.card_id")

CARD_UPDATE_HTTPS = "UPDATE cards SET embedding=$1::vector, body_hash=$2 WHERE card_id=$3"
SECTION_UPDATE_HTTPS = ("UPDATE card_sections SET embedding=$1::vector, body_hash=$2 "
                        "WHERE card_id=$3 AND ord=$4")


def clean(text: str) -> str:
    """좌표 계산용 텍스트 정리. 원본 md에는 영향 없음."""
    text = HTML_COMMENT.sub(" ", text)
    text = SOURCE_TAG.sub(" ", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def fingerprint(model_name: str, text: str) -> str:
    # 모델명을 지문에 섞음: 모델 바꾸면 모든 행이 '변경'으로 잡혀 재계산됨.
    #
    # 장치(cpu/cuda)와 정밀도(fp16/fp32)는 일부러 넣지 않는다. fp16 반올림 차이는
    # 1e-3 수준이라 코사인 순위를 바꾸지 않는데, 지문에 넣으면 노트북에서 돌렸다
    # 데스크톱에서 돌릴 때마다 전량 재계산이 걸린다 - 이득 없는 비용이다.
    return hashlib.sha256((model_name + "\n" + text).encode("utf-8")).hexdigest()


def _https():
    sys.path.insert(0, str(BASE / "db"))
    import neon_https
    return neon_https


def fetch_pg(dsn, sql):
    conn = psycopg2.connect(dsn)
    try:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
    finally:
        conn.close()


def write_pg(dsn, sql, rows):
    """execute_values로 한 번에 밀어 넣는다.

    예전에는 행마다 UPDATE를 따로 보냈다. 카드 1,000장이면 절이 약 4,800개이므로
    왕복도 4,800번이 된다 - 원격 Neon에서는 이것만으로 수 분이 걸린다.
    """
    if not rows:
        return
    conn = psycopg2.connect(dsn)
    try:
        cur = conn.cursor()
        psycopg2.extras.execute_values(cur, sql, rows, page_size=200)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


CARD_WRITE_PG = """
UPDATE cards SET embedding = v.emb::vector, body_hash = v.h
FROM (VALUES %s) AS v(emb, h, card_id)
WHERE cards.card_id = v.card_id
"""
SECTION_WRITE_PG = """
UPDATE card_sections SET embedding = v.emb::vector, body_hash = v.h
FROM (VALUES %s) AS v(emb, h, card_id, ord)
WHERE card_sections.card_id = v.card_id AND card_sections.ord = v.ord::int
"""


def load_model(name, device, fp16, max_seq, batch_size):
    """모델을 올리고 (모델, 실제 배치 크기)를 돌려준다.

    ## VRAM 주의

    bge-m3는 568M 파라미터다. fp32면 가중치만 약 2.3GB로, 4GB급 노트북 GPU
    (RTX 3050 Laptop 등)에서는 활성값까지 얹으면 OOM이 난다. GPU를 쓸 때는
    fp16을 기본으로 켠다 - 임베딩 품질에 실질적 차이가 없고 메모리는 절반이다.

    max_seq도 낮춘다. 모델 기본값은 8192지만 실제 절 청크는 최대 759토큰
    (중앙값 163, p90 327)이라 1024면 하나도 안 잘린다. 8192짜리 버퍼를 잡을
    이유가 없다.
    """
    import torch
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda" and not torch.cuda.is_available():
        raise SystemExit(
            "CUDA is unavailable. torch may be a CPU-only build. Check:\n"
            "  python -c \"import torch; print(torch.__version__, torch.version.cuda)\"\n"
            "Install a CUDA build: pip install --upgrade torch "
            "--index-url https://download.pytorch.org/whl/cu130")

    use_fp16 = fp16 if fp16 is not None else (device == "cuda")
    model = SentenceTransformer(name, device=device)
    # .half()로 낮춘다 - SentenceTransformer 생성자에 dtype을 넘기는 인자 이름이
    # transformers 버전마다 달라(torch_dtype -> dtype) 깨지기 쉽다.
    if use_fp16:
        model = model.half()
    model.max_seq_length = min(max_seq, model.max_seq_length)

    if device == "cuda":
        gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"Device: cuda ({torch.cuda.get_device_name(0)}, {gb:.1f}GB) "
              f"| dtype {'fp16' if use_fp16 else 'fp32'} | max_seq {model.max_seq_length} "
              f"| batch {batch_size}")
        if gb < 6 and batch_size > 8:
            batch_size = 8
            print(f"  VRAM {gb:.1f}GB — reduced batch size to {batch_size} to avoid OOM")
    else:
        print(f"Device: cpu | max_seq {model.max_seq_length} | batch {batch_size}")
    return model, batch_size


def run(scope, rows, model, model_name, dsn, used, batch_size=16):
    """(대상 목록) -> 변경분만 인코딩해 저장. 처리 건수를 돌려준다."""
    todo = []
    for r in rows:
        if scope == "cards":
            card_id, title, summary, tags, old_hash = r
            text = clean(f"{title}\n{summary}\n{tags}")
            ident = (card_id,)
        else:
            card_id, ordn, card_title, sec_title, body, old_hash = r
            # 카드 제목을 절 앞에 붙인다: 절만 떼면 "이게 어느 게임 얘기인지"가 사라져
            # 고유명사 질의에 안 걸린다.
            text = clean(f"{card_title}\n{sec_title}\n{body}")
            ident = (card_id, ordn)
        h = fingerprint(model_name, text)
        if h != old_hash:
            todo.append((ident, text, h))

    label = "cards" if scope == "cards" else "sections"
    if not todo:
        print(f"[{used}] {label}: no changes; embedding update skipped")
        return 0
    print(f"[{used}] {label} to embed: {len(todo)}")

    vecs = model.encode([t for _, t, _ in todo], show_progress_bar=len(todo) > 50,
                        normalize_embeddings=True, batch_size=batch_size)
    # fp16으로 뽑으면 half 배열이 온다. pgvector로 보내는 건 어차피 텍스트라
    # 여기서 float로 올려 자릿수 표기를 안정시킨다.
    vecs = vecs.astype("float32")

    # fp16은 드물게 오버플로로 NaN/Inf를 낸다. 그대로 쓰면 코사인 비교가
    # 조용히 무의미해지므로(정렬에서 그 행만 사라지거나 아무 데나 붙는다)
    # 여기서 크게 실패시킨다 - 잘못된 좌표를 저장하느니 저장하지 않는 편이 낫다.
    import numpy as np
    bad = ~np.isfinite(vecs).all(axis=1)
    if bad.any():
        ids = [todo[i][0] for i in np.nonzero(bad)[0][:5]]
        raise SystemExit(
            f"Embedding contains {int(bad.sum())} NaN/Inf values (for example: {ids}). "
            "Nothing was written. Retry with --fp32 "
            "(or --device cpu --fp32 if VRAM is insufficient).")

    if used == "5432":
        sql = CARD_WRITE_PG if scope == "cards" else SECTION_WRITE_PG
        write_pg(dsn, sql, [(vec_literal(v.tolist()), h, *ident)
                            for (ident, _, h), v in zip(todo, vecs)])
    else:
        stmt = CARD_UPDATE_HTTPS if scope == "cards" else SECTION_UPDATE_HTTPS
        _https().transaction([(stmt, [vec_literal(v.tolist()), h, *ident])
                              for (ident, _, h), v in zip(todo, vecs)])
    print(f"Complete - stored embeddings for {len(todo)} {label}")
    return len(todo)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None, help="defaults to DATABASE_URL from the environment or .env")
    ap.add_argument("--model", default="BAAI/bge-m3",
                    help="8192-token window, 1024 dimensions, Korean/English cross-lingual; changing it re-embeds all rows")
    ap.add_argument("--scope", choices=["all", "cards", "sections"], default="all")
    ap.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto",
                    help="auto uses GPU when available (default)")
    ap.add_argument("--fp16", dest="fp16", action="store_true", default=None,
                    help="force fp16 (enabled by default on GPU)")
    ap.add_argument("--fp32", dest="fp16", action="store_false",
                    help="force fp32; use only when VRAM is sufficient")
    ap.add_argument("--max-seq", type=int, default=1024,
                    help="input-token cap; 1024 covers the current largest section chunk")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto tries 5432 first, then falls back to 443/HTTPS (default)")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    scopes = ["cards", "sections"] if a.scope == "all" else [a.scope]
    sql_for = {"cards": CARD_SELECT, "sections": SECTION_SELECT}
    cols_for = {
        "cards": ["card_id", "title", "summary", "tags", "body_hash"],
        "sections": ["card_id", "ord", "title", "section_title", "body", "body_hash"],
    }

    # 1) 현재 상태 읽기 (5432 -> 실패 시 HTTPS)
    used, fetched = None, {}
    if a.transport in ("auto", "pg"):
        try:
            fetched = {s: fetch_pg(dsn, sql_for[s]) for s in scopes}
            used = "5432"
        except psycopg2.OperationalError as e:
            if a.transport == "pg":
                raise
            print(f"5432 connection failed; falling back to the 443/HTTPS bridge "
                  f"({str(e).strip().splitlines()[0][:100]})", file=sys.stderr)
            used = "443/HTTPS"
    else:
        used = "443/HTTPS"
    if used == "443/HTTPS":
        h = _https()
        fetched = {s: [tuple(r[c] for c in cols_for[s]) for r in h.query(sql_for[s])]
                   for s in scopes}

    if not any(fetched.values()):
        print("No target rows; run tools/sync_db.py first", file=sys.stderr)
        sys.exit(1)

    model, batch = load_model(a.model, a.device, a.fp16, a.max_seq, a.batch_size)
    total = sum(run(s, fetched[s], model, a.model, dsn, used, batch) for s in scopes)
    if total == 0:
        print("No embeddings to update (all current)")


if __name__ == "__main__":
    main()
