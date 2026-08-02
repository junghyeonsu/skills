# Headless primitives

스타일 없이 동작·접근성만 제공하는 React 라이브러리들. **훅 API와 컴파운드 구조를 설계할 때** 보는 축이다.

각 엔트리의 `repo:` 라인은 업데이트 다이제스트가 grep으로 수집한다 — 형식을 바꾸지 말 것.

---

## Base UI — 1순위

MUI/Radix/Floating UI 핵심 기여자들이 다시 만든 헤드리스 라이브러리. 현재 이 분야에서 가장 정돈된 API를 가지고 있고 활발하다 (v1.6.0, 2026-06).

**볼 때**: 새 컴포넌트의 훅/컴파운드 API를 설계할 때, 렌더 위임(`render` prop) 패턴을 정할 때, Field/Form 연결 구조를 볼 때.
**안 볼 때**: 프레임워크 무관 로직이 필요할 때(→ Zag), 스타일까지 필요할 때.

```
repo: mui/base-ui
branch: master          ← main 아님, 주의
components: packages/react/src/<kebab-name>/
tests: 컴포넌트 디렉토리 안 *.test.tsx 공존
docs: docs/src/app/(public)/(content)/react/
updates: https://github.com/mui/base-ui/releases
```

fetch 예시:
`https://raw.githubusercontent.com/mui/base-ui/master/packages/react/src/select/root/SelectRoot.tsx`

훔칠 포인트:
- `packages/react/src/use-render/` — `asChild`(Radix Slot)의 대안. 자식 복제 대신 렌더 함수를 넘겨 타입 안정성을 확보한 접근
- `packages/react/src/merge-props/` — prop 병합 규칙(이벤트 핸들러 체이닝, className/style 처리)의 단독 구현
- `packages/react/src/field/` — 라벨·설명·에러와 컨트롤 자동 연결
- `packages/react/src/floating-ui-react/` — floating-ui를 벤더링해서 관리하는 방식 자체

수록 컴포넌트(2026-08 기준): accordion, alert-dialog, autocomplete, avatar, checkbox(-group), collapsible, combobox, context-menu, dialog, drawer, field, fieldset, form, input, menu, menubar, meter, navigation-menu, number-field, otp-field, popover, preview-card, progress, radio(-group), scroll-area, select, separator, slider, switch, tabs, toast, toggle(-group), toolbar, tooltip

---

## Radix Primitives

이 분야의 패턴 원조. `asChild`, 컴파운드 컴포넌트, `dismissable-layer` 등 지금 표준이 된 개념 다수가 여기서 나왔다.

**유지 상태 (2026-08 실측)**: 커밋은 계속 올라온다(최근 푸시 7/31, `one-time-password-field`·`password-toggle-field` 같은 신규 primitive도 있음). 다만 **GitHub Releases를 쓰지 않아** 릴리스 목록이 비어 있고, 새 기능 속도는 Base UI보다 느리다. "죽었다"고 단정할 상태는 아니지만 신규 채택 1순위로 삼기엔 애매하다.

**볼 때**: 특정 패턴의 원본 구현이 궁금할 때, 이미 Radix에 의존 중인 코드를 고칠 때, roving-focus/collection 같은 재사용 유틸을 볼 때.
**안 볼 때**: 새 프로젝트의 기본 선택지로 (→ Base UI).

```
repo: radix-ui/primitives
branch: main
components: packages/react/<component>/src/
core: packages/core/
updates: (Releases 미사용 — 커밋으로 확인)
```

fetch 예시:
`https://raw.githubusercontent.com/radix-ui/primitives/main/packages/react/slot/src/slot.tsx`

훔칠 포인트:
- `packages/react/slot/src/` + `packages/react/compose-refs/src/` — `asChild`의 표준 구현
- `packages/react/roving-focus/src/` — roving tabindex를 컴포넌트로 추출한 것. 재사용 가치 높음
- `packages/react/dismissable-layer/src/` — 레이어 스택·바깥 클릭·Escape 처리의 원조
- `packages/react/collection/src/` — 자식 항목을 순서대로 수집하는 추상화

---

## React Aria Components (RAC)

Adobe React Spectrum 생태계의 컴포넌트 레이어. 접근성·국제화 정확도는 이 분야 최고 기준이다.

