# 상태머신 코어

UI 로직을 프레임워크와 분리해 상태머신으로 기술하는 접근. **React가 아닌 런타임으로 로직을 옮겨야 할 때** 1순위 참고처다.

---

## Zag — 1순위

Chakra 팀이 만든 framework-agnostic UI 상태머신 모음. 각 컴포넌트의 로직이 순수 머신으로 있고, React/Vue/Solid/Svelte 어댑터가 그 위에 얇게 붙는다. Ark UI와 Chakra v3가 이걸 기반으로 만들어졌다.

**볼 때**:
- 컴포넌트 로직을 **React 밖으로 옮겨야 할 때** — Lynx 포팅처럼 런타임이 다른 경우 1순위
- 상태 전이를 명시적으로 정리하고 싶을 때 (어떤 이벤트가 어떤 상태에서 무엇을 하는가)
- 커버리지가 필요할 때 — 51개 머신으로 이 분야에서 가장 넓다

**안 볼 때**: React 전용이고 관용적인 훅 API를 원할 때(→ Base UI). 머신 추상화는 읽는 비용이 있다.

```
repo: chakra-ui/zag
branch: main
machines: packages/machines/<component>/src/
  <component>.machine.ts   상태·전이 정의
  <component>.connect.ts   상태 → DOM prop 변환 (여기가 실제 접근성 구현)
  <component>.types.ts     공개 API 타입
  <component>.anatomy.ts   파트 정의
core: packages/core/src/
utilities: packages/utilities/<domain>/src/
updates: https://github.com/chakra-ui/zag/releases
```

fetch 예시:
`https://raw.githubusercontent.com/chakra-ui/zag/main/packages/machines/combobox/src/combobox.connect.ts`

> **v2 프리릴리스 진행 중 (2026-08, `2.0.0-next.*`).** 가장 큰 변경은 `data-scope`/`data-part`/`data-ownedby` 3종을 **단일 `data-{scope}-{part}="{uid}"` 로 병합**하는 것이다. 셀렉터가 `[data-dialog-trigger]`처럼 단순해지고 한 엘리먼트가 여러 머신에 참여할 수 있게 되지만, **Lynx는 `[data-*]` 속성 셀렉터를 지원하지 않으므로** Lynx 포팅 관점에서는 이 변경이 그대로 도움이 되지 않는다(postcss 변환 계층에서 어떻게 받을지 별도 판단 필요). 그 밖에 Select/Combobox/Listbox에 `list` 파트가 신설되어 `role="listbox"`가 content→list로 이동하는 마크업 breaking이 있다.

### 머신 하나를 읽는 순서

1. `*.types.ts` — 공개 API와 컨텍스트가 무엇인지
2. `*.machine.ts` — 상태 목록과 전이. **여기서 "어떤 상황이 존재하는가"의 전체 목록을 얻는다.** 직접 구현할 때 빠뜨리는 엣지케이스가 대부분 여기 적혀 있다
3. `*.connect.ts` — 각 파트에 실제로 붙는 ARIA 속성·이벤트 핸들러. 접근성 구현의 알맹이

### 수록 머신 (2026-08, 51개)

accordion, angle-slider, async-list, avatar, carousel, cascade-select, checkbox, clipboard, collapsible, color-picker, combobox, date-input, date-picker, dialog, drawer, editable, file-upload, floating-panel, hover-card, image-cropper, listbox, marquee, menu, navigation-menu, number-input, pagination, password-input, pin-input, popover, presence, progress, qr-code, radio-group, rating-group, scroll-area, select, signature-pad, slider, splitter, steps, switch, tabs, tags-input, timer, toast, toc, toggle, toggle-group, tooltip, tour, tree-view

이 목록은 **"어떤 컴포넌트가 만들 만한가"의 체크리스트로도 쓸 수 있다.** color-picker, signature-pad, qr-code, tour처럼 흔치 않은 것까지 있다.

훔칠 포인트:
- `packages/machines/combobox/src/combobox.machine.ts` — 가장 복잡한 머신. 입력·필터·선택·포커스가 얽힌 상태를 어떻게 쪼갰는지
- `packages/machines/file-upload/src/file-upload.connect.ts` — SEED가 참조한 구현. 거부 사유 분류 방식
- `packages/utilities/dom-query/src/` — 프레임워크 없이 DOM을 다루는 유틸 모음
- `packages/core/src/` — 머신 런타임 자체. 상태머신을 직접 만든다면 여기 스케일 참고

---

## Lynx 포팅 관점

SEED에서 Lynx(React가 아닌 런타임)로 컴포넌트를 옮길 때 Zag가 특히 유용한 이유:

- 로직이 DOM/React에 묶여 있지 않아서, **무엇이 순수 로직이고 무엇이 플랫폼 의존인지 경계가 이미 그어져 있다**
- `connect.ts`가 "이 상태에서 어떤 속성이 나가야 하는가"를 데이터로 표현하므로, 그 출력을 Lynx 엘리먼트 속성으로 바꾸는 매핑 문제로 축소된다
- 단, Zag의 `dom-query` 유틸은 실제 DOM API를 쓰므로 그대로는 못 옮긴다. 머신은 참고하되 DOM 계층은 분리해서 볼 것

관련: SEED에 `lynx-react-headless` 패키지는 아직 없다(2026-08 기준). `packages/lynx-react/src/components/`에 13개 컴포넌트가 있고 로직이 컴포넌트에 붙어 있는 상태다.

---

## 대안: XState

범용 상태머신 라이브러리. Zag가 내부적으로 참고한 계보이기도 하다.

**볼 때**: UI가 아닌 도메인 로직(결제 플로우, 온보딩 단계 등)을 머신으로 짤 때, statechart 개념(병렬 상태, 계층 상태)이 필요할 때.
**안 볼 때**: 컴포넌트 하나의 로직 — 그건 Zag가 이미 만들어 뒀다.

```
repo: statelyai/xstate
branch: main
core: packages/core/src/
updates: https://github.com/statelyai/xstate/releases
```
