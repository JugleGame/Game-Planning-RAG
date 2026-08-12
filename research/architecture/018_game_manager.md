+++
card_id = "ARCH-018"
type = "structure"
title = "게임 매니저 (전역 게임 상태: Playing / Paused / GameOver)"
summary = "지금 게임이 진행 중인지, 멈춰 있는지, 끝났는지를 여러 스크립트가 각자 판단하지 않고, 딱 한 곳(GameManager)이 들고 있다가 물어보면 답해주는 구조"
tags = ["gamemanager", "singleton", "game-state", "core", "unity", "2d"]
updated = "2026-07-31"
confidence = "medium"
+++
## Problem
"지금 일시정지 상태인가?", "게임이 끝났는가?" 같은 질문에 여러 스크립트가 각자
`Time.timeScale`이나 자체 변수로 답하기 시작하면, 한쪽은 멈췄다고 생각하는데
다른 쪽은 계속 움직이는 상태 불일치가 생긴다. `reference/unity_project_baseline.md`의 기준 구조는
`Core/`에 GameManager를 EventBus·SaveSystem과 나란히 명시하지만
[source: reference/unity_project_baseline.md, 3절 폴더 지도], 이 프로젝트에는 아직 EventBus(ARCH-001)와
SaveSystem(ARCH-004) 카드만 있고 GameManager 자체를 다루는 카드가 없다.

## Structure
- `Core/`에 두는 전역 싱글턴 하나가 "현재 게임 상태"라는 단 하나의 값을 들고 있다.
  상태 목록은 최소 Playing / Paused / GameOver 세 가지에서 시작한다
  [source: Unity GameManager 패턴 정리 보도, uhiyama-lab.com, 2026-07 확인].
- 다른 시스템은 이 상태를 직접 바꾸지 않고 GameManager에 "바꿔달라"고 요청하거나,
  ARCH-001 이벤트 버스를 통해 상태 변경 사건을 구독한다.
- ARCH-011 Boot 부트스트랩 규칙에 따라 Boot 씬에서 딱 한 번 생성되고
  `DontDestroyOnLoad`로 씬 전환에도 살아남는다.

## Core Rules
- 상태를 바꾸는 진입점은 GameManager의 공개 메서드(예: `Pause()`, `Resume()`,
  `EndGame()`) 하나로 좁힌다 — 여러 스크립트가 제각각 `Time.timeScale = 0`을
  직접 건드리면 "누가 멈췄다가 다시 풀었는지"를 추적할 수 없다.
- 상태가 바뀌는 순간 ARCH-001 이벤트 버스로 방송한다. UI, 입력(ARCH-016),
  오디오(ARCH-017) 등 상태에 반응해야 하는 시스템은 GameManager를 직접 참조하지
  않고 이 방송만 구독한다 — 방송 규칙은 플레이어 행동뿐 아니라 게임 상태 변화에도
  동일하게 적용된다.
- GameManager는 "지금 상태가 무엇인가"만 책임진다. 점수 계산, 승패 판정 같은
  구체적 게임 규칙 로직까지 이 안에 몰아넣지 않는다 — 비대해지면 다시 여러
  스크립트가 각자 상태를 흉내 내는 문제로 돌아간다.

## Unity Implementation Steps
1. `Scripts/Core/GameManager.cs`를 만들고 상태를 enum(Playing, Paused, GameOver
   등, 스펙에서 필요한 만큼만)으로 정의한다.
2. Boot 씬에서 인스턴스를 생성하고 ARCH-011 규칙대로 `DontDestroyOnLoad`를
   적용한다. 이미 인스턴스가 있으면 중복 생성을 막는다(싱글턴 가드).
3. 상태 변경 메서드 안에서만 상태 값을 바꾸고, 바뀐 직후 이벤트 버스로
   `GameStateChanged` 류의 이벤트를 방송한다.
4. 일시정지 처리(`Time.timeScale`)는 GameManager 내부에만 두고, UI의 "일시정지
   버튼"은 GameManager의 `Pause()`를 호출하는 방식으로만 접근하게 한다.
5. 씬을 넘나드는 흐름(Boot → World_Base → GameOver 화면 등)이 필요하면 ARCH-002
   씬 스트리밍 규칙과 맞춰, GameManager가 어떤 씬 전환을 트리거할지 스펙에서
   먼저 정한다.

## Anti-patterns
- 여러 스크립트가 각자 `bool isPaused` 같은 지역 플래그를 들고 있는 것 — 하나만
  갱신을 놓쳐도 전체 게임이 반쪽만 멈춘 것처럼 보인다.
- GameManager에 UI 갱신, 사운드 재생, 점수 계산까지 전부 몰아넣어 하나의
  거대한 "만능 매니저"로 만드는 것 — 책임이 한 클래스에 쏠려 수정할 때마다
  전체를 다시 읽어야 한다.
- 상태 전이 규칙 없이 아무 상태로나 즉시 바꾸는 것(GameOver 중에 Pause 요청을
  그대로 받아주는 등) — 상태 조합에 따라 다른 시스템이 잘못된 값을 관찰하게 된다.

## Verification
- 상태 변경 메서드 호출 시마다 이벤트 버스로 방송되는지 로그(ARCH-010 로그
  규약)로 확인 — 상태 전이당 로그 한 줄이 있어야 한다.
- 일시정지 상태에서 플레이어 이동·전투 등 게임플레이 입력이 실제로 멈추는지
  관찰(Time.timeScale 반영 여부).
- 씬 전환 후에도 GameManager 인스턴스가 중복 생성되지 않고 하나만 존재하는지
  확인(싱글턴 가드 동작 여부).
- 콘솔 에러 0개.

## Synergy
- ARCH-001 (이벤트 버스): 상태 변화를 다른 시스템에 전달하는 유일한 통로.
- ARCH-011 (Boot 부트스트랩 & 매니저 수명): GameManager 자체가 이 규칙을 따르는
  대표 사례.
- ELEM-005 (AI 통합): 게임 상태(GameOver 등)에 따라 AI 해설자 반응 여부를
  갈라야 하는 경우, GameManager의 상태 방송이 그 판단 근거가 된다.
