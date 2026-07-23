#!/usr/bin/env python3
"""init_db.py - db/00_init_all.sql을 대상 Postgres(Neon 포함)에 실행한다.

사용법:
  python tools/init_db.py [--dsn postgresql://...]
DSN 생략 시 .env의 DATABASE_URL을 사용한다 (_db.resolve_dsn 참조).
"""
import argparse
import pathlib
import sys

import psycopg2

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _db import resolve_dsn

BASE = pathlib.Path(__file__).resolve().parent.parent
INIT_SQL = BASE / "db" / "00_init_all.sql"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None)
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    sql = INIT_SQL.read_text(encoding="utf-8")
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        print(f"초기화 실패: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()
    print(f"{INIT_SQL.relative_to(BASE)} 실행 완료 -> {dsn.split('@')[-1] if '@' in dsn else dsn}")


if __name__ == "__main__":
    main()
