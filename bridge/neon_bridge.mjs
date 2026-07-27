#!/usr/bin/env node
/**
 * neon_bridge.mjs — 5432가 막힌 네트워크에서 443(HTTPS)으로 Neon에 SQL을 실행.
 * Neon 공식 서버리스 드라이버(@neondatabase/serverless)는 edge/서버리스 환경처럼
 * TCP(5432) 접속이 안 되는 곳을 위해 만들어졌고, 순수 HTTPS(443)로 통신한다.
 * 이 스크립트는 Python 파이프라인에서 subprocess로 호출하는 '다리' 역할만 한다.
 *
 * 두 가지 모드:
 *
 * 1) 단일 질의 — SQL을 인자로 전달 (파라미터는 $1,$2… 자리표시자 + JSON 배열)
 *      DATABASE_URL="postgres://…" node neon_bridge.mjs "SELECT * FROM cards WHERE card_id=$1;" '["GAME-001"]'
 *    출력: {"rows":[…]}
 *
 * 2) 배치 트랜잭션 — stdin으로 JSON을 받아 **하나의 트랜잭션**으로 실행
 *      echo '{"statements":[{"sql":"…","params":[…]}, …]}' | node neon_bridge.mjs --batch
 *    출력: {"results":[{"rowCount":n,"rows":[…]}, …]}
 *    한 건이라도 실패하면 전체가 롤백되고 {"error":"…"}를 돌려준다.
 *    (statements가 많아 명령줄 길이 제한에 걸리므로 stdin을 쓴다)
 *
 * 실패는 항상 stdout에 {"error":"…"} JSON으로 낸다 — 호출자가 조용한 실패로
 * 오인하지 않도록.
 */
import { neon } from '@neondatabase/serverless';

function fail(msg) {
  console.log(JSON.stringify({ error: String(msg) }));
  process.exit(1);
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let buf = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (c) => { buf += c; });
    process.stdin.on('end', () => resolve(buf));
    process.stdin.on('error', reject);
  });
}

async function main() {
  const dsn = process.env.DATABASE_URL;
  if (!dsn) fail('.env의 DATABASE_URL이 없음');

  const sql = neon(dsn, { fullResults: true });   // rowCount를 받기 위해 fullResults

  if (process.argv[2] === '--batch') {
    const raw = await readStdin();
    let payload;
    try {
      payload = JSON.parse(raw);
    } catch (e) {
      fail(`stdin JSON 파싱 실패: ${e.message}`);
    }
    const statements = payload.statements;
    if (!Array.isArray(statements)) fail('statements 배열이 없음');
    if (statements.length === 0) {
      console.log(JSON.stringify({ results: [] }));
      return;
    }
    try {
      // 배열로 넘기면 드라이버가 단일 비대화형 트랜잭션으로 묶어 보낸다.
      // 하나라도 실패하면 전체 롤백.
      const results = await sql.transaction(
        statements.map((s) => sql.query(s.sql, s.params ?? []))
      );
      console.log(JSON.stringify({
        results: results.map((r) => ({ rowCount: r.rowCount, rows: r.rows })),
      }));
    } catch (e) {
      fail(`트랜잭션 실패(전체 롤백됨): ${e.message || e}`);
    }
    return;
  }

  const query = process.argv[2];
  if (!query) fail('SQL 쿼리를 인자로 전달할 것');
  let params = [];
  if (process.argv[3]) {
    try {
      params = JSON.parse(process.argv[3]);
    } catch (e) {
      fail(`params JSON 파싱 실패: ${e.message}`);
    }
  }
  try {
    // sql.query(): $1,$2… 자리표시자 + 파라미터 배열 (태그드 템플릿 아님)
    const r = await sql.query(query, params);   // 내부적으로 https://<host>/sql 로 POST (443만 사용)
    console.log(JSON.stringify({ rows: r.rows, rowCount: r.rowCount }));
  } catch (e) {
    fail(e.message || e);
  }
}

main().catch((e) => fail(e.message || e));
