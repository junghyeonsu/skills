# 대형 · 멀티플랫폼 시스템

기업 규모로 운영되는 디자인시스템들. 개별 컴포넌트보다 **시스템을 어떻게 운영·확장·배포하는가**를 볼 때 참고한다.

---

## Astryx (Meta) — 주목

Meta 내부에서 오래 쓰이다 오픈소스로 나온 시스템. React + StyleX 기반, MIT.

**볼 때**: **"에이전트가 쓰는 디자인시스템"을 어떻게 설계하는가** — 이 시스템이 내건 명시적 목표다. 그리고 eject(swizzle) 모델, 테마를 CSS 변수 오버라이드로만 정의하는 방식.
**안 볼 때**: 성숙도가 중요한 프로덕션 의존성으로 — 공개된 지 얼마 안 됐다. 채택 전에 현재 안정성 단계를 직접 확인할 것.

```
repo: facebook/astryx
branch: main
components: packages/core/src/<PascalCase>/
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

훔칠 포인트:
- **스타일 구현을 소비자에게 숨기는 경계** — StyleX로 작성했지만 사용자는 미리 빌드된 CSS를 import하고 `className`으로 덮어쓴다. 빌드 플러그인·PostCSS 설정이 필요 없다. "우리는 X로 만들지만 너희는 X를 몰라도 된다"는 선긋기. 스타일 도구를 어디까지 노출할지 정할 때의 한 극단
- **swizzle (eject)** — `packages/cli/`. 컴포넌트 전체 소스를 프로젝트로 꺼내 소유하게 하는 명령. shadcn의 복사 모델과 라이브러리 모델의 절충안이다
- **agent-ready 표방** — 레포 루트에 `CLAUDE.md`와 `.claude/`가 있고 CLI가 agent용 문서를 낸다. 문서·API·CLI를 사람과 에이전트가 같은 방식으로 쓰도록 설계했다고 주장한다
- **테마 = CSS custom property 오버라이드만** — 포크나 래핑 없이 디자이너가 테마를 바꿀 수 있게 한 제약
- `packages/lab/` — 실험 컴포넌트를 별도 dist-tag로만 배포해 안정 API와 분리하는 방식

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

> **함정**: `packages/@react-aria/*`, `packages/@react-stately/*`, `packages/@react-spectrum/*`은 `index.ts`만 있는 re-export 셸이다. 실제 구현은 위 표의 경로에 있다. 외부 문서나 블로그가 안내하는 `packages/@react-aria/...` 경로로는 소스를 못 읽는다. `@internationalized/*`만 예외로 그 경로에 실물이 있다.

훔칠 포인트: **각 층의 경계 규칙 자체.** 상태는 DOM을 모르고, 동작은 스타일을 모르고, 제품 층만 브랜드를 안다. 자기 시스템의 레이어와 대응시켜 읽으면 어디가 새는지 보인다. 그리고 `packages/dev/docs/` — 같은 소스에서 여러 층의 문서를 생성하는 방식.

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

**볼 때**: **웹과 React Native를 하나의 코드로 커버**하는 접근. 컴파일러가 플랫폼별로 스타일을 갈라 내보낸다. 멀티 런타임을 "하나의 소스로 컴파일" 쪽으로 풀 때의 참고 사례 — 반대 극단은 런타임별로 구현을 나누고 스펙만 공유하는 방식이다.
**안 볼 때**: 웹 전용 프로젝트 (추상화 비용만 남는다).

