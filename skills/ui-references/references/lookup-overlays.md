# 오버레이 계열 컴포넌트

Dialog, Drawer/BottomSheet, Menu, Toast, Tooltip/Popover + focus·scroll 유틸.

오버레이는 **레이어 스택**(무엇이 위인가, Escape가 무엇을 닫는가), **포커스 관리**, **바깥 스크롤 차단** 셋이 얽힌다. 개별 컴포넌트보다 이 세 축의 공통 인프라를 먼저 정하는 게 낫다 — 맨 아래 유틸 비교 섹션 참고.

---

## Dialog / AlertDialog

**1순위: Base UI.** 네이티브 `<dialog>`와 커스텀 구현의 절충, `inert` 처리, 중첩 다이얼로그가 정리돼 있다. AlertDialog는 "닫기 경로가 제한된 Dialog"로 분리돼 있고 이 구분은 지킬 만하다.

갈리는 지점 — **네이티브 `<dialog>`를 쓸 것인가**: `showModal()`은 focus trap·`inert`·Escape·top layer를 공짜로 준다. 대신 애니메이션 제어와 스크롤 처리에 제약이 생긴다. 대부분의 라이브러리가 아직 커스텀 구현을 유지하는 이유다.

포인터:
- `mui/base-ui` (**branch: master**) — `packages/react/src/dialog/`, `packages/react/src/alert-dialog/`
- `radix-ui/primitives` — `packages/react/dialog/src/dialog.tsx`, `packages/react/alert-dialog/src/`
- `chakra-ui/zag` — `packages/machines/dialog/src/`

---

## Drawer / BottomSheet

**1순위: vaul** (드래그 제스처 품질 기준), **구조는 Base UI/Zag의 drawer**.

갈리는 지점 — **드래그를 지원할 것인가**: 단순히 옆에서 밀려나오는 패널이면 Dialog + transform으로 충분하다. 손가락으로 끌어 닫기, 스냅 포인트, 관성 스크롤 연동(시트 안이 스크롤될 때 언제 시트를 끄는가)이 필요하면 난이도가 완전히 달라진다. vaul은 그 어려운 쪽만 판다.

포인터:
- `emilkowalski/vaul` — `repo: emilkowalski/vaul` — `src/index.tsx` (드래그 임계값·스냅 포인트), `src/use-prevent-scroll.ts`
- `mui/base-ui` (master) — `packages/react/src/drawer/`
- `chakra-ui/zag` — `packages/machines/drawer/src/`

---

## Menu / DropdownMenu / ContextMenu

**1순위: Radix** (typeahead·중첩 서브메뉴의 참조 구현), API 설계는 Base UI.

갈리는 지점 — **Menu와 Select/Listbox를 같은 것으로 볼 것인가**: 역할이 다르다. Menu는 *행동*(누르면 실행), Listbox는 *선택*(값이 남는다). ARIA role도 다르고 키보드 모델도 다르다. `role="menu"`를 내비게이션에 쓰는 건 흔한 오용이다.

챙길 디테일: typeahead(문자 연타로 항목 점프), 서브메뉴 열림 지연과 대각선 이동 허용(safe triangle), 트리거로 포커스 복귀.

포인터:
- `radix-ui/primitives` — `packages/react/menu/src/menu.tsx` (공통 코어), `packages/react/dropdown-menu/src/`, `packages/react/context-menu/src/`, `packages/react/menubar/src/`
- `mui/base-ui` (master) — `packages/react/src/menu/`, `packages/react/src/menubar/`, `packages/react/src/context-menu/`
- `chakra-ui/zag` — `packages/machines/menu/src/`

---

## Toast / Snackbar

**1순위: sonner** (UX·모션), **구조는 Base UI toast / Zag**.

갈리는 지점 — **큐를 어떻게 다룰 것인가**: sonner는 쌓인 토스트를 카드 덱처럼 겹치고 hover 시 펼친다. Base UI/Zag는 큐 상태를 노출해 렌더링을 맡긴다. 접근성 측면에선 `role="status"`(polite) 기본, 에러만 `alert`가 정답이고, **액션이 담긴 토스트는 자동으로 사라지면 안 된다**.

