+++
card_id = "ARCH-015"
type = "pattern"
title = "오브젝트 풀링 (UnityEngine.Pool ObjectPool<T>)"
summary = "총알·이펙트처럼 자주 생기고 사라지는 오브젝트를 매번 만들고 없애지 않고, 미리 만들어둔 재고를 빌렸다 반납하는 방식으로 순간적인 성능 부담을 없애는 구조"
tags = ["pooling", "performance", "objectpool", "bullet", "vfx", "unity"]
updated = "2026-07-31"
confidence = "high"
+++
## 문제
총알, 히트 이펙트, 적 스폰처럼 짧게 살고 자주 반복해서 생기는 오브젝트를 매번
`Instantiate`/`Destroy`로 만들고 없애면, 순간적으로 몰릴 때마다 메모리 할당과
가비지 컬렉션이 겹쳐 프레임이 튄다 [출처: Unity Manual, Pooling and reusing objects,
https://docs.unity3d.com/6000.4/Documentation/Manual/performance-reusable-code.html].
재고를 미리 만들어두고 빌렸다 돌려받는 편이 싸다.

## 구조
- Unity 6000(2021.3 이상)부터 `UnityEngine.Pool` 네임스페이스에 `ObjectPool<T>`가
  내장되어 있다. 생성/대여/반납/파괴 시점마다 실행할 델리게이트를 생성자에 넘겨
  동작을 정의하는 스택 기반 풀이다 [출처: Unity Scripting API, Pool.ObjectPool_1,
  https://docs.unity3d.com/6000.5/Documentation/ScriptReference/Pool.ObjectPool_1.html].
- 이 프로젝트에서는 총알·이펙트 등 반복 스폰 대상마다 `Core/`에 풀 하나씩 두거나,
  공용 매니저가 프리팹별 풀을 딕셔너리로 들고 있는 두 방식 중 하나를 스펙 단계에서
  선택한다. 임의로 섞지 않는다.
- 콜백 4종: createFunc(새로 만들 때), actionOnGet(꺼낼 때 활성화), actionOnRelease
  (반납할 때 비활성화), actionOnDestroy(풀 최대치 초과로 실제 파괴할 때).

## 핵심 규칙
- `Destroy()`를 직접 호출하지 않는다 — 풀 대상은 항상 `Release()`로 돌려준다.
  `Destroy`를 쓰면 풀의 재고 수가 어긋나 다음 `Get()`이 예상과 다른 개수를 새로 만든다.
- `actionOnGet`/`actionOnRelease`에서 위치·속도·타이머 등 이전 사용 흔적을 반드시
  초기화한다 — 재사용 오브젝트는 이전 상태를 들고 있다는 것이 일반 Instantiate와의
  핵심 차이다.
- `defaultCapacity`와 `maxSize`는 스펙의 예상 동시 발생 개수를 근거로 정한다.
  근거 없이 임의로 크게 잡지 않는다 (메모리 낭비) — 근거 없이 작게 잡지도 않는다
  (풀이 매번 넘쳐 새로 생성).
- `collectionCheck`(중복 반납 감지)는 개발 중 켜두고, 같은 인스턴스를 두 번
  `Release()`하는 버그를 조기에 잡는다.

## Unity 구현 절차
1. 풀링 대상(총알, 이펙트 등)의 프리팹과 최대 동시 개수를 스펙에서 확인한다.
2. 대상 스크립트에 풀로부터 빌린 것임을 표시하는 참조를 두어, 스스로 수명이
   끝나면(충돌·타이머 만료) `Release()`를 호출하게 만든다 — 자기 자신을 반납한다.
3. 풀 소유 주체를 정한다: 총알처럼 발사자가 다양하면 공용 매니저 풀, 특정 오브젝트
   전용이면 그 오브젝트가 직접 풀을 들고 있는 구조.
4. `actionOnGet`에서 `SetActive(true)`와 상태 초기화, `actionOnRelease`에서
   `SetActive(false)`를 짝지어 넣는다 — 이 두 콜백이 비어 있으면 풀링 효과가 없다.
5. 씬 전환 시 풀을 비우는지, `DontDestroyOnLoad`로 유지하는지 스펙/ARCH-011
   부트스트랩 규칙과 맞춰 결정한다.

## 안티패턴
- `Instantiate`와 `Destroy`를 그대로 두고 이름만 "풀"이라고 부르는 가짜 풀링 —
  할당 비용이 그대로 남는다.
- 풀에서 꺼낸 오브젝트의 이전 상태(체력, 속도, 구독한 이벤트)를 초기화하지 않아
  "가끔 이상한 상태로 나타나는" 재현하기 어려운 버그를 만드는 것.
- 최대치 없이 무한정 키우는 풀 — 스폰이 몰리는 상황에서 메모리가 계속 불어난다.

## 검증 방법
- 총알처럼 빈번한 스폰 오브젝트를 다수 연속 발생시키는 동안 프로파일러의
  GC Alloc이 프레임당 0에 가까운지 확인한다 [출처: Unity Manual, Pooling and
  reusing objects].
- 풀 대상을 반복 재사용한 뒤에도 이전 회차의 상태(속도, 색상 등)가 남지 않는지
  콘솔 로그나 인스펙터로 관찰한다.
- 콘솔 에러 0개, 특히 collectionCheck로 잡히는 "이미 반납된 항목을 또 반납" 경고
  0건.

## 조합 궁합
- ARCH-001 (이벤트 버스): 총알 소멸·적 처치 같은 사건을 방송해 풀 반납 시점을
  이벤트로 트리거하면 발사 로직과 풀 관리 로직이 분리된다.
- ELEM-004 (반복 메커닉): 로그라이크형 전투처럼 짧은 반복 루프가 많은 장르일수록
  풀링의 성능 이득이 커진다.
