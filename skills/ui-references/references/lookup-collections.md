# 컬렉션 계열 컴포넌트

Carousel, Tabs, Accordion, Virtual, Table, Command, TreeView/Listbox.

공통 축은 **roving tabindex**(그룹 전체가 Tab 한 번, 내부는 화살표)와 **컬렉션 추상화**(항목을 어떻게 모델링할 것인가)다.

---

## Carousel

**1순위: embla-carousel** (제스처·물리), **접근성 구조는 Zag carousel**.

갈리는 지점 — **스크롤 기반이냐 transform 기반이냐**: 요즘은 CSS `scroll-snap` + `overflow-x`만으로 상당 부분 해결된다(네이티브 관성·접근성 무료). embla는 그 위에 관성/스냅/드래그를 직접 얹어 세밀하게 제어하는 쪽이다. 라이브러리를 넣기 전에 **scroll-snap으로 충분한지부터 확인**할 것.

접근성으로 챙길 것: 자동재생이면 일시정지 컨트롤 필수, `prefers-reduced-motion`이면 자동재생 끄기, 다음 항목이 `16–32px` 정도 보이게 해서 스크롤 가능함을 알리기.

포인터:
- `davidjerleke/embla-carousel` (**branch: master**) — `repo: davidjerleke/embla-carousel` — `packages/embla-carousel/src/components/` (`ScrollBody`, `DragHandler`, `ScrollSnaps`/`ScrollSnapList`가 핵심)
- `chakra-ui/zag` — `packages/machines/carousel/src/` (`carousel.machine.ts`, `carousel.anatomy.ts`)
- `chakra-ui/ark` — `packages/react/src/components/carousel/` (slot 분해: item-group / indicator-group / autoplay-trigger)

---

## Tabs / SegmentedControl

**1순위: Radix 또는 Base UI** (차이가 크지 않다). 참조할 건 W3C APG의 탭 패턴 자체다.

갈리는 지점 — **활성화 모드**: automatic(화살표로 포커스 이동 시 즉시 패널 전환) vs manual(Enter/Space로 확정). 패널 렌더링이 비싸면 manual. 대부분은 automatic이 자연스럽다. 그리고 **패널을 언마운트할 것인가**(상태 유지 vs 메모리).

포인터:
- `radix-ui/primitives` — `packages/react/tabs/src/tabs.tsx`, `packages/react/roving-focus/src/` (roving tabindex 공통 구현 — 여기가 재사용 가치 높음)
- `mui/base-ui` (**branch: master**) — `packages/react/src/tabs/`, `packages/react/src/toggle-group/`
- `chakra-ui/zag` — `packages/machines/tabs/src/`

---

## Accordion / Collapsible / Disclosure

**1순위: Base UI** (높이 애니메이션 처리가 정리돼 있다).

갈리는 지점 — **`height: auto` 애니메이션을 어떻게 할 것인가**. 고전적 난제이고 선택지가 갈린다:
- CSS 변수로 측정된 높이를 넘겨 `height` 전환 (Radix `--radix-collapsible-content-height`)
- `grid-template-rows: 0fr → 1fr` (최근 방식, 측정 불필요)
- `interpolate-size: allow-keywords` / `calc-size()` (신형 CSS, 지원 범위 확인 필요)

포인터:
- `mui/base-ui` (master) — `packages/react/src/accordion/`, `packages/react/src/collapsible/`
- `radix-ui/primitives` — `packages/react/accordion/src/`, `packages/react/collapsible/src/`
- `chakra-ui/zag` — `packages/machines/accordion/src/`

---

## 가상 스크롤 (Virtual)

**1순위: TanStack Virtual.** 헤드리스로 측정·오프셋만 계산해 주는 구조라 어떤 렌더링에도 붙는다.

갈리는 지점 — **항목 높이를 아는가**: 고정 높이면 계산이 단순하다. 가변 높이(동적 측정)면 `measureElement`와 스크롤 앵커링이 필요하고, 여기서 스크롤 점프가 생기기 쉽다. 그리고 **가상화가 정말 필요한가** — 수백 개 정도면 그냥 렌더링하는 게 낫고, `content-visibility: auto`가 대안이 되기도 한다.

접근성 주의: 가상화된 목록은 DOM에 일부만 있어서 스크린리더의 항목 수 인식이 깨진다. `aria-setsize`/`aria-posinset`을 직접 넣어야 한다.

포인터:
- `TanStack/virtual` — `repo: TanStack/virtual` — `packages/virtual-core/src/index.ts` (프레임워크 무관 코어), `packages/react-virtual/src/`

---

## Table / DataGrid

**1순위: TanStack Table** (정렬·필터·그룹핑·페이지네이션 모델), **키보드 그리드 내비게이션은 React Aria**.

갈리는 지점 — **`<table>`이냐 grid role이냐**: 정적 데이터 표시면 시맨틱 `<table>`로 충분하다. 셀 단위 포커스 이동·편집·선택이 필요하면 `role="grid"`와 2차원 roving tabindex가 필요하고 난이도가 급상승한다.

포인터:
- `TanStack/table` (**branch: beta** — main 아님 주의) — `repo: TanStack/table` — `packages/table-core/src/features/` (정렬·필터 등 기능별 분리 구조가 참고할 만함)
- `adobe/react-spectrum` — `packages/react-aria/src/grid/`, `packages/react-aria/src/table/` (그리드 키보드 모델)

---

## Command / CommandPalette

**1순위: cmdk.** 필터링·점수 매칭·그룹 처리가 한 덩어리로 정리돼 있고, 사실상 이 UI의 표준이 됐다(shadcn Command도 이걸 쓴다).

갈리는 지점 — **필터링을 누가 하는가**: cmdk는 기본적으로 자체 점수 기반 필터를 내장하되 `shouldFilter={false}`로 서버 필터링에 넘길 수 있다. 비동기 검색이면 반드시 후자.

주의: 업데이트 주기가 느린 편이다. 새로 의존성으로 넣을 거면 현재 활성도를 확인하고 쓸 것.

포인터:
- `pacocoursey/cmdk` — `repo: pacocoursey/cmdk` — `cmdk/src/index.tsx` (`score` 함수와 항목 등록 방식이 핵심)
- `facebook/astryx` — `packages/core/src/CommandPalette/` (완성형 구현 비교용)

---

## TreeView / Listbox

**1순위: Zag** (`tree-view`, `listbox`). 트리는 확장 상태·다중 선택·타입어헤드가 얽혀서 직접 만들면 키보드 모델을 반드시 빠뜨린다.

챙길 것: 화살표 좌우로 접기/펼치기, 부모-자식 선택 전파(3-state 체크박스), 가상화와의 결합.

포인터:
- `chakra-ui/zag` — `packages/machines/tree-view/src/`, `packages/machines/listbox/src/`
- `adobe/react-spectrum` — `packages/react-aria/src/tree/`, `packages/react-stately/src/tree/`
- `radix-ui/primitives` — `packages/react/collection/src/` (컬렉션 추상화 자체가 볼 만함)

---

## 참고: 패널 분할 (Resizable)

목록엔 안 넣었지만 자주 같이 필요하다.
- `bvaughn/react-resizable-panels` — `repo: bvaughn/react-resizable-panels` — 키보드 리사이즈·레이아웃 영속화 포함
- `chakra-ui/zag` — `packages/machines/splitter/src/`
