## 읽기 지도 (무엇을 할 때 무엇만 읽는가)
| 상황 | 읽을 파일 (이것만) |
|---|---|
| 조사 주제 발굴 | prompts/0_scout.md |
| 카드 조사 | prompts/1_researcher.md |
| 카드 집필 | prompts/2_writer.md + templates/해당종류 1개 |
| 카드 검수 | prompts/3_validator.md |
| 다이제스트 반영 | prompts/4_updater.md |
| Unity 구현 지시 | prompts/5_developer.md |
| 기획/스펙 작성 | prompts/6_planner.md |
| QA 판정 | prompts/7_qa.md |
| 기존 카드 확인 | research/_index.md 먼저 → 필요한 카드 최대 2장 |
| 카드 형식 오류 | templates/해당종류 1개 (전체 templates 열람 금지)
| 여러 카드의 특정 절만 필요 (궁합, 빈칸 등) | tools/read_section.py <카드들> "<절 제목>" — 전체 열람 금지 |
| 절 제목은 표준 사전의 문자열 그대로 | 변형 제목 발견 시 lint로 잡아 수정 (임의 추측 금지) |

## 읽기 규율 (토큰 예산)
1. 위 지도에 없는 파일은 열지 않는다. 단계당 프롬프트 1개만 읽는다.
2. 카드 확인은 반드시 _index.md부터. 본문 열람은 작업당 최대 2장.
3. research/ 하위 폴더를 통째로 여는 것 금지 (ls는 허용, cat 전체 금지).