포인터:
- `emilkowalski/sonner` — `repo: emilkowalski/sonner` — `src/index.tsx` (스택 레이아웃·스와이프 해제), `src/state.ts` (큐)
- `mui/base-ui` (master) — `packages/react/src/toast/`
- `chakra-ui/zag` — `packages/machines/toast/src/toast-group.machine.ts`
- `radix-ui/primitives` — `packages/react/toast/src/`

---

## Tooltip / Popover / HoverCard

**1순위: Base UI**(세 컴포넌트 분리가 명확), **위치 계산은 floating-ui가 공통 기반**.

갈리는 지점 — **트리거 방식으로 나눌 것인가**: Tooltip=hover/focus·보조 정보·포커스 안 뺏음, Popover=클릭·상호작용 가능·포커스 이동, HoverCard=hover·상호작용 가능(마우스가 카드로 건너갈 수 있어야 함). 하나로 합치면 반드시 접근성이 깨진다. 툴팁은 **터치에서 hover가 없다**는 점도 별도 처리 필요.

포인터:
- `mui/base-ui` (master) — `packages/react/src/tooltip/`, `popover/`, `preview-card/`(=HoverCard), `packages/react/src/floating-ui-react/` (벤더링된 floating-ui)
- `radix-ui/primitives` — `packages/react/tooltip/src/`, `popover/src/`, `hover-card/src/`, `packages/react/popper/src/` (공통 위치 계산)
- `floating-ui/floating-ui` (**branch: master**) — `repo: floating-ui/floating-ui` — `packages/react/src/` (인터랙션 훅), `packages/core/src/middleware/` (flip/shift/offset/size/arrow — 미들웨어는 `dom`이 아니라 `core`에 있다)

---

## 공통 유틸: focus trap · scroll lock · 레이어 스택

오버레이를 만들 때 매번 다시 마주치는 세 문제. **컴포넌트보다 먼저 정해야 한다.**

### focus trap

| 선택지 | 특징 |
| --- | --- |
| 네이티브 `<dialog showModal()>` | 공짜. top layer + `inert` + Escape 포함. 애니메이션 제약 |
| `inert` 속성 직접 사용 | 현대적 방식. 배경 전체를 한 번에 비활성화 |
| Radix `FocusScope` | `radix-ui/primitives` → `packages/react/focus-scope/src/` |
| `theKashey/react-focus-lock` (**master**) | `repo: theKashey/react-focus-lock` — 독립 라이브러리. 엣지케이스가 가장 많이 다뤄짐 |
| React Aria `FocusScope` | `adobe/react-spectrum` → `packages/react-aria/src/focus/FocusScope.tsx` |

### scroll lock

| 선택지 | 특징 |
| --- | --- |
| `theKashey/react-remove-scroll` (**master**) | `repo: theKashey/react-remove-scroll` — Radix가 쓰는 것. 스크롤바 너비 보정 포함 |
| React Aria `usePreventScroll` | `adobe/react-spectrum` → `packages/react-aria/src/overlays/usePreventScroll.ts` — **iOS Safari 처리가 가장 견고** |

둘 중 하나를 골라 프로젝트에 고정해 두는 편이 낫다. 오버레이마다 다른 방식을 쓰면 중첩됐을 때 서로 간섭한다. 포팅해서 내재화할 거라면 upstream이 iOS 대응을 계속 패치하므로 원본과 재대조할 시점을 정해둘 것.

### 레이어 스택 (무엇이 위이고 Escape가 무엇을 닫는가)

- `radix-ui/primitives` — `packages/react/dismissable-layer/src/` (원조 패턴)
- `chakra-ui/zag` — `packages/machines/dialog/src/` 내 레이어 처리 (포커스 전환에 따른 연쇄 dismiss)
- `mui/base-ui` (master) — `packages/react/src/floating-ui-react/` 의 FloatingNode/FloatingTree (중첩 팝업 트리)

세 라이브러리가 같은 문제를 다르게 푼다. 중첩 오버레이를 직접 만들 거면 셋을 나란히 보는 게 가장 빠르다.
