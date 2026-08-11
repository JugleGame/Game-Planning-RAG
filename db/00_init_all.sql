-- ============================================================
-- 00_init_all.sql : 전체 DB 초기화 (한 번에, 올바른 순서로)
-- 실행: psql -d research -f db/00_init_all.sql
-- 원칙: md 파일이 원본, 이 DB는 거울. 손으로 INSERT 금지.
--
-- 주의: 이 파일은 '빈 DB를 새로 짓는' 스크립트다. 이미 데이터가 있는 DB에
--       스키마 v2를 적용하려면 db/01_migrate_v2.sql을 쓸 것 (DROP 없음).
-- ============================================================

-- [0] 확장 ------------------------------------------------------
-- pg_trgm은 선택이 아니다. tools/search_cards.py의 하이브리드 검색이
-- similarity() 함수를 쓰므로, 이게 없으면 검색기가 통째로 깨진다.
-- (v1 스키마에는 이 줄이 빠져 있어 재구축 시 검색이 죽는 상태였다.)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- [1] 거울 본체 -------------------------------------------------
DROP TABLE IF EXISTS card_sections, card_refs, digests, cards CASCADE;

CREATE TABLE cards (
  card_id    TEXT PRIMARY KEY CHECK (card_id ~ '^(ELEM|GAME|GENRE|ARCH)-[0-9]{3}$'),
  kind       TEXT GENERATED ALWAYS AS (split_part(card_id, '-', 1)) STORED,
  type       TEXT NOT NULL,
  title      TEXT NOT NULL,
  summary    TEXT NOT NULL,
  tags       TEXT[] NOT NULL DEFAULT '{}',
  elements   TEXT[] NOT NULL DEFAULT '{}',
  genres     TEXT[] NOT NULL DEFAULT '{}',
  updated    DATE NOT NULL,
  confidence TEXT NOT NULL CHECK (confidence IN ('high','medium','medium-low','low')),
  body       TEXT NOT NULL,
  file_path  TEXT NOT NULL,
  CONSTRAINT type_vocab CHECK (
    (split_part(card_id,'-',1)='ELEM'  AND type IN ('mechanic','narrative-device','tone','tech')) OR
    (split_part(card_id,'-',1)='GAME'  AND type IN ('success','failure','mixed')) OR
    (split_part(card_id,'-',1)='GENRE' AND type = 'genre') OR
    (split_part(card_id,'-',1)='ARCH'  AND type IN ('pattern','structure','convention')))
);

-- 절 단위 청크. 검색의 실제 작업 단위다.
--
-- 왜 카드가 아니라 절인가:
--   1) 정밀도 - "실패 사례"를 물었는데 카드 전체의 평균 벡터와 비교하면, 성공 서사가
--      대부분인 카드에서 실패 문단의 신호가 묻힌다.
--   2) 토큰 - 소비 측이 카드 전문(평균 2,075자)이 아니라 필요한 절(평균 340자)만
--      주입하면 된다. 실측 기준 회수당 약 85% 절감.
--   3) 경계가 공짜다 - 절 제목은 lint_card.py가 표준 사전으로 강제하므로
--      임의 길이 슬라이딩 윈도우가 아니라 의미 단위로 정확히 쪼개진다.
--
-- section_key는 언어 중립 식별자(card_schema.SECTIONS). 절 제목을 영어로 바꿔도
-- 이 키와 그 위에 걸린 모든 질의는 그대로 산다.
CREATE TABLE card_sections (
  card_id       TEXT NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
  ord           INT  NOT NULL,                 -- 카드 안에서의 등장 순서
  section_key   TEXT NOT NULL,
  section_title TEXT NOT NULL,                 -- 사람이 읽는 원문 제목 (표시용)
  body          TEXT NOT NULL,
  PRIMARY KEY (card_id, ord)
);
CREATE INDEX idx_sections_key ON card_sections(section_key);

CREATE TABLE card_refs (
  from_id TEXT NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
  to_id   TEXT NOT NULL,
  PRIMARY KEY (from_id, to_id)
);
-- 그래프 확장(어떤 카드가 나를 참조하는가)은 to_id로 역방향 조회한다.
CREATE INDEX idx_card_refs_to ON card_refs(to_id);

