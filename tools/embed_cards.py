#!/usr/bin/env python3
"""embed_cards.py - 카드 본문에서 좌표(임베딩)를 뽑아 DB에 저장한다.

핵심 설계:
1) 본문의 지문(hash)이 안 바뀐 카드는 재계산을 건너뛴다 - 매번 전량 임베딩은 낭비.
2) 임베딩 모델은 '설정 한 곳'에서만 지정. 모델을 바꾸면 지문 규칙도 따라 바뀌어
   자동으로 전량 재계산이 걸린다(모델 혼용으로 좌표 체계가 어긋나는 사고 방지).
3) API 키 불필요 - 로컬 sentence-transformers 사용. 한국어 모델 기본값.

사용법:
  python tools/embed_cards.py [--dsn postgresql://...] [--model jhgan/ko-sroberta-multitask]
  (--dsn 생략 시 DATABASE_URL 환경변수 또는 .env 파일 사용)
"""
import hashlib, argparse, pathlib, sys
import psycopg2
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _db import resolve_dsn

def body_hash(model_name: str, body: str) -> str:
    # 모델명을 지문에 섞음: 모델 바꾸면 모든 카드가 '변경'으로 잡혀 재계산됨
    return hashlib.sha256((model_name + "\n" + body).encode("utf-8")).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None, help="생략 시 DATABASE_URL 환경변수 또는 .env 사용")
    ap.add_argument("--model", default="jhgan/ko-sroberta-multitask")  # 한국어 특화, 768차원
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    model = SentenceTransformer(a.model)
    conn = psycopg2.connect(dsn); cur = conn.cursor()
    cur.execute("SELECT card_id, title, summary, body, body_hash FROM cards")
    rows = cur.fetchall()

    todo = []
    for card_id, title, summary, body, old_hash in rows:
        # 임베딩 대상은 본문만이 아니라 title+summary+body의 합 - 짧은 요약도 검색에 잡히게
        text = f"{title}\n{summary}\n{body}"
        h = body_hash(a.model, text)
        if h != old_hash:
            todo.append((card_id, text, h))

    if not todo:
        print("변경 없음 - 임베딩 갱신 생략"); return
    print(f"임베딩 갱신 대상: {len(todo)}장")
    vecs = model.encode([t for _, t, _ in todo], show_progress_bar=False, normalize_embeddings=True)
    for (card_id, _, h), v in zip(todo, vecs):
        cur.execute("UPDATE cards SET embedding=%s, body_hash=%s WHERE card_id=%s",
                    (v.tolist(), h, card_id))
    conn.commit()
    print(f"완료 - {len(todo)}장 좌표 저장")

if __name__ == "__main__":
    main()
