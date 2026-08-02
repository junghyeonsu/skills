# 상태머신 코어

UI 로직을 프레임워크와 분리해 상태머신으로 기술하는 접근. **React가 아닌 런타임으로 로직을 옮겨야 할 때** 1순위 참고처다.

---

## Zag — 1순위

Chakra 팀이 만든 framework-agnostic UI 상태머신 모음. 각 컴포넌트의 로직이 순수 머신으로 있고, React/Vue/Solid/Svelte 어댑터가 그 위에 얇게 붙는다. Ark UI와 Chakra v3가 이걸 기반으로 만들어졌다.

**볼 때**:
- 컴포넌트 로직을 **React 밖으로 옮겨야 할 때** — 런타임이 다른 환경으로 포팅하는 경우 1순위
- 상태 전이를 명시적으로 정리하고 싶을 때 (어떤 이벤트가 어떤 상태에서 무엇을 하는가)
- 커버리지가 필요할 때 — 이 분야에서 다루는 컴포넌트 범위가 가장 넓다

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

머신이 파트를 식별하는 데 `data-scope`/`data-part` 속성을 쓴다. 스타일을 이 속성에 걸면 그 규약에 묶이므로, **속성 셀렉터를 제한적으로만 지원하는 환경**에 옮길 거라면 파트 식별을 클래스 등으로 바꿔 받을 계층이 따로 필요하다.

### 머신 하나를 읽는 순서

1. `*.types.ts` — 공개 API와 컨텍스트가 무엇인지
2. `*.machine.ts` — 상태 목록과 전이. **여기서 "어떤 상황이 존재하는가"의 전체 목록을 얻는다.** 직접 구현할 때 빠뜨리는 엣지케이스가 대부분 여기 적혀 있다
3. `*.connect.ts` — 각 파트에 실제로 붙는 ARIA 속성·이벤트 핸들러. 접근성 구현의 알맹이

### 수록 머신

최신 목록은 `gh api repos/chakra-ui/zag/contents/packages/machines --jq '.[].name'`로 확인한다. 아래는 하한선으로 쓸 것 — 늘어나기만 하고 잘 줄지 않는다.

accordion, angle-slider, async-list, avatar, carousel, cascade-select, checkbox, clipboard, collapsible, color-picker, combobox, date-input, date-picker, dialog, drawer, editable, file-upload, floating-panel, hover-card, image-cropper, listbox, marquee, menu, navigation-menu, number-input, pagination, password-input, pin-input, popover, presence, progress, qr-code, radio-group, rating-group, scroll-area, select, signature-pad, slider, splitter, steps, switch, tabs, tags-input, timer, toast, toc, toggle, toggle-group, tooltip, tour, tree-view

이 목록은 **"어떤 컴포넌트가 만들 만한가"의 체크리스트로도 쓸 수 있다.** color-picker, signature-pad, qr-code, tour처럼 흔치 않은 것까지 있다.

훔칠 포인트:
- `packages/machines/combobox/src/combobox.machine.ts` — 가장 복잡한 머신. 입력·필터·선택·포커스가 얽힌 상태를 어떻게 쪼갰는지
- `packages/machines/file-upload/src/file-upload.connect.ts` — 파일 거부 사유를 코드로 분류해 넘기는 방식
- `packages/utilities/dom-query/src/` — 프레임워크 없이 DOM을 다루는 유틸 모음
- `packages/core/src/` — 머신 런타임 자체. 상태머신을 직접 만든다면 여기 스케일 참고

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