CREATE TABLE digests (
  digest_date DATE PRIMARY KEY,
  period      TEXT NOT NULL,
  sources     TEXT[] NOT NULL,
  status      TEXT NOT NULL,
  body        TEXT NOT NULL
);
CREATE VIEW unresolved_refs AS
  SELECT r.to_id AS missing_card, array_agg(r.from_id) AS referenced_by
  FROM card_refs r LEFT JOIN cards c ON c.card_id = r.to_id
  WHERE c.card_id IS NULL GROUP BY r.to_id;

-- 트라이그램(표층/고유명사) 검색에는 인덱스를 두지 않는다 - 의도적이다.
--
-- search_cards.py의 트라이그램 팔은 cards와 card_sections를 가로지르는 표현식에
-- similarity()를 걸어 전 행의 점수를 매긴다. 이런 질의는 단일 테이블 GIN 인덱스로
-- 가속되지 않는다 (GIN trgm이 돕는 건 `%` / LIKE 필터이지 전 행 랭킹이 아니다).
-- 게다가 array_to_string은 STABLE이라 표현식 인덱스에 들어가지도 못한다.
--
-- 병목이 되면: card_sections에 search_blob TEXT 컬럼을 sync_db.py가 채우고,
-- 거기 GIN을 건 뒤 `search_blob % query`로 후보를 먼저 거를 것.

-- [2] 신선도 + 토큰 최적화 계층 ---------------------------------
CREATE TABLE IF NOT EXISTS build_meta (id INT PRIMARY KEY DEFAULT 1, last_built_at TIMESTAMPTZ);
CREATE TABLE IF NOT EXISTS search_cache (
  query_norm  TEXT PRIMARY KEY,
  fetched_at  TIMESTAMPTZ NOT NULL,
  evidence    JSONB NOT NULL,
  ttl_days    INT NOT NULL DEFAULT 30
);
CREATE TABLE IF NOT EXISTS facts (
  fact_id     BIGSERIAL PRIMARY KEY,
  subject     TEXT NOT NULL,
  topic       TEXT NOT NULL,
  claim       TEXT NOT NULL,
  source_url  TEXT,
  as_of       DATE,
  UNIQUE (subject, topic, claim)
);
CREATE INDEX IF NOT EXISTS idx_facts_subject ON facts(subject);

-- [3] 벡터(선택): pgvector 설치돼 있을 때만 조용히 켠다 ----------
--
-- 차원 1024 = BAAI/bge-m3 (tools/embed_cards.py 기본 모델).
-- 이전 v1은 768 = jhgan/ko-sroberta-multitask 였는데, 그 모델은 입력 창이
-- 128토큰이라 카드 168장 전부가 잘려 나갔다(임베딩 텍스트 중앙값 811토큰,
-- 실제 반영 15.8%). 모델을 바꾸면 차원도 함께 바뀐다.
DO $$ BEGIN
  CREATE EXTENSION IF NOT EXISTS vector;

  ALTER TABLE cards ADD COLUMN IF NOT EXISTS embedding vector(1024);
  ALTER TABLE cards ADD COLUMN IF NOT EXISTS body_hash TEXT;
  ALTER TABLE card_sections ADD COLUMN IF NOT EXISTS embedding vector(1024);
  ALTER TABLE card_sections ADD COLUMN IF NOT EXISTS body_hash TEXT;

  -- HNSW: 카드 1,000장이면 절 청크는 약 4,800행(현재 168장=811절 기준).
  -- 순차 스캔이 질의마다 수십 MB를 훑게 되는 지점이라 인덱스가 필요하다.
  -- 168장 규모에서는 인덱스가 없어도 빠르지만, 있어도 손해가 아니다.
  CREATE INDEX IF NOT EXISTS idx_sections_hnsw
    ON card_sections USING hnsw (embedding vector_cosine_ops);
  CREATE INDEX IF NOT EXISTS idx_cards_hnsw
    ON cards USING hnsw (embedding vector_cosine_ops);
EXCEPTION WHEN OTHERS THEN
  RAISE NOTICE 'pgvector 미설치 또는 인덱스 생성 실패 - 벡터 기능 없이 진행 (%)', SQLERRM;
END $$;

-- [4] 전략 AI 읽기 전용 역할 ------------------------------------
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='strategy_ai') THEN
    CREATE ROLE strategy_ai LOGIN PASSWORD '반드시_교체할_것';
  END IF;
END $$;
DO $$ BEGIN
  EXECUTE format('GRANT CONNECT ON DATABASE %I TO strategy_ai', current_database());
END $$;
GRANT USAGE ON SCHEMA public TO strategy_ai;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO strategy_ai;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO strategy_ai;
