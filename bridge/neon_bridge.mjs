#!/usr/bin/env node
/**
 * neon_bridge.mjs — 5432가 막힌 네트워크에서 443(HTTPS)으로 Neon에 SQL을 실행.
 * Neon 공식 서버리스 드라이버(@neondatabase/serverless)는 edge/서버리스 환경처럼
 * TCP(5432) 접속이 안 되는 곳을 위해 만들어졌고, 순수 HTTPS(443)로 통신한다.
 * 이 스크립트는 Python 파이프라인에서 subprocess로 호출하는 '다리' 역할만 한다.
 *
 * 사용법:
 *   DATABASE_URL="postgresql://user:pw@ep-xxx.neon.tech/db?sslmode=require" \
 *     node neon_bridge.mjs "SELECT count(*) FROM cards;"
 * 출력: JSON (성공 시 행 배열, 실패 시 {"error": "..."})
 */
import { neon } from '@neondatabase/serverless';

async function main() {
  const query = process.argv[2];
  const dsn = process.env.DATABASE_URL;
  if (!dsn) { console.log(JSON.stringify({ error: ".env의 DATABASE_URL이 없음" })); process.exit(1); }
  if (!query) { console.log(JSON.stringify({ error: "SQL 쿼리를 인자로 전달할 것" })); process.exit(1); }
  try {
    const sql = neon(dsn);
    // sql.query(): 일반 문자열 SQL + 파라미터 배열을 받는 호출 방식(태그드 템플릿 아님)
    const rows = await sql.query(query);   // 내부적으로 https://<host>/sql 로 POST (443 포트만 사용)
    console.log(JSON.stringify({ rows }));
  } catch (e) {
    console.log(JSON.stringify({ error: String(e.message || e) }));
    process.exit(1);
  }
}
main();
