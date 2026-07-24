#!/usr/bin/env python3
"""neon_https.py - 5432가 막힌 네트워크용 대체 접속 경로 (443/HTTPS).

psycopg2.connect() 대신 이 함수를 쓰면, TCP 5432 대신 Neon의 공식
서버리스 드라이버(Node.js, HTTPS 통신)를 subprocess로 불러 같은 결과를 얻는다.
전제: Node.js 설치 + `npm install @neondatabase/serverless` (bridge 폴더에서 1회).

사용법 (기존 psycopg2 코드와 최대한 비슷하게):
    from neon_https import query
    rows = query("SELECT card_id, title FROM cards LIMIT 5;")

주의: 이 경로는 '진단/우회용'이다. 정상적으로 5432가 열리면 psycopg2 직접
연결이 더 빠르고 기능도 완전하다(트랜잭션, COPY 등). 443 경로는 단순 조회에 적합.
"""
import json
import os
import pathlib
import subprocess
import sys

BRIDGE = pathlib.Path(__file__).resolve().parent / "neon_bridge.mjs"

def query(sql: str) -> list[dict]:
    """SQL을 443/HTTPS로 실행해 결과 행(dict 리스트)을 반환. 실패 시 RuntimeError."""
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError(".env 또는 환경변수에 DATABASE_URL이 없음")
    result = subprocess.run(
        ["node", str(BRIDGE), sql],
        capture_output=True, text=True, env={**os.environ, "DATABASE_URL": dsn},
        timeout=30,
    )
    try:
        payload = json.loads(result.stdout.strip() or "{}")
    except json.JSONDecodeError:
        raise RuntimeError(f"브리지 출력 파싱 실패: {result.stdout!r} / stderr: {result.stderr!r}")
    if "error" in payload:
        raise RuntimeError(f"Neon HTTPS 질의 실패: {payload['error']}")
    return payload.get("rows", [])


if __name__ == "__main__":
    # 단독 실행 시 간단 점검: python neon_https.py "SELECT 1;"
    q = sys.argv[1] if len(sys.argv) > 1 else "SELECT 1;"
    try:
        print(query(q))
    except RuntimeError as e:
        print(f"[실패] {e}")
