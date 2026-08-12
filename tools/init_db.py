#!/usr/bin/env python3
"""Run db/00_init_all.sql against the target Postgres database (including Neon).

Usage:
  python tools/init_db.py [--dsn postgresql://...]
Without a DSN, use DATABASE_URL from .env (see _db.resolve_dsn).
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
        print(f"Initialization failed: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        cur.close()
        conn.close()
    print(f"Executed {INIT_SQL.relative_to(BASE)} -> {dsn.split('@')[-1] if '@' in dsn else dsn}")


if __name__ == "__main__":
    main()
