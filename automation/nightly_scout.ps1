# 매일 밤 23:05 실행 - 스카우트 후보 발굴 전용 (카드 생성 없음, 큐에 추가만 함)
# 사용 전 확인: $RepoPath 를 본인 노트북의 실제 저장소 경로로 바꿀 것

$RepoPath = "C:\path\to\Game-Design-and-Planning_resarch"
Set-Location $RepoPath

$categories = @("ELEM", "GAME", "GENRE")
$category = Get-Random -InputObject $categories
$today = Get-Date -Format "yyyy-MM-dd"

$prompt = @"
너는 prompts/0_scout.md 에 정의된 역할만 수행한다. 다른 프롬프트는 절대 실행하지 마라.

입력:
- 배정된 카테고리: $category
- research/_index.md 전체 내용을 읽어 기존 카드와 중복되지 않게 할 것
- research/signals/ 폴더에서 가장 최근 다이제스트 2개를 읽어 참고할 것

작업:
1. prompts/0_scout.md 의 Rules를 그대로 따라 후보 5개를 뽑아라.
2. 카드를 직접 만들지 마라. 조사도 하지 마라. 오직 후보 제안만 한다.
3. research/_scout_queue.md 파일을 열어, 파일 맨 위(첫 번째 "---" 구분선 아래)에
   다음 형식으로 새 블록을 추가하라. 기존 내용은 절대 지우거나 수정하지 마라.

## $today 23:05 생성 (카테고리: $category)
- [ ] <후보명> — connects_to: <카드ID> — why_now: <이유> — obscurity: <낮음/중간/높음>
(총 5개)

4. research/_scout_queue.md 이외의 어떤 파일도 수정하지 마라. git commit/push 도 하지 마라.
"@

claude -p $prompt