**볼 때**: ARIA 스펙 해석이 애매할 때, 로케일·RTL·날짜/숫자 포맷이 얽힐 때, 데스크톱급 위젯(table grid, tree)이 필요할 때.
**안 볼 때**: 가벼운 API를 원할 때 (추상화 층이 두껍고 학습 비용이 있다).

```
repo: adobe/react-spectrum
branch: main
components: packages/react-aria-components/src/<Component>.tsx
hooks: packages/react-aria/src/<domain>/
state: packages/react-stately/src/<domain>/
i18n: packages/@internationalized/{date,number,string}/src/
updates: https://github.com/adobe/react-spectrum/releases
```

자세한 훅 단위 내용은 [behavior-hooks.md](behavior-hooks.md)에 있다.

---

## Ark UI

Zag 상태머신 위에 React/Vue/Solid/Svelte 바인딩을 올린 컴포넌트 레이어. Park UI와 Chakra v3의 기반이기도 하다.

**볼 때**: 같은 로직을 여러 프레임워크로 내보내는 구조가 궁금할 때, Zag 머신을 컴포넌트로 감싸는 방식을 볼 때.
**안 볼 때**: React만 쓸 거고 추상화 층을 줄이고 싶을 때 (→ 그냥 Zag나 Base UI).

```
repo: chakra-ui/ark
branch: main
components: packages/react/src/components/<component>/
frameworks: packages/{react,vue,solid,svelte}/
updates: https://github.com/chakra-ui/ark/releases
```

훔칠 포인트: `packages/react/src/components/<c>/` 안의 `*.tsx`와 `use-*.ts` 분리 방식 — 머신 연결과 렌더링을 나누는 경계.

---

## Headless UI

Tailwind Labs 제작. API가 가장 단순하다.

**유지 상태**: 최근 푸시 2026-04로 정체 중. 커버리지도 좁다(Dialog, Menu, Listbox, Combobox, Tabs, Switch, Disclosure, Popover 정도).
**볼 때**: 최소한의 API 표면이 어떤 모습인지 참고할 때.
**안 볼 때**: 커버리지나 최신성이 필요할 때.

```
repo: tailwindlabs/headlessui
branch: main
components: packages/@headlessui-react/src/components/<component>/
updates: https://github.com/tailwindlabs/headlessui/releases
```

---

## Ariakit

접근성 중심의 오래된 라이브러리. 활발하다(2026-08 푸시).

**볼 때**: 컴포지션을 극단까지 밀어붙인 API가 궁금할 때, 특정 ARIA 패턴의 또 다른 해석이 필요할 때(교차 검증용 3번째 소스로 유용).
**안 볼 때**: 첫 참고처로 (문서/멘탈모델이 독특해서 진입 비용이 있다).

```
repo: ariakit/ariakit
branch: main
components: packages/ariakit-react-core/src/<component>/
updates: https://github.com/ariakit/ariakit/releases
```

---

## SEED react-headless

당근 디자인시스템의 헤드리스 레이어. 위 라이브러리들에서 필요한 부분만 포팅·확장한 구조라, **"외부 구현을 어떻게 내재화하는가"의 사례**로 볼 만하다.

**볼 때**: 이미 SEED 작업 중일 때, 포팅 시 귀속·diff 관리 방식을 볼 때.
**안 볼 때**: 범용 라이브러리 API 설계 참고 (SEED 제품 요구에 맞춰 좁혀진 부분이 있다).

```
repo: daangn/seed-design
branch: dev             ← main 아님, 주의
components: packages/react-headless/<component>/src/
infra: packages/react-headless/{dismissible-layer,floating,portal,presence,prevent-scroll,primitive,use-controllable-state}/
styled: packages/react/src/components/<Component>/
updates: https://github.com/daangn/seed-design/releases
```

특징적인 것 — **포팅 귀속 컨벤션**: 외부에서 가져온 파일은 1행에 출처를 적는다.
```
// This code includes portions derived from radix-ui/primitives (https://github.com/radix-ui/primitives)
```
현재 계보: Radix ← `presence`, `slider`, `use-controllable-state`, `dismissible-layer` / React Aria ← `prevent-scroll` / Zag ← `progress`, `file-upload`. `README.md`의 "Prior Arts" 절에 Radix·React Aria·Zag·Ark·Ariakit이 명시돼 있다.

`packages/react-headless/dismissible-layer/src/layer-stack.ts`는 Radix·Zag·Base UI 세 방식을 한 파일에서 참조·비교하고 있어서, 세 라이브러리의 접근 차이를 보기에 좋은 단일 지점이다.
