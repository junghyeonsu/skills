# 대형 · 멀티플랫폼 시스템

기업 규모로 운영되는 디자인시스템들. 개별 컴포넌트보다 **시스템을 어떻게 운영·확장·배포하는가**를 볼 때 참고한다.

---

## Astryx (Meta) — 주목

2026-01 공개. Meta 내부에서 8년간 자란 시스템을 오픈소스로 낸 것으로, 13,000+ 앱에 쓰였다고 밝히고 있다. React + StyleX 기반, 현재 Beta, MIT.

**볼 때**: **"에이전트가 쓰는 디자인시스템"을 어떻게 설계하는가** — 이 시스템의 명시적 목표다. 그리고 eject(swizzle) 모델, 테마를 CSS 변수 오버라이드로만 정의하는 방식.
**안 볼 때**: 안정성이 필요한 프로덕션 의존성으로 (Beta).

```
repo: facebook/astryx
branch: main
components: packages/core/src/<PascalCase>/      (121개 디렉토리)
themes: packages/themes/
cli: packages/cli/
experimental: packages/lab/
charts: packages/charts/, packages/vega/
richtext: packages/richtext/
docsite: apps/docsite/src/
examples: apps/example-nextjs-{tailwind,stylex,source}/, apps/example-vite*/
updates: https://github.com/facebook/astryx/releases
site: https://astryx.atmeta.com
```

fetch 예시:
`https://raw.githubusercontent.com/facebook/astryx/main/packages/core/src/Dialog/Dialog.tsx`

훔칠 포인트 (SEED 관점에서 특히):
- **스타일 구현을 소비자에게 숨기는 경계** — StyleX로 작성했지만 사용자는 미리 빌드된 CSS를 import하고 `className`으로 덮어쓴다. 빌드 플러그인·PostCSS 설정이 필요 없다. "우리는 X로 만들지만 너희는 X를 몰라도 된다"는 선긋기. qvism/Panda 노출 범위를 정할 때 비교 대상
- **swizzle (eject)** — `packages/cli/`. 컴포넌트 전체 소스를 프로젝트로 꺼내 소유하게 하는 명령. shadcn의 복사 모델과 라이브러리 모델의 절충안이며, SEED snippet registry와 직접 비교된다
- **agent-ready 표방** — 레포 루트에 `CLAUDE.md`와 `.claude/`가 있고 CLI가 "agent-ready docs"를 낸다. 문서·API·CLI를 사람과 에이전트가 같은 방식으로 쓰도록 설계했다고 주장한다. SEED의 llms.txt 체계와 비교해 볼 것
- **테마 = CSS custom property 오버라이드만** — 포크나 래핑 없이 디자이너가 테마를 바꿀 수 있게 한 제약. rootage 다중 테마와 비교
- `packages/lab/` — 실험 컴포넌트를 `@canary` dist-tag로만 배포하는 분리 (SEED의 archive/실험 정책과 비교)

---

## React Spectrum (Adobe)

이 목록에서 가장 층이 잘 나뉜 시스템. **3층 구조**가 핵심이다:

| 층 | 패키지 | 역할 |
| --- | --- | --- |
| 상태 | `@react-stately/*` | 프레임워크 무관 상태 로직 |
| 동작 | `@react-aria/*` | ARIA·키보드·포인터 (스타일 없음) |
| 컴포넌트 | `react-aria-components` | 스타일 없는 완성 컴포넌트 |
| 제품 | `@react-spectrum/*` | Adobe 브랜드 스타일 적용 |

**볼 때**: 레이어를 어디서 끊을지 설계할 때, 접근성·i18n 정확도, 데스크톱급 위젯(table, tree, dnd).
**안 볼 때**: 가벼움이 필요할 때.

```
repo: adobe/react-spectrum
branch: main
state: packages/react-stately/src/<domain>/
behavior: packages/react-aria/src/<domain>/
components: packages/react-aria-components/src/
product: packages/@react-spectrum/<component>/src/     ← re-export 셸 (아래 주의)
i18n: packages/@internationalized/{date,number,string}/src/
updates: https://github.com/adobe/react-spectrum/releases
site: https://spectrum.adobe.com
```

