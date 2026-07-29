-- ============================================================
-- 00_init_all.sql : 전체 DB 초기화 (한 번에, 올바른 순서로)
-- 실행: psql -d research -f db/00_init_all.sql
-- 원칙: md 파일이 원본, 이 DB는 거울. 손으로 INSERT 금지.
-- ============================================================

-- [1] 거울 본체 -------------------------------------------------
DROP TABLE IF EXISTS card_refs, digests, cards CASCADE;

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
CREATE TABLE card_refs (
  from_id TEXT NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
  to_id   TEXT NOT NULL,
  PRIMARY KEY (from_id, to_id)
);
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
DO $$ BEGIN
  CREATE EXTENSION IF NOT EXISTS vector;
  ALTER TABLE cards ADD COLUMN IF NOT EXISTS embedding vector(768);
  ALTER TABLE cards ADD COLUMN IF NOT EXISTS body_hash TEXT;
EXCEPTION WHEN OTHERS THEN
  RAISE NOTICE 'pgvector 미설치 - 벡터 기능 없이 진행 (나중에 켤 수 있음)';
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
