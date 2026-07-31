# 스카우트 추천 큐 (자동 생성)

사용 방법:
1. 매일 밤 23:05, `nightly_scout.ps1`이 이 파일 맨 위에 새 후보 5개를 `[ ]` 미체크 상태로 추가합니다.
2. 사람이 아침이나 저녁에 이 파일을 열어, 실제로 진행하고 싶은 항목만 `[ ]` → `[x]`로 바꿔 저장합니다.
3. 다음날 00:40, `nightly_executor.ps1`이 `[x]` 항목만 골라 카드로 만들고, 처리 완료되면 `[done]`으로 바꿉니다.
4. `[ ]`로 남아있는(선택 안 된) 항목은 건드리지 않고 그대로 큐에 남습니다.

---

## 2026-07-30 23:05 생성 (카테고리: ELEM)
- [ ] 재화 전환형 제작 마찰 완화 (Craft Material Conversion to Reduce Grind Friction) — connects_to: ELEM-019, GAME-023 — why_now: Diablo IV 3.1.1/3.1.1a 패치가 판데모니움 조각 요구량을 5→4로 낮추고 "신화 아이템 1회 제작" 제한을 철폐해, 루트 기반 마찰을 재화 전환으로 완화하는 신호 (07-27 다이제스트) — obscurity: 중간
- [done] 광기 파생 액티브 전투 메커닉 (Derangement-driven Active Combat Mechanic) — connects_to: ELEM-015, GAME-022 — why_now: 다키스트 던전 10주년 DLC 'The Fire's Edge'(2026-08-18)가 발작(derangement) 시스템을 신규 'Burn' 전투 메커닉으로 확장 투자 (07-27 다이제스트) — obscurity: 중간 — [removed 2026-07-31] ELEM-024는 ELEM-015와 근거(GAME-022 DLC 발표)가 동일해 중복 → ELEM-015 성공 사례·리스크로 통합 후 삭제
- [done] 온디바이스 SLM 실시간 음성 대화 NPC (On-device SLM Real-time Voice NPC, e.g. NVIDIA ACE) — connects_to: ELEM-005, ELEM-006, GAME-011 — why_now: NVIDIA ACE 스택(ASR+소형 언어모델+TTS+표정)이 데모를 넘어 inZOI·NARAKA: BLADEPOINT 등 실제 출시 빌드에 탑재되기 시작, 텍스트 기반 AI 통합과 구분되는 음성 전용 파이프라인 (07-27 다이제스트) — obscurity: 낮음 — ELEM-025
- [done] 추출형 런 구조 (Loot-and-Extract Run Structure) — connects_to: ELEM-004, ELEM-014, GENRE-009 — why_now: 다크 판타지 추출형 ARPG 'Mistfall Hunter' 오픈베타에 약 43만 명 참여 후 07-29 정식 출시 - 죽음=손실이 아니라 '탈출 성공 여부'로 보상이 갈리는 별도 순환 구조 (07-27 다이제스트) — obscurity: 높음 — ELEM-027
- [done] 테마 쏠림형 바이럴 소재 선택 (Thematic Convergence for Shareability, 고양이 테마 사례) — connects_to: ELEM-010, GENRE-007 — why_now: 2026년 7월 코지 신작 밀집 출시 중 고양이 테마가 SNS 공유·참여도에서 일관된 우위를 보인다는 보도 - 장르 관습이 아니라 '소재 선택'이 바이럴리티를 좌우하는 신호 (07-25 다이제스트) — obscurity: 중간 — [removed 2026-07-31] ELEM-026의 관측(고양이 테마 우위)이 ELEM-010·GENRE-007에 이미 동일 출처로 기록돼 중복 → ELEM-010 조합 궁합으로 통합 후 삭제
