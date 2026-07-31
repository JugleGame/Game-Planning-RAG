+++ 
card_id = "ARCH-001"
type = "pattern"
title = "이벤트 버스 (EventBus / Pub-Sub)"
summary = "시스템끼리 직접 부르지 않고, 가운데 방송국(EventBus)에 사건을 방송하면 듣고 싶은 쪽만 구독해서 반응하는 느슨한 연결 구조"
tags = ["decoupling", "core", "commentator", "2d-open-world", "unity", "pub-sub"]
updated = "2026-07-31"
confidence = "high" # 프로젝트 기준 구조(prompts/5_developer.md)의 방송 규칙과 동일 + Unity 공식 아키텍처 자료 근거
+++ 
## 문제

게임 시스템이 서로를 직접 참조하면(PlayerController가 Commentator를 직접 부르고, NPC가 UI를 직접 부르는 식) 하나를 고칠 때마다 연결된 전부가 깨진다. 특히 이 프로젝트의 AI 해설자(Commentator)는 전투·획득·대화·진입 등 거의 모든 사건을 알아야 하는데, 직접 참조로 만들면 해설자가 모든 시스템에 빨대를 꽂은 괴물이 된다. 쉽게 말해: 반 친구들이 서로서로 귓속말로 소식을 전하면 한 명이 결석했을 때 소식이 끊기지만, 교실 스피커로 방송하면 듣고 싶은 사람만 들으면 된다. EventBus가 그 스피커다.

## 구조

- 위치: `Assets/Scripts/Core/EventBus.cs` [출처: prompts/5_developer.md 기준 구조]
- 흐름: 발신자(Player, NPC, World) → `EventBus.Publish(GameEvent)` → 구독자(Commentator, UI, SaveSystem)가 각자 반응
- `GameEvent`는 이벤트 ID·발생 주체·좌표·페이로드를 담는 직렬화 가능한 데이터 묶음으로 `Scripts/Core/`에 정의한다.
- 발신자는 누가 듣는지 모르고, 구독자는 누가 보냈는지에 의존하지 않는다. 둘 다 EventBus 하나만 안다.
- 구현 선택지는 C# `event/Action` 기반 정적 버스, 또는 ScriptableObject 이벤트 채널 방식이 있다. [출처: Unity 공식 e-book "Level up your code with design patterns" 및 Unite 2017 Ryan Hipple 강연 "Game Architecture with Scriptable Objects" — Schell Games가 실제 상용 프로젝트에 적용한 방식] [해석] 본 프로젝트는 씬이 Additive로 자주 갈리는 구조라, 씬 수명에 묶이지 않는 정적 버스 또는 SO 채널이 안전하다.

## 핵심 규칙

- 방송 규칙: 플레이어 행동(전투, 획득, 대화, 진입)은 반드시 `EventBus.Publish(GameEvent)`로 방송한다. 직접 참조 금지. [출처: prompts/5_developer.md]
- 해설자 시스템은 이 방송에만 의존한다. Commentator가 다른 시스템의 필드를 직접 읽으면 규칙 위반이다. [출처: prompts/5_developer.md]
- 구독자는 `OnEnable`에서 구독하고 `OnDisable`에서 반드시 해지한다. 해지를 빼먹으면 파괴된 오브젝트를 부르다 터진다.
- 이벤트 타입 정의는 `Scripts/Core/`에만 둔다. Chunk 씬 안의 스크립트가 자기만의 이벤트 타입을 만들지 않는다.

## Unity 구현 절차

1. `Scripts/Core/GameEvent.cs` 생성 — 이벤트 ID(enum), 주체, 페이로드 필드 정의.
2. `Scripts/Core/EventBus.cs` 생성 — `Publish(GameEvent)`, `Subscribe(Action<GameEvent>)`, `Unsubscribe(...)` 3개 공개 함수만 노출.
3. 발신 지점 연결 — PlayerController(전투/획득), Interaction(대화), ChunkLoader(진입)에서 해당 사건 발생 시 `Publish` 호출 한 줄 추가.
4. 구독 지점 연결 — Commentator가 `OnEnable`에서 구독, 반응 생성 후 `Logs/commentator.log`에 `[시각] [이벤트ID] [반응요약]` 한 줄 기록. [출처: prompts/5_developer.md 로그 규칙]
5. 자체 점검 — 컴파일 에러 0, 콘솔 에러 0 확인 후 커밋.

## 안티패턴

- 직접 참조 연결: `FindObjectOfType`이나 public 필드 드래그로 시스템끼리 묶는 방식. Chunk 씬이 Additive로 내려가는 순간 참조가 끊겨 NullReference가 난다. [해석] 이 프로젝트처럼 씬을 켜고 끄는 구조에서 가장 자주 터지는 유형이다.
- 만능 이벤트: 모든 것을 이벤트로 쏘는 남용. 프레임마다 위치를 방송하는 식이면 버스가 소음으로 가득 차 디버깅이 불가능해진다. 이벤트는 "사건"(죽었다, 얻었다, 들어왔다)에만 쓴다.
- 구독 해지 누락: 씬 언로드 후에도 구독이 남아 유령 구독자가 쌓이는 메모리 누수. Unity 공식 자료도 이벤트 구독 해지 누락을 대표적 실수로 꼽는다. [출처: Unity 공식 e-book "Level up your code with design patterns"의 Observer 패턴 장]
- 이벤트 안에서 이벤트 발행 연쇄: A 이벤트 처리 중 B를 발행하고 B가 다시 A를 부르는 순환. 발행 깊이 제한 또는 큐 처리로 막는다.

## 검증 방법

- 컴파일 에러 0개, 콘솔 에러 0개. [출처: prompts/5_developer.md 자체 점검 기준]
- `Logs/commentator.log`에 이벤트당 한 줄 형식 `[시각] [이벤트ID] [반응요약]`이 남는지 QA가 로그로 판정. [출처: prompts/5_developer.md 로그 규칙]
- 느슨함 테스트: Commentator 오브젝트를 씬에서 제거해도 게임 본편이 에러 없이 돌아가야 한다. 돌아가지 않으면 어딘가 직접 참조가 숨어 있다는 뜻이다.
- 방송 누락 테스트: 전투·획득·대화·진입 4종 행동을 각 1회 수행했을 때 로그에 4줄이 남아야 한다.

## 조합 궁합

- ELEM-005 (AI 통합): AI 해설자가 실시간 반응을 만들려면 사건 스트림이 필요하다. EventBus가 그 공급선이라 사실상 전제 조건이다.
- 궁합 좋음 — 저장 시스템: SaveSystem이 "무슨 일이 있었나"를 이벤트 구독으로 수집하면 저장 로직이 게임플레이 코드에 침투하지 않는다.
- ARCH-018 (게임 매니저): 전역 게임 상태(Playing/Paused/GameOver)가 바뀔 때 이 버스로 방송한다. UI·입력·오디오가 GameManager를 직접 참조하지 않게 만드는 유일한 통로다.
- ARCH-014 (UI 캔버스 구조): 동적 캔버스는 버스 구독으로만 갱신한다 — 매 프레임 폴링 대신 사건이 왔을 때만 다시 그리는 것이 정적/동적 분리의 전제다.
- 충돌 주의 — 즉시성이 필요한 물리 반응(피격 넉백 등)은 버스를 거치지 말고 해당 컴포넌트 안에서 직접 처리한다. 버스는 "알림"용이지 "제어"용이 아니다.
