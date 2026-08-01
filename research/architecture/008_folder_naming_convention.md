+++ 
card_id = "ARCH-008"
type = "convention"
title = "폴더·네이밍 규약"
summary = "새 파일을 어디에 두고 무슨 이름을 붙일지 미리 정해두어, 사람과 AI가 매번 고민하거나 서로 다르게 놓는 일을 없애는 약속"
tags = ["convention", "naming", "folder", "project-structure", "unity", "workflow"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)와 저장소 실제 관례에서 도출
+++ 
## 문제

파일 놓을 자리와 이름 규칙이 없으면, 같은 종류의 코드가 세 곳에 흩어지고 이름이 제각각이 된다. 특히 AI가 코드를 생성하는 이 프로젝트에서는 매번 다른 자리에 다른 이름으로 만들어 놓기 쉽고, 그러면 나중에 무엇이 어디 있는지 아무도 모른다. 쉽게 말해: 물건마다 놓는 서랍을 정해두면 눈 감고도 찾지만, 아무 데나 넣으면 매번 온 집을 뒤져야 한다. 이 카드가 서랍 이름표다.

## 구조

- 코드 폴더 지도 [출처: reference/unity_project_baseline.md 기준 구조]
- `Scripts/Core/` — GameManager, SaveSystem, EventBus. 게임 전체 수명 동안 살아 있는 것.
- `Scripts/World/` — ChunkLoader 등 월드 구성·스트리밍.
- `Scripts/Player/` — PlayerController, PlayerInput.
- `Scripts/Interaction/` — IInteractable 및 상호작용 처리.
- `Scripts/NPC/` — NPC 상태머신.
- `Scripts/Commentator/` — AI 해설자.
- 비코드 폴더 — `Scenes/`(Boot, World_Base, Chunk_x_y), `Prefabs/`, `Tilemaps/`, `Data/`.
- 리서치 저장소 쪽 규약(별도 체계) — 카드 파일은 `research/<종류>/번호_영문_스네이크.md`, 카드 ID는 `<접두어>-###`. 아키텍처 카드는 `research/architecture/`와 `ARCH-###`.

## 핵심 규칙

- 배치 판단은 "누가 이걸 소유하는가"로 정한다. 플레이어만 쓰면 Player, 월드 전체가 쓰면 World, 게임 전체가 쓰면 Core.
- 어디에 둘지 애매하면 Core에 넣지 않는다. Core가 잡동사니 서랍이 되는 순간 구조가 무너진다. 애매하면 사람에게 묻는다.
- 구조 자체의 변경(새 최상위 폴더 추가 등)은 사람 승인이 필요하다. [출처: reference/unity_project_baseline.md]
- 파일 이름 = 그 안의 주된 클래스 이름. C# 스크립트는 파스칼 표기(PlayerController.cs), 인터페이스는 접두어 I(IInteractable).
- 씬 이름은 역할이 드러나게. 청크는 `Chunk_x_y`로 좌표를 이름에 담는다 — ARCH-003 로더가 이름으로 씬을 찾으므로 임의 변경 금지.
- 리서치 카드 ID는 `_index.md`가 단일 발급처다. 임의로 새 ID를 만들지 않는다.
- 임시 이름 금지: Test, New, Temp, Untitled, Copy가 들어간 이름을 커밋하지 않는다.

## Unity 구현 절차

1. 새 파일을 만들기 전에 소유자를 정한다(위 판단 기준). 소유자가 정해지면 폴더가 정해진다.
2. 기존 폴더에 같은 역할의 파일이 있는지 먼저 확인한다. 있으면 옆에 둔다.
3. 파일 이름을 클래스 이름과 같게 맞춘다. Unity는 MonoBehaviour의 파일명과 클래스명이 다르면 컴포넌트로 붙지 않는다.
4. 계획 보고서에 파일 경로를 정확히 적는다. Developer AI는 계획에 없는 파일을 만들지 않는다. [출처: reference/unity_project_baseline.md 작업 순서]
5. 데이터는 코드와 분리한다 — 수치·대사·경로 같은 값은 `Data/`로, 코드는 규칙만.
6. 폴더가 필요해 보이면 만들기 전에 사람에게 승인을 받는다.

## 안티패턴

- Core 비대화: 판단이 어려운 것을 전부 Core에 넣는 습관. 결국 Core가 프로젝트의 절반이 되고, 무엇이 진짜 공용인지 알 수 없게 된다.
- 기능별 폴더와 계층별 폴더 혼용: 어떤 것은 기능(Player)으로, 어떤 것은 종류(Managers, Utils)로 나누는 방식. 두 기준이 섞이면 같은 파일이 두 곳 다 어울려 보여 매번 다른 결정이 난다.
- Utils / Common / Misc 폴더: 이름이 아무 정보도 주지 않는 폴더. 여기 들어간 파일은 다시 나오지 못한다.
- 파일명·클래스명 불일치: Unity에서 조용히 컴포넌트가 안 붙는 원인이며 초보자가 가장 오래 헤매는 실수다.
- 씬 이름 임의 변경: `Chunk_x_y` 규칙을 어기면 로더가 찾지 못한다. 이름이 곧 데이터인 경우가 있다.
- 규약을 문서에만 두고 검사하지 않기: 규약은 지켜지는지 확인할 방법이 있을 때만 유지된다. 검사 가능한 형태로 적는다.

## 검증 방법

- 컴파일 에러 0개, 콘솔 에러 0개. [출처: reference/unity_project_baseline.md 자체 점검 기준]
- 배치 검사: 커밋된 새 스크립트가 전부 위 6개 폴더 중 하나에 있는지 확인. 최상위나 잘못된 폴더에 있으면 불합격.
- 이름 검사: MonoBehaviour 스크립트의 파일명과 클래스명이 일치하는지 확인.
- 금지어 검사: 파일명에 Test/New/Temp/Untitled/Copy가 포함된 파일이 없어야 한다(테스트 폴더 내 정식 테스트는 예외).
- 씬 이름 검사: Chunk 씬 이름이 좌표 규칙을 따르고 Build Settings에 등록되어 있는지 확인.
- 계획 일치 검사: devreport의 변경 파일 목록이 계획서의 파일 목록과 일치하는지 확인. [출처: reference/unity_project_baseline.md 보고서 양식]

## 조합 궁합

- ARCH-002 (씬 스트리밍): 씬 이름 규칙의 근거지. 이름이 로더의 입력이라는 점에서 두 카드는 붙어 있다.
- ARCH-010 (로그 규약): 같은 성격의 규약 카드. 규약은 "지식"이 아니라 "합의"이므로 변경 시 사람 승인이 필요하다는 점이 공통이다.
- ARCH-001 (이벤트 버스): 이벤트 타입 정의를 Core에만 두는 규칙이 이 카드의 배치 원칙과 같은 근거에서 나온다.
- ARCH-022 (어셈블리 정의 모듈 경계): 이 규약의 폴더 구분선이 그대로 모듈 경계선이 된다. 폴더가 먼저 정해져 있어야 어디서 어셈블리를 자를지가 논쟁이 아니다.
- ELEM-013 (도트 그래픽 아트 스타일): 궁합 참고 — 픽셀 아트 파이프라인은 스프라이트·타일맵 자산이 빠르게 늘어나므로, `Tilemaps/`와 `Prefabs/` 하위 규약을 코드 폴더만큼 일찍 정해두는 편이 좋다.
