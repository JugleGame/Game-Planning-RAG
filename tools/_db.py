"""_db.py - DSN 해석 공통 헬퍼 (모든 db 스크립트가 공유).

우선순위: --dsn CLI 인자 > DATABASE_URL 환경변수 > .env 파일의 DATABASE_URL > 로컬 기본값.
python-dotenv 등 추가 의존성 없이 .env를 직접 파싱한다 (KEY=VALUE, # 주석, 따옴표 지원).
"""
import os
import pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent


def load_dotenv(path: pathlib.Path = BASE / ".env") -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def resolve_dsn(cli_dsn: str | None) -> str:
    if cli_dsn:
        return cli_dsn
    load_dotenv()
    dsn = os.environ.get("DATABASE_URL")
    if dsn:
        return dsn
    return "dbname=research"
