-- ============================================================
-- 01_migrate_v2.sql : 살아 있는 DB를 스키마 v1 -> v2로 올린다 (DROP TABLE 없음)
--
-- 실행: psql "$DATABASE_URL" -f db/01_migrate_v2.sql
--       (Neon 콘솔 SQL 편집기에 붙여넣어도 된다)
--
-- 왜 00_init_all.sql을 다시 돌리면 안 되는가: 그 스크립트는 DROP TABLE로 시작한다.
-- 카드 본문은 md에서 복구되지만 굳이 지웠다 넣을 이유가 없다.
--
-- v1 -> v2 변경점
--   1. pg_trgm 확장을 명시적으로 설치 (v1 스키마에 빠져 있었다 - 검색기가
--      similarity()를 쓰는데 확장 생성 구문이 어디에도 없어서, 스키마 파일로
--      DB를 재구축하면 검색이 죽는 상태였다)
--   2. card_sections 절 청크 테이블 추가
--   3. 임베딩 차원 768 -> 1024 (ko-sroberta 128토큰 창 -> bge-m3 8192토큰 창)
--   4. HNSW / GIN 인덱스 추가
--
-- 실행 후 반드시: python tools/sync_db.py && python tools/embed_cards.py
--   (임베딩 컬럼을 새로 만들었으므로 전량 재계산된다)
-- ============================================================

BEGIN;

-- [1] 확장 ------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- [2] 절 청크 테이블 --------------------------------------------
CREATE TABLE IF NOT EXISTS card_sections (
  card_id       TEXT NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
  ord           INT  NOT NULL,
  section_key   TEXT NOT NULL,
  section_title TEXT NOT NULL,
  body          TEXT NOT NULL,
  PRIMARY KEY (card_id, ord)
);
CREATE INDEX IF NOT EXISTS idx_sections_key ON card_sections(section_key);
CREATE INDEX IF NOT EXISTS idx_card_refs_to ON card_refs(to_id);

-- [3] 트라이그램 인덱스는 두지 않는다 (의도적) -------------------
--
-- search_cards.py의 트라이그램 팔은 cards와 card_sections를 가로지르는 표현식
-- (c.title || c.summary || tags || s.body)에 similarity()를 걸어 **전 행의 점수를
-- 매긴다**. 이런 질의는 어느 단일 테이블 GIN 인덱스도 탈 수 없다 - GIN trgm이
-- 도와주는 건 `%` / LIKE 필터이지 전 행 랭킹이 아니다.
-- (덧붙여 array_to_string은 STABLE이라 표현식 인덱스에 아예 들어가지 못한다.)
--
-- 언젠가 트라이그램이 병목이 되면: card_sections에 search_blob TEXT 컬럼을
-- sync_db.py가 채우게 하고 거기에 GIN을 건 뒤, `search_blob % query`로 후보를
-- 먼저 걸러라. 지금(절 811개)은 순차 계산이 충분히 싸다.

COMMIT;

-- [4] 벡터 차원 교체 --------------------------------------------
--
-- 768차원 컬럼에 1024차원 값을 넣을 수 없고, ALTER TYPE은 기존 데이터가 있으면
-- 실패한다. 임베딩은 md에서 언제든 다시 뽑을 수 있는 파생 데이터이므로
-- 컬럼을 버리고 새로 만든다 (원본은 md, DB는 거울 - 거울은 다시 비추면 된다).
DO $$ BEGIN
  CREATE EXTENSION IF NOT EXISTS vector;

  ALTER TABLE cards DROP COLUMN IF EXISTS embedding;
  ALTER TABLE cards ADD  COLUMN embedding vector(1024);
  ALTER TABLE cards ADD  COLUMN IF NOT EXISTS body_hash TEXT;
  UPDATE cards SET body_hash = NULL;          -- 전량 재임베딩을 강제

  ALTER TABLE card_sections ADD COLUMN IF NOT EXISTS embedding vector(1024);
  ALTER TABLE card_sections ADD COLUMN IF NOT EXISTS body_hash TEXT;

  CREATE INDEX IF NOT EXISTS idx_sections_hnsw
    ON card_sections USING hnsw (embedding vector_cosine_ops);
  CREATE INDEX IF NOT EXISTS idx_cards_hnsw
    ON cards USING hnsw (embedding vector_cosine_ops);
EXCEPTION WHEN OTHERS THEN
  RAISE NOTICE 'pgvector 단계 실패 - 벡터 없이 진행 (%)', SQLERRM;
END $$;

-- [5] 새 테이블에도 읽기 전용 권한 -------------------------------
GRANT SELECT ON ALL TABLES IN SCHEMA public TO strategy_ai;
