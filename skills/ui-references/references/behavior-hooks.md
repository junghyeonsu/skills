# 저수준 훅 · 유틸

컴포넌트가 아니라 **동작 조각**을 제공하는 것들. 위치 계산, 포커스, 스크롤, 제스처, i18n.

---

## React Aria / React Stately — 접근성·국제화 정본

Adobe. `@react-aria/*`는 동작+ARIA를, `@react-stately/*`는 상태를 담당하도록 분리돼 있다. 이 **동작/상태 분리 자체**가 참고할 만한 설계다.

**볼 때**: ARIA 스펙 해석이 애매할 때, 로케일·RTL·날짜/숫자가 얽힐 때, 포인터/키보드/터치 이벤트의 크로스 브라우저 정규화가 필요할 때.
**안 볼 때**: 간단한 것을 간단하게 하고 싶을 때 (추상화가 두껍다).

```
repo: adobe/react-spectrum
branch: main
hooks: packages/react-aria/src/<domain>/
state: packages/react-stately/src/<domain>/
i18n: packages/@internationalized/{date,number,string}/src/
updates: https://github.com/adobe/react-spectrum/releases
```

fetch 예시:
`https://raw.githubusercontent.com/adobe/react-spectrum/main/packages/react-aria/src/interactions/usePress.ts`

훔칠 포인트:
- `packages/react-aria/src/interactions/usePress.ts` — **이 레포에서 가장 값어치 있는 파일 중 하나.** 마우스/터치/펜/키보드를 하나의 press 개념으로 정규화하고, 터치 후 유령 클릭·드래그 취소·롱프레스를 다 다룬다. 직접 만들면 반드시 빠뜨리는 것들
- `packages/react-aria/src/interactions/useFocusVisible.ts` — `:focus-visible` 판정을 JS로 재현
- `packages/react-aria/src/overlays/usePreventScroll.ts` — iOS Safari 스크롤 잠금. SEED가 포팅한 원본
- `packages/react-aria/src/focus/FocusScope.tsx` — focus trap + 복원
- `packages/@internationalized/date/src/` — 캘린더/타임존 계산. 날짜를 다룬다면 사실상 필수
- `packages/react-aria/src/i18n/` — 로케일·방향(RTL) 컨텍스트

---

## floating-ui — 위치 계산 표준

툴팁·팝오버·드롭다운의 위치 계산. 이 분야에 실질적 경쟁자가 없다. Radix·Base UI·SEED 모두 이걸 쓴다.

**볼 때**: 뷰포트 경계 처리(flip/shift), 화살표 위치, 가상 요소(커서 위치에 띄우기), 자동 업데이트가 필요할 때.
**안 볼 때**: CSS Anchor Positioning으로 충분한 경우 — 지원 범위를 먼저 확인할 것 (네이티브가 되면 이 의존성이 사라질 수 있다).

```
repo: floating-ui/floating-ui
branch: master          ← main 아님, 주의
core: packages/core/src/
middleware: packages/core/src/middleware/     ← dom이 아니라 core
dom: packages/dom/src/
react: packages/react/src/
updates: https://github.com/floating-ui/floating-ui/releases
```

훔칠 포인트:
- `packages/core/src/middleware/` — flip/shift/offset/size/arrow/autoPlacement/hide/inline 각각이 독립 파일. **미들웨어 파이프라인 구조 자체**가 참고할 만한 설계
- `packages/react/src/hooks/` — `useInteractions`로 hover/click/focus/dismiss를 조합하는 방식. 인터랙션을 훅 단위로 쪼개 합성하는 패턴

---

## 스크롤 · 포커스 유틸

| 라이브러리 | 용도 | 비고 |
| --- | --- | --- |
| `theKashey/react-remove-scroll` (**master**) | 배경 스크롤 잠금 | Radix가 쓰는 것. 스크롤바 너비 보정 포함 |
| `theKashey/react-focus-lock` (**master**) | focus trap | 독립 라이브러리 중 엣지케이스가 가장 많이 다뤄짐 |
| React Aria `usePreventScroll` | 배경 스크롤 잠금 | iOS Safari 처리가 가장 견고. SEED 채택 |
| Radix `FocusScope` | focus trap | 라이브러리에 내장된 형태 |

```
repo: theKashey/react-remove-scroll
repo: theKashey/react-focus-lock
```

셋 다 같은 문제를 푸는데 해법이 다르다. **오버레이를 만들기 전에 이 둘(스크롤·포커스)을 무엇으로 할지부터 정하면** 이후 컴포넌트마다 반복 결정이 없어진다. 자세한 비교는 [lookup-overlays.md](lookup-overlays.md) 하단.

---

## 제스처 · 애니메이션 저수준

| 라이브러리 | 용도 |
| --- | --- |
| `pmndrs/use-gesture` | 드래그/핀치/휠 제스처 정규화. vaul 같은 시트 구현의 기반 |
| `motiondivision/motion` (구 framer-motion) | 스프링·레이아웃 애니메이션. `AnimatePresence`의 enter/exit 처리 |

```
repo: pmndrs/use-gesture
repo: motiondivision/motion
```

모션 **판단 기준**(무엇을 애니메이션할지, 값을 얼마로 할지)은 이 파일이 아니라 설치된 모션 스킬 쪽이 정본이다 — [skill-collections.md](skill-collections.md) 참고.

---

## 가상화

```
repo: TanStack/virtual
branch: main
core: packages/virtual-core/src/index.ts
```

프레임워크 무관 코어 + 얇은 어댑터 구조. Zag와 같은 철학이고, **"코어를 프레임워크에서 떼어내는 방법"의 작고 읽기 쉬운 예제**로도 좋다.

---

## 그 밖에 자주 필요한 것

| 문제 | 참고 |
| --- | --- |
| 제어/비제어 상태 통합 | Radix `packages/react/use-controllable-state/`, SEED `packages/react-headless/use-controllable-state/` |
| ref 합성 | Radix `packages/react/compose-refs/src/` |
| prop 병합 | Base UI `packages/react/src/merge-props/`, SEED `packages/utils/dom-utils/src/mergeProps.ts` (react-aria + zag 참고 명시) |
| 요소 크기 관찰 | Radix `packages/react/use-size/`, SEED `react-headless/slider/src/useElementSizesMap.ts` (다중 요소 확장) |
| Portal | Radix `packages/react/portal/src/`, SEED `react-headless/portal/` |
| enter/exit 언마운트 지연 | Radix `packages/react/presence/src/`, SEED `react-headless/presence/` (Radix 포팅) |