> **레이아웃이 바뀌었다 (2026-08 실측).** 예전 경로 `packages/@react-aria/<domain>/src/`와 `packages/@react-stately/<domain>/src/`에는 이제 `index.ts` 하나만 있고, 실제 구현은 `packages/react-aria/src/<domain>/`, `packages/react-stately/src/<domain>/`로 옮겨졌다. `@react-spectrum/*`도 마찬가지로 셸이며 `@adobe/react-spectrum`을 다시 내보낸다. 오래된 문서·블로그의 `packages/@react-aria/...` 경로는 그대로 안 먹는다. `@internationalized/*`는 예전 위치 그대로다.

훔칠 포인트: **각 층의 경계 규칙 자체.** 상태는 DOM을 모르고, 동작은 스타일을 모르고, 제품 층만 브랜드를 안다. SEED의 headless/qvism/react 3층과 대응시켜 읽으면 어디가 새는지 보인다. 그리고 `packages/dev/docs/` — 같은 소스에서 여러 층의 문서를 생성하는 방식.

---

## Fluent UI (Microsoft)

```
repo: microsoft/fluentui
branch: master          ← main 아님, 주의
v9: packages/react-components/react-<component>/src/
tokens: packages/tokens/src/
updates: https://github.com/microsoft/fluentui/releases
```

**볼 때**: 대규모 조직에서 **버전 세대를 병행 운영**하는 방법(v8과 v9가 한 레포에 공존한다). 마이그레이션 기간이 몇 년 단위인 시스템의 현실적 구조. 그리고 `@fluentui/react-components`의 슬롯 기반 커스터마이징 API.

---

## Primer (GitHub)

```
repo: primer/react
branch: main
components: packages/react/src/<Component>/
updates: https://github.com/primer/react/releases
```

**볼 때**: 문서/디자인 가이드라인과 코드가 얼마나 밀착돼 있는지. 컴포넌트별 "언제 쓰지 말아야 하는가"를 명시하는 문서 관행.

---

## Polaris (Shopify)

```
repo: Shopify/polaris
branch: main
components: polaris-react/src/components/<Component>/
tokens: polaris-tokens/src/
updates: https://github.com/Shopify/polaris/releases
site: https://polaris.shopify.com
```

**유지 상태**: 최근 푸시 2026-01로 상당히 조용하다. 코드 참고보다 **가이드라인 문서** 쪽 가치가 크다.
**볼 때**: 콘텐츠 가이드라인(UX 라이팅 규범)이 이 분야에서 가장 상세한 축에 든다. 컴포넌트마다 "이럴 때 쓰고 이럴 때 쓰지 마라"가 문서화돼 있다.

---

## Carbon (IBM)

```
repo: carbon-design-system/carbon
branch: main
react: packages/react/src/components/<Component>/
styles: packages/styles/scss/
updates: https://github.com/carbon-design-system/carbon/releases
```

**볼 때**: 멀티 프레임워크 배포(React/Web Components/Angular/Vue)와 SCSS 토큰 체계. 접근성 검증 프로세스를 공개적으로 운영하는 방식.

---

## Tamagui

```
repo: tamagui/tamagui
branch: main
core: packages/core/src/
components: packages/tamagui/src/
updates: https://github.com/tamagui/tamagui/releases
```

**볼 때**: **웹과 React Native를 하나의 코드로 커버**하는 접근. 컴파일러가 플랫폼별로 스타일을 갈라 내보낸다. SEED의 web/Lynx 이원화와 문제의식이 겹치므로, "하나의 소스로 두 런타임"을 시도한 사례로 볼 가치가 있다.
**안 볼 때**: 웹 전용 프로젝트 (추상화 비용만 남는다).

---

## SEED (멀티플랫폼 관점)

```
repo: daangn/seed-design
branch: dev             ← main 아님, 주의
web: packages/react/src/components/          (84)
lynx: packages/lynx-react/src/components/    (13)
shared-spec: packages/rootage/
web-recipe: packages/qvism-preset/
lynx-recipe: packages/lynx-qvism-preset/
```

웹(React)과 Lynx 두 런타임을 **rootage 스펙을 공유하되 구현은 분리**하는 전략. Tamagui(하나의 소스로 컴파일)와 반대 방향의 선택이며, 각 런타임의 제약이 다를 때 이쪽이 현실적일 수 있다. 커버리지 격차(84 vs 13)가 이 전략의 비용이다.
