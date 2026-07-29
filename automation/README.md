# 야간 카드 자동화 (집 노트북 전용)

이 폴더의 스크립트는 **이 컴퓨터가 아니라 사용자의 집 노트북**에서, Windows 작업 스케줄러(Task Scheduler)로
매일 밤 두 번 자동 실행하기 위한 것입니다. 클라우드가 아니라 노트북이 켜져 있어야 실행됩니다.

## 전체 흐름

```
23:05  nightly_scout.ps1     -> research/_scout_queue.md 에 후보 5개 추가 ([ ] 미체크)
       (사람) 큐 파일을 열어 진행하고 싶은 항목만 [x] 로 체크
00:40  nightly_executor.ps1  -> [x] 항목만 카드로 제작, 신호/기존카드 갱신, 색인/DB 동기화
06:00  이전에 종료 (세션이 버거우면 스스로 멈춤)
       (사람) 아침에 git diff 확인 후 직접 commit/push
```

- **사람이 할 일은 딱 하나**: 밤 23:05~00:40 사이에 `research/_scout_queue.md` 를 열어
  원하는 후보만 `[ ]` → `[x]` 로 체크하는 것. 나머지는 스크립트가 처리합니다.
- 두 스크립트 모두 **git commit/push를 하지 않습니다.** 매일 아침 변경 사항을 직접 확인하고
  커밋할지 결정하도록 일부러 그렇게 만들었습니다.

## 설치 순서 (집 노트북에서)

1. 이 저장소를 노트북에 clone/pull 받고, 노트북에도 Claude Code CLI가 설치·로그인되어 있는지 확인합니다.
2. `nightly_scout.ps1`, `nightly_executor.ps1` 두 파일 안의 `$RepoPath` 를
   노트북에서의 실제 저장소 경로로 바꿉니다.
3. **중요 - 권한 설정**: 밤에 사람 없이 돌기 때문에, `claude -p` 실행 중 파일 쓰기/Bash 실행
   권한을 매번 묻지 않도록 미리 설정해야 합니다. 이 저장소의 `.claude/settings.json` (또는
   `settings.local.json`) 에 `Read/Write/Edit/Bash/WebSearch` 등 필요한 도구를 이 폴더 범위에서
   허용하도록 등록해두세요. (Claude Code 안에서 "이 명령을 항상 허용" 을 선택하거나,
   update-config 관련 설정으로 permission을 사전 승인해두는 방식입니다.) 이 설정 없이 그냥 두면
   한밤중에 승인 대기 상태로 멈춰 있을 수 있습니다.
4. 아래 두 명령을 노트북의 PowerShell(관리자 권한 불필요)에서 실행해 작업 스케줄러에 등록합니다.

```powershell
schtasks /create /tn "CardNightlyScout" /tr "powershell.exe -ExecutionPolicy Bypass -File \"C:\path\to\Game-Design-and-Planning_resarch\automation\nightly_scout.ps1\"" /sc daily /st 23:05
```

```powershell
schtasks /create /tn "CardNightlyExecutor" /tr "powershell.exe -ExecutionPolicy Bypass -File \"C:\path\to\Game-Design-and-Planning_resarch\automation\nightly_executor.ps1\"" /sc daily /st 00:40
```

5. 등록 확인: `schtasks /query /tn "CardNightlyScout"` / `schtasks /query /tn "CardNightlyExecutor"`
6. 삭제하고 싶을 때: `schtasks /delete /tn "CardNightlyScout" /f` (Executor도 동일하게)

## 갱신 주기 규칙 (이 스크립트들이 지키는 약속)

| 대상 | 주기 | 처리 위치 |
|---|---|---|
| 신호(다이제스트) | 주 1회 (마지막 다이제스트 후 7일 경과 시) | `nightly_executor.ps1` 2-b |
| 신규 카드 | 하루 최소 1회, 세션 예산 닿는 만큼 | `nightly_executor.ps1` 2 |
| 기존 카드 수정 | 신규 카드 누적 10장 초과 시 | `nightly_executor.ps1` 2-c |

`research/_automation_state.md` 가 누적 카운터(`pending_new_cards`)와 마지막 다이제스트 날짜
(`last_signal_digest`)를 기억하는 상태 파일입니다. 사람이 직접 수정할 필요는 없습니다.

## 안전장치

- 큐에서 `[ ]` (미체크) 상태인 항목은 사람이 고르기 전까지 실행기가 절대 건드리지 않습니다.
- 카드 생성/수정은 항상 로컬 파일에만 반영되고, 커밋·푸시는 사람의 몫입니다.
- `4_updater.md` 처리 중 "conflict"로 분류된 항목은 카드에 자동 반영하지 않고
  `research/_automation_state.md` 하단 "## 사람 확인 필요" 목록에 쌓아둡니다.
