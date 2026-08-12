# ⑤ 아키텍처 색인 (자동 생성 - 직접 수정 금지)
생성: 2026-08-12 | 27장

- ARCH-001 | Event Bus (EventBus / Pub-Sub) | A loose coupling structure where systems never call each other directly: senders broadcast events to a central station (EventBus), and only the parties that want to listen subscribe and react | #decoupling #core #commentator #2d-open-world #unity #pub-sub | 07-31
- ARCH-002 | Scene Streaming (Boot / World_Base / Chunk Additive Structure) | A world composition approach that never builds the game as one monolithic scene, splitting it into startup, always-on and fragment scenes, then adding only the fragments needed and switching them on and off | #scene #streaming #additive #open-world #core #unity #2d | 07-29
- ARCH-003 | Chunk Loader (3x3 Active Rule) | A loading manager that keeps only the surrounding 3x3 chunks active around the tile the player stands on and switches off the ones left behind, holding a wide world at a constant cost | #streaming #chunk #world #performance #open-world #unity #2d | 07-29
- ARCH-004 | Save System (JSON Serialization) | A structure that turns game state into a human-readable JSON document, writes it safely to the per-platform save path, and restores it | #save #persistence #json #core #unity #data | 07-29
- ARCH-005 | NPC 상태머신 (Idle / Patrol / Talk) | NPC의 행동을 여러 개의 '상태'로 나누고 한 번에 하나만 켜지게 해서, 조건에 따라 상태를 갈아타는 방식으로 행동을 만드는 구조 | #npc #fsm #state-machine #ai-behavior #unity #2d | 07-29
- ARCH-006 | 상호작용 (IInteractable 인터페이스 + Trigger) | 말 걸기·줍기·열기처럼 서로 다른 행동을 '상호작용할 수 있다'는 하나의 약속으로 묶어, 플레이어가 대상의 정체를 몰라도 다룰 수 있게 하는 구조 | #interaction #interface #trigger #player #unity #2d | 07-29
- ARCH-007 | 해설자 파이프라인 (구독 → 반응 생성 → 로그) | AI 해설자가 게임 사건 방송을 듣고, 반응을 만들고, 반드시 한 줄 로그를 남기는 3단 처리 흐름 | #commentator #ai #pipeline #logging #core #unity | 08-01
- ARCH-008 | 폴더·네이밍 규약 | 새 파일을 어디에 두고 무슨 이름을 붙일지 미리 정해두어, 사람과 AI가 매번 고민하거나 서로 다르게 놓는 일을 없애는 약속 | #convention #naming #folder #project-structure #unity #workflow | 07-29
- ARCH-009 | 2D 물리 이동 (Rigidbody2D) | 캐릭터를 좌표로 순간이동시키지 않고 물리 엔진에 '이렇게 움직여 달라'고 부탁해서, 벽과 충돌이 제대로 동작하게 만드는 이동 방식 | #physics #rigidbody2d #movement #player #unity #2d | 07-29
- ARCH-010 | 로그 규약 (QA 판정용) | 게임이 남기는 기록의 형식과 위치를 미리 못 박아, QA AI가 사람의 감각이 아니라 관찰 가능한 증거로 합격·불합격을 판정할 수 있게 하는 약속 | #logging #convention #qa #verification #observability #unity | 07-29
- ARCH-011 | Boot 부트스트랩 & 매니저 수명 (DontDestroyOnLoad) | 게임이 켜질 때 딱 한 곳에서만 관리자들을 만들고, 그 관리자들만 씬이 바뀌어도 죽지 않게 남겨서 '누가 언제까지 살아 있는가'를 헷갈리지 않게 하는 방식 | #bootstrap #lifetime #manager #scene #core #unity | 07-31
- ARCH-012 | Data/ 데이터 자산 규약 (ScriptableObject 테이블) | 아이템 능력치나 확률표 같은 설정값을 코드 안에 박아넣지 않고 프로젝트의 데이터 파일로 따로 빼서, 코드를 안 고치고도 수치를 바꿀 수 있게 하는 규칙 | #data #scriptableobject #convention #balance #unity #authoring | 07-30
- ARCH-013 | 2D 카메라 추적 (Cinemachine 3 + 경계 제한 + 픽셀 퍼펙트) | 카메라를 캐릭터에 그냥 붙이지 않고 '따라가는 전용 부품'에 맡겨서, 부드럽게 쫓아가면서도 월드 밖 빈 공간은 보여주지 않게 만드는 방식 | #camera #cinemachine #pixel-perfect #2d #unity #world-base | 07-30
- ARCH-014 | UI 캔버스 구조 (World_Base 정적/동적 분리) | 화면 UI를 한 덩어리로 두지 않고 '거의 안 변하는 것'과 '자주 변하는 것'으로 나눠 담아서, 체력바 한 칸 바뀔 때 화면 전체를 다시 그리지 않게 하는 배치 | #ui #canvas #performance #world-base #unity #structure | 07-30
- ARCH-015 | 오브젝트 풀링 (UnityEngine.Pool ObjectPool<T>) | 총알·이펙트처럼 자주 생기고 사라지는 오브젝트를 매번 만들고 없애지 않고, 미리 만들어둔 재고를 빌렸다 반납하는 방식으로 순간적인 성능 부담을 없애는 구조 | #pooling #performance #objectpool #bullet #vfx #unity | 07-31
- ARCH-016 | 입력 시스템 (Input System 패키지 + InputActionAsset) | 키보드·게임패드 같은 서로 다른 장치의 버튼을 코드에 흩어 적지 않고, '이동'·'상호작용' 같은 행동 이름 하나에 여러 장치의 입력을 미리 묶어두는 입력 처리 구조 | #input #inputsystem #inputaction #player #unity #2d | 07-31
- ARCH-017 | 오디오 매니저 (AudioSource 풀 + BGM/SFX 분리) | 소리를 재생할 때마다 AudioSource를 새로 만들지 않고, BGM 전용과 SFX 풀을 미리 나눠 관리해서 겹쳐 재생되는 효과음도 끊기지 않게 하는 구조 | #audio #sfx #bgm #pooling #singleton #unity | 07-31
- ARCH-018 | 게임 매니저 (전역 게임 상태: Playing / Paused / GameOver) | 지금 게임이 진행 중인지, 멈춰 있는지, 끝났는지를 여러 스크립트가 각자 판단하지 않고, 딱 한 곳(GameManager)이 들고 있다가 물어보면 답해주는 구조 | #gamemanager #singleton #game-state #core #unity #2d | 07-31
- ARCH-020 | 애니메이션 상태 머신 (Animator Controller / Animation State Machine) | 캐릭터의 애니메이션 클립을 코드에서 직접 재생하지 않고, 상태(State)와 전환 조건(Transition)으로 미리 짜둔 그래프에 맡겨 파라미터만 바꾸면 알맞은 동작이 자동으로 이어지게 하는 구조 | #animation #animator #state-machine #unity #pattern #player | 07-31
- ARCH-021 | 인벤토리 시스템 (Inventory / Item Database, ScriptableObject 기반) | 아이템의 '정의'(이름, 아이콘, 능력치)와 '보유 상태'(개수, 내구도)를 분리해, 데이터 자산 하나로 여러 캐릭터·슬롯이 같은 아이템 정보를 공유하게 만드는 구조 | #inventory #item #scriptableobject #rpg #unity #pattern | 07-31
- ARCH-022 | 어셈블리 정의 모듈 경계 (Assembly Definition / asmdef) | 스크립트 폴더마다 어셈블리 정의 파일을 두어 모듈의 경계와 의존 방향을 컴파일러가 강제하게 만드는 프로젝트 분할 규약 | #asmdef #module #dependency #compile-time #convention #unity #project-structure | 08-02
- ARCH-023 | 게임 흐름 구조 (Boot → 타이틀 → 플레이 → 결과 씬 전이) | 씬을 아무 스크립트나 부르지 않고 흐름 담당자 한 곳이 허용된 전이만 비동기로 수행하게 만드는 게임 전체 골격 | #scene-flow #game-loop #loadsceneasync #structure #unity #core | 08-02
- ARCH-024 | 타일맵 레벨 구조 (Grid + 다중 Tilemap + Composite Collider 2D) | 2D 맵을 스프라이트 오브젝트로 하나씩 놓지 않고 격자 위 여러 겹의 타일맵으로 나눠 그리기·충돌·판정을 겹별로 분리하는 레벨 구성 방식 | #tilemap #grid #collider #level-design #2d #unity #performance | 08-02
- ARCH-025 | 2D 정렬 순서 규약 (Sorting Layer / Order in Layer / Y축 정렬) | 2D에서 무엇이 무엇 앞에 그려지는지를 개별 오브젝트의 좌표 조정이 아니라 프로젝트 전체가 공유하는 정렬 층과 축 규칙으로 정하는 약속 | #sorting #sprite #render-order #convention #2d #unity | 08-02
- ARCH-026 | 스프라이트 아틀라스 & 드로우콜 배칭 (Sprite Atlas) | 흩어진 스프라이트를 큰 텍스처 한 장으로 묶어 GPU에 보내는 그리기 요청 횟수를 줄이는 자산 묶음 규약 | #sprite-atlas #draw-call #batching #performance #2d #unity #asset | 08-02
- ARCH-027 | URP 2D 라이팅 (2D Renderer + Light 2D + Shadow Caster 2D) | 2D 화면의 밝기와 분위기를 스프라이트에 그려 넣지 않고 조명 오브젝트와 정렬 레이어별 영향 범위로 조립하는 렌더링 구조 | #lighting #urp #light2d #rendering #2d #unity #atmosphere | 08-02
- ARCH-028 | 피격·대미지 인터페이스 (IDamageable + 체력 컴포넌트) | 때리는 쪽이 맞는 쪽의 정체를 모르게 '피해를 받을 수 있다'는 하나의 약속으로 묶어, 적·플레이어·상자를 같은 방식으로 다루는 전투 구조 | #combat #damage #interface #health #pattern #unity #2d | 08-02
