+++
card_id = "ARCH-020"
type = "pattern"
title = "애니메이션 상태 머신 (Animator Controller / Animation State Machine)"
summary = "캐릭터의 애니메이션 클립을 코드에서 직접 재생하지 않고, 상태(State)와 전환 조건(Transition)으로 미리 짜둔 그래프에 맡겨 파라미터만 바꾸면 알맞은 동작이 자동으로 이어지게 하는 구조"
tags = ["animation", "animator", "state-machine", "unity", "pattern", "player"]
updated = "2026-07-31"
confidence = "high"
+++
## 문제
캐릭터가 Idle, Walk, Attack, Hit 같은 여러 동작을 오갈 때, 코드에서
"지금 이 애니메이션을 재생해라"를 매번 직접 지정하면 상태 전환 조건이 스크립트
곳곳에 흩어지고, 어떤 상태에서 어떤 상태로 갈 수 있는지 한눈에 보기 어렵다.
ARCH-005(NPC 상태머신)와 유사한 문제지만, 이건 "행동 로직"이 아니라 "화면에
보이는 애니메이션 재생"에 특화된 문제다.

## 구조
- 기준 형식: Unity의 Animator Controller는 State(애니메이션 클립 하나)와
  Transition(상태 간 전환 조건)으로 구성된 그래프다 [출처: Unity 공식 매뉴얼,
  Animation state machine, docs.unity3d.com, Unity 6 기준].
- Parameter(Bool/Trigger/Float/Int)가 스크립트와 그래프 사이의 유일한 접점이다
  - 코드는 파라미터 값만 바꾸고, 실제로 어떤 애니메이션이 재생될지는 그래프가
  결정한다 [출처: Unity 공식 매뉴얼, Animation Parameters, Unity 6 기준].
- Transition은 조건이 없으면 Exit Time(재생 진행률)만으로 발동하고, 조건이 있으면
  모든 조건이 충족돼야 발동한다 [출처: Unity 공식 매뉴얼, State Machine Transitions].

## 핵심 규칙
- 스크립트는 상태 이름을 직접 다루지 않고 Parameter만 조작한다 - 상태 이름을
  코드에 하드코딩하면 애니메이터 그래프 구조가 바뀔 때마다 스크립트도 고쳐야 한다.
- Trigger 파라미터는 한 번 소비되면 자동 리셋된다는 것을 전제로 설계한다 - Bool과
  혼동하면 "눌렀는데 씹히는" 버그가 생긴다.
- 전환 조건이 겹치면(동시에 여러 조건 충족) 그래프 순서에 따라 예상 밖의 전환이
  일어날 수 있으므로, 상호 배타적인 조건으로 설계한다.

## Unity 구현 절차
1. 캐릭터의 상태 목록(Idle/Walk/Attack/Hit/Die 등)을 스펙에서 먼저 확정한다.
2. Animator Controller에 상태별 State를 만들고 각 State에 애니메이션 클립을 연결한다.
3. 상태 간 Transition을 그래프로 연결하고, 각 Transition에 Parameter 조건을 건다.
4. 스크립트에서는 `Animator.SetBool`/`SetTrigger`/`SetFloat`로 파라미터만 갱신한다.
5. ARCH-005(NPC 상태머신)의 행동 상태와 애니메이션 상태를 1:1로 강제하지 않는다
   - 행동은 "Patrol"이어도 애니메이션은 "Walk"/"Idle"을 오갈 수 있어, 두 계층을
   분리해서 설계한다.

## 안티패턴
- 스크립트에서 `Animator.Play("StateName")`으로 상태 이름을 직접 호출: 그래프의
  전환 조건을 무시하고 강제 전환해 다른 Transition과 충돌할 수 있다.
- 하나의 State에 너무 많은 조건 분기를 넣어 그래프가 거대해지는 것: 서브 상태머신
  (Sub-State Machine)으로 쪼개는 것이 정석.
- Bool 파라미터를 리셋하지 않고 방치: 다음 전환 시 의도치 않은 상태로 튐.

## 검증 방법
- 상태 전환 검사: 각 상태 조합(Idle→Walk, Walk→Attack 등)을 1회씩 수행해 의도한
  애니메이션이 재생되는지 확인.
- 콘솔 청결: 존재하지 않는 파라미터를 `SetTrigger` 등으로 호출할 때 나는 경고가
  정상 플레이 중 0건이어야 한다.
- 회귀 검사: 애니메이터 그래프 수정 후, 기존에 동작하던 전환들이 여전히 동작하는지
  재확인 (그래프 특성상 한 곳 수정이 다른 전환에 영향을 줄 수 있음).

## 조합 궁합
- ARCH-005 (NPC 상태머신): 행동 로직과 애니메이션 재생을 분리된 두 계층으로
  연결하는 다리 역할.
- ELEM-031 (펙트로스핑 그래픽 효과): 애니메이션 전환 시점에 파티클·화면 흔들림을
  얹으면 반응성이 배가된다.
