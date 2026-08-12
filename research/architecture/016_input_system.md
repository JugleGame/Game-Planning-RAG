+++
card_id = "ARCH-016"
type = "structure"
title = "입력 시스템 (Input System 패키지 + InputActionAsset)"
summary = "키보드·게임패드 같은 서로 다른 장치의 버튼을 코드에 흩어 적지 않고, '이동'·'상호작용' 같은 행동 이름 하나에 여러 장치의 입력을 미리 묶어두는 입력 처리 구조"
tags = ["input", "inputsystem", "inputaction", "player", "unity", "2d"]
updated = "2026-07-31"
confidence = "high"
+++
## Problem
`Input.GetKeyDown("space")`처럼 장치와 키를 코드에 직접 박아 넣으면, 게임패드
지원을 추가하거나 키 재배정 기능을 넣을 때마다 여러 스크립트를 뒤져 고쳐야 한다.
행동("점프")과 장치별 버튼("스페이스바" 또는 "패드 남쪽 버튼")을 분리해두지 않은
탓이다.

## Structure
- Unity의 Input System 패키지는 `InputActionAsset` 자산 하나에 "행동(Action)"을
  정의하고, 각 행동에 여러 장치의 바인딩(키보드 방향키, 패드 스틱 등)을 매핑한다
  [source: Unity Input System Manual, Input Action Assets,
  https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/manual/ActionAssets.html].
- `PlayerInput` 컴포넌트를 플레이어 오브젝트에 붙이고 이 Action Asset을 연결하면,
  행동이 발생할 때 지정한 메서드를 호출해준다 [source: Unity Input System Manual,
  The Player Input component,
  https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/manual/PlayerInput.html].
- 2D 이동처럼 상하좌우 네 방향을 하나의 벡터로 합쳐야 하는 입력은 "2D Vector
  Composite"로 구성한다 [source: Unity Input System Manual, Quick start guide,
  https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/manual/QuickStartGuide.html].
- 이 프로젝트는 `Scripts/Player/`에 `PlayerInput` 처리 스크립트를 두고,
  `PlayerController`(ARCH-009 Rigidbody2D 이동)는 입력값을 직접 폴링하지 않고
  이 스크립트가 넘겨주는 값만 받는다.

## Core Rules
- 행동 이름(Move, Interact 등)은 장치를 언급하지 않는다 — "스페이스바를 누르면"이
  아니라 "상호작용 행동이 발생하면"으로 코드가 반응해야 장치 추가·재배정이 코드
  변경 없이 가능하다.
- 입력 읽기와 게임 로직을 분리한다: 입력 스크립트는 값을 만들어 전달만 하고,
  이동·상호작용의 실제 처리는 각자의 스크립트(PlayerController, IInteractable
  대상)가 맡는다 — ARCH-001 이벤트 버스의 방송 규칙과 같은 이유다.
- 씬을 넘나드는 전역 입력(일시정지 등)과 플레이어 전용 입력(이동, 공격)은 서로
  다른 Action Map으로 나눈다. 한 Map에 다 넣으면 UI가 떠 있을 때도 이동 입력이
  같이 반응하는 문제가 생긴다.

## Unity Implementation Steps
1. `Packages/manifest.json`에 Input System 패키지가 있는지 먼저 확인한다 — 없으면
   패키지 추가이므로 reference/unity_project_baseline.md의 금지 목록(패키지 추가는 사람 승인 필요)에
   해당해 사람에게 먼저 확인한다.
2. `InputActionAsset`을 만들고 Action Map(예: Player)과 행동(Move, Interact 등)을
   정의한다. Move는 2D Vector Composite로 WASD/방향키/패드 스틱을 함께 바인딩한다.
3. 플레이어 프리팹에 `PlayerInput` 컴포넌트를 붙이고 이 Asset을 연결한다.
4. Behavior를 이 프로젝트의 이벤트 방송 규칙에 맞게 선택한다 — 직접 참조를
   늘리는 Unity Events보다, C# 이벤트나 콜백으로 값만 넘기는 방식을 우선한다.
5. `PlayerController`, 상호작용 트리거 등 소비자는 입력 스크립트가 넘긴 값만
   받고, `Input System` API를 직접 호출하지 않는다.

## Anti-patterns
- 여러 스크립트가 각자 `Keyboard.current` 등으로 직접 장치를 폴링 — 행동과
  바인딩이 다시 코드에 흩어져 이 카드가 해결하려던 문제가 재발한다.
- Action Map을 나누지 않고 UI 입력과 플레이어 입력을 한 Map에 몰아넣어, 메뉴가
  열려 있을 때도 캐릭터가 움직이는 버그.
- 구식 `Input` 매니저(Input Manager)와 새 Input System을 한 프로젝트에 혼용해서
  같은 키 입력이 두 번 처리되는 것.

## Verification
- 키보드와 게임패드 각각으로 이동·상호작용 행동을 1회씩 수행해 동일한 게임
  반응이 나오는지 확인 — 장치 무관 동작이 이 구조의 핵심 합격 기준이다.
- 메뉴/일시정지 UI가 열린 상태에서 플레이어 이동 입력이 씬에 전달되지 않는지
  Action Map 전환 로그로 확인.
- 콘솔 에러 0개, 특히 "No Action Map" 류의 바인딩 누락 경고 0건.

## Synergy
- ARCH-009 (2D 물리 이동, Rigidbody2D): Move 행동의 벡터값을 그대로 물리 이동
  입력으로 넘겨받는 가장 직접적인 소비자.
- ARCH-006 (상호작용, IInteractable): Interact 행동이 눌렸을 때 트리거 범위 안의
  IInteractable 대상을 호출하는 연결점.
