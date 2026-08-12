"""_db.py - DSN 해석 + 접속 경로(5432 / 443 HTTPS) 공통 헬퍼.

우선순위: --dsn CLI 인자 > DATABASE_URL 환경변수 > .env 파일의 DATABASE_URL > 로컬 기본값.
python-dotenv 등 추가 의존성 없이 .env를 직접 파싱한다 (KEY=VALUE, # 주석, 따옴표 지원).

읽기 경로(search_cards.py, eval_retrieval.py)는 psycopg2 커서를 그대로 쓰도록 짜여
있었다. 5432가 막힌 망에서 이 둘만 통째로 죽던 것이 open_cursor()가 생긴 이유다 -
쓰기·점검 경로(sync_db/embed_cards/verify_db)에는 이미 폴백이 있었다.
"""
import os
import pathlib
import re
import sys

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


def vec_literal(v) -> str:
    """pgvector는 '[0.1,0.2,…]' 문자열을 vector로 캐스팅해 받는다.

    5432(psycopg2)든 443(HTTPS)이든 같은 표기를 쓴다. psycopg2는 리스트를
    ARRAY[…]로도 적어 주지만, 두 경로가 서로 다른 표기를 타면 언젠가 한쪽만
    조용히 달라진다 - 좌표 표기는 한 곳에서만 만든다.
    """
    return "[" + ",".join(f"{x:.8f}" for x in v) + "]"


_NAMED_PLACEHOLDER = re.compile(r"%\((\w+)\)s")


def to_positional(sql: str, params: dict):
    """psycopg2식 %(name)s 를 Postgres 네이티브 $1,$2… 로 바꾼다.

    HTTPS 브리지(@neondatabase/serverless)는 $N 자리표시자만 받는다.
    같은 이름이 여러 번 나오면(HYBRID_SQL의 %(window)s는 6번) 같은 번호를
    재사용하고 값은 한 번만 넘긴다. 사전에 없는 이름은 KeyError로 시끄럽게 죽는다 -
    검색 SQL에서 자리표시자가 어긋난 채 조용히 다른 결과를 내는 것보다 낫다.
    """
    order: list[str] = []

    def sub(m):
        name = m.group(1)
        if name not in order:
            order.append(name)
        return f"${order.index(name) + 1}"

    return _NAMED_PLACEHOLDER.sub(sub, sql), [params[n] for n in order]


class HttpsCursor:
    """neon_https.query 를 DB-API 커서처럼 보이게 하는 최소 어댑터.

    query_sections()가 cur.execute / cur.description / cur.fetchall 만 쓰기 때문에
    이 셋이면 충분하다. 브리지는 dict를 주므로 psycopg2와 같은 '컬럼 순서 튜플'로
    맞춰 돌려준다.
    """

    def __init__(self, https):
        self._https = https
        self.description = None
        self._rows = []

    def execute(self, sql, params=None):
        if isinstance(params, dict):
            sql, params = to_positional(sql, params)
        rows = self._https.query(sql, list(params or []))
        # 컬럼 순서는 브리지가 돌려준 첫 행의 키 순서 = SELECT 절 순서.
        self.description = [(c,) for c in (rows[0].keys() if rows else [])]
        self._rows = [tuple(r.values()) for r in rows]

    def fetchall(self):
        return self._rows

    def close(self):
        pass


def open_cursor(dsn: str, transport: str = "auto"):
    """(cursor, close, 경로이름). 5432가 되면 psycopg2, 안 되면 443/HTTPS 브리지.

    auto 에서만 connect_timeout 을 짧게 준다. 막힌 망에서 기본값으로 두면 DNS가
    돌려주는 주소마다 수십 초씩 기다린 뒤에야 폴백한다(실측 24초 이상) - 사람이
    기다리는 검색 경로에서는 그 자체가 고장이다.
    """
    if transport in ("auto", "pg"):
        import psycopg2
        try:
            kw = {"connect_timeout": 5} if transport == "auto" else {}
            conn = psycopg2.connect(dsn, **kw)
            return conn.cursor(), conn.close, "5432"
        except psycopg2.OperationalError as e:
            if transport == "pg":
                raise
            print(f"5432 접속 실패 -> 443/HTTPS 브리지로 폴백합니다 "
                  f"({str(e).strip().splitlines()[0][:100]})", file=sys.stderr)
    sys.path.insert(0, str(BASE / "db"))
    import neon_https
    return HttpsCursor(neon_https), (lambda: None), "443/HTTPS"


if __name__ == "__main__":
    # 자리표시자 재작성 자체 점검 (DB 없이 실행 가능): python tools/_db.py
    sql, params = to_positional(
        "SELECT $$x$$, %(vec)s::vector, %(k)s FROM t "
        "WHERE a <= %(window)s OR b <= %(window)s LIMIT %(k)s",
        {"vec": "[1,2]", "k": 5, "window": 60, "unused": "안 쓰이면 안 넘어간다"},
    )
    assert sql.endswith("WHERE a <= $3 OR b <= $3 LIMIT $2"), sql
    assert "$$x$$" in sql, sql          # 달러 인용 문자열은 건드리지 않는다
    assert params == ["[1,2]", 5, 60], params
    try:
        to_positional("SELECT %(nope)s", {})
        raise AssertionError("없는 파라미터는 KeyError로 죽어야 한다")
    except KeyError:
        pass
    assert vec_literal([1, 0.5]) == "[1.00000000,0.50000000]"
    print("ok")
