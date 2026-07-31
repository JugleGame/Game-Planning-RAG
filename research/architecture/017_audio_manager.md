+++
card_id = "ARCH-017"
type = "structure"
title = "오디오 매니저 (AudioSource 풀 + BGM/SFX 분리)"
summary = "소리를 재생할 때마다 AudioSource를 새로 만들지 않고, BGM 전용과 SFX 풀을 미리 나눠 관리해서 겹쳐 재생되는 효과음도 끊기지 않게 하는 구조"
tags = ["audio", "sfx", "bgm", "pooling", "singleton", "unity"]
updated = "2026-07-31"
confidence = "medium"
+++
## 문제
효과음은 짧은 시간 안에 여러 번 겹쳐 재생돼야 한다(연타 공격음 등). 오브젝트 하나에
`AudioSource` 하나만 두고 매번 `Play()`를 다시 호출하면 앞 소리가 잘리고, 반대로
소리마다 새 `AudioSource`를 만들고 파괴하면 ARCH-015가 다루는 것과 같은 생성·파괴
비용 문제가 그대로 생긴다. 배경음악(BGM)과 효과음(SFX)은 재생 방식 자체가 다르다
(BGM은 한 번에 하나, 루프, 페이드 / SFX는 다수 동시, 1회성)
[출처: GitHub perezromeojohn/unity-audiomanager, 오브젝트 풀링 기반 오디오 매니저,
https://github.com/perezromeojohn/unity-audiomanager].

## 구조
- 이 프로젝트의 `Core/`에 두는 전역 매니저 하나가 오디오 재생의 유일한 진입점이다
  — 개별 스크립트가 자기 `AudioSource`를 직접 `Play()`하지 않는다.
- BGM용 `AudioSource` 1~2개(크로스페이드가 필요하면 2개)와, SFX용 `AudioSource`
  풀(ARCH-015 오브젝트 풀링 구조 재사용)을 분리해서 든다 — 하나는 "항상 하나만
  재생", 다른 하나는 "여러 개 동시 재생 가능"이라는 서로 다른 요구를 만족해야
  하기 때문이다 [출처: Medium, Gaetano Tonzuso, Unity: How to make an
  AudioManager, https://medium.com/@gaetano.tonzuso/unity-how-to-make-an-audiomanager-07d059f4e894].
- 볼륨·음소거 같은 전역 설정은 `AudioMixer`의 노출된 파라미터로 두어, BGM/SFX를
  각각 따로 조절할 수 있게 한다.

## 핵심 규칙
- 재생 요청은 반드시 매니저를 거친다 — `AudioManager.PlaySfx(clipId)`처럼 클립을
  이름/ID로 요청하고, 어떤 `AudioSource`가 실제로 재생하는지는 매니저 내부
  구현으로 숨긴다.
- BGM은 씬이 바뀌어도 끊기지 않아야 하는 경우가 많으므로 ARCH-011 Boot
  부트스트랩 규칙에 따라 `DontDestroyOnLoad` 대상 매니저로 둔다.
- SFX 풀의 `AudioSource`는 재생이 끝나면(clip 길이만큼 지난 뒤) 자동으로 풀에
  반납되어야 한다 — 수동으로 매번 반납을 잊지 않도록 코루틴이나 타이머로
  자동화한다.

## Unity 구현 절차
1. `Core/AudioManager`를 만들고 ARCH-011의 부트스트랩 규칙에 따라 Boot 씬에서
   생성 후 `DontDestroyOnLoad`로 유지한다.
2. BGM 재생용 `AudioSource`(loop=true)와 SFX용 `AudioSource` 풀(ARCH-015의
   ObjectPool 구조)을 매니저 아래에 둔다.
3. 클립은 코드에 직접 참조로 박지 않고 ARCH-012의 ScriptableObject 데이터 규약을
   따라 "사운드 ID → AudioClip" 테이블로 둔다 — 사운드 교체가 코드 수정 없이
   가능해진다.
4. `PlaySfx(id)`, `PlayBgm(id)`, `StopBgm()` 등 소수의 공개 메서드만 외부에
   노출한다. 소비자는 이벤트 버스(ARCH-001)를 구독해 "이 사건엔 이 사운드"를
   재생하도록 연결한다.
5. 재생이 끝난 SFX `AudioSource`가 풀로 반납되는지, BGM 전환 시 이전 클립이
   정지되는지 확인한다.

## 안티패턴
- 소리를 낼 필요가 있는 스크립트마다 각자 `AudioSource`를 붙이고 직접 재생 —
  전역 볼륨 조절, 음소거, 동시 재생 제한이 불가능해진다.
- SFX용 `AudioSource`를 매번 `AddComponent`/`Destroy`로 새로 만드는 것 — 짧고
  잦은 효과음일수록 이 비용이 누적된다.
- BGM 재생용 `AudioSource`를 SFX 풀과 같은 풀에서 꺼내 쓰는 것 — 풀로 반납되는
  순간 배경음악이 끊기는 사고로 이어진다.

## 검증 방법
- 같은 효과음을 짧은 간격으로 연속 재생시켰을 때 소리가 겹쳐 들리고 잘리지
  않는지 확인 — SFX 동시 재생이 이 구조의 핵심 합격 기준이다.
- 씬 전환 시 BGM이 끊기지 않는지(또는 스펙에 정의된 대로 페이드 전환되는지)
  관찰.
- 콘솔 에러 0개, 특히 풀이 비어 새 `AudioSource`를 계속 생성하는 경고(풀 크기
  부족 신호) 0건.

## 조합 궁합
- ARCH-015 (오브젝트 풀링): SFX용 `AudioSource` 풀의 기반 구조. 별도로 새로
  설계하지 않고 그대로 재사용한다.
- ARCH-001 (이벤트 버스): 전투·획득·대화 같은 게임 사건에 사운드를 매다는
  연결점. 재생 로직과 게임 로직을 직접 참조 없이 묶는다.
