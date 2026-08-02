# 완성형 시스템 · registry

스타일까지 갖춘 컴포넌트 시스템들. **조립 방식과 배포(어떻게 사용자 손에 들어가는가)**를 볼 때 참고한다.

---

## shadcn/ui — 1순위 (배포 모델)

라이브러리가 아니라 **소스를 복사해 넣는 registry**. 이 모델 자체가 이 분야에서 가장 영향력 있는 아이디어였고, SEED의 snippet registry도 여기서 영감을 받았다.

**볼 때**: registry JSON 스키마, CLI로 컴포넌트를 주입하는 방식, 여러 primitive base를 동시에 지원하는 구조.
**안 볼 때**: 헤드리스 로직 자체 (shadcn은 Radix/Base UI/react-aria를 조합할 뿐이다).

> **CLI 4.13.0(2026-07)부터 base-ui가 기본 primitive다** — Radix가 아니다. 생태계의 무게중심이 옮겨가는 신호로 읽을 만하다. 이후 `addRegistryItems` 공개 API(4.15, CLI 없이 프로그램적 설치)와 `package.json`의 `registries` 필드(4.16)가 추가됐다.

```
repo: shadcn-ui/ui
branch: main
components: apps/v4/registry/new-york-v4/ui/<component>.tsx
blocks: apps/v4/registry/new-york-v4/blocks/
bases: apps/v4/registry/bases/{aria,base,radix}/
registry-def: apps/v4/registry/new-york-v4/registry.ts, apps/v4/registry/directory.json
cli: packages/shadcn/src/
updates: https://github.com/shadcn-ui/ui/releases
```

> 구조가 개편됐다: 예전 `apps/www/registry/...` 경로는 없어졌고 `apps/v4/` 하나만 남았다. 오래된 블로그/문서의 경로는 그대로 안 먹는다.

fetch 예시:
`https://raw.githubusercontent.com/shadcn-ui/ui/main/apps/v4/registry/new-york-v4/ui/select.tsx`

훔칠 포인트:
- `apps/v4/registry/bases/` — **같은 컴포넌트를 react-aria / Base UI / Radix 세 base 위에 각각 구현해 둔 구조.** primitive를 갈아끼울 수 있게 만든 접근이고, 같은 UI를 세 라이브러리로 비교해 읽기에 최적의 자료다
- `apps/v4/registry/.../registry.ts` + `directory.json` — 항목 메타(의존성, 파일 목록, 타입)를 어떻게 기술하는가
- `packages/shadcn/src/` — CLI가 항목을 해석해 프로젝트에 쓰는 절차 (SEED CLI와 비교)

SEED 대응: `docs/registry/react/ui/` (59개 snippet), `docs/registry/lynx/ui/` (7개), `__registry__/{framework}/`로 배포. framework 스코핑이 shadcn엔 없는 축이다.

---

## Park UI

Ark UI(=Zag) + Panda 조합의 완성형. **SEED와 구조적으로 가장 가까운 오픈소스**다: 헤드리스 로직 + recipe 스타일 레이어 + 토큰이 분리된 3층 구조.

**유지 상태**: 최근 푸시 2026-04로 다소 정체. 구조 참고용으로는 여전히 유효하다.

**볼 때**: "헤드리스 + recipe + 토큰"을 하나의 제품으로 묶는 방법, Panda recipe를 컴포넌트별로 배치하는 방식.
**안 볼 때**: 최신 유지보수가 필요한 프로덕션 의존성으로.

```
repo: cschroeter/park-ui
branch: main
components: packages/react/src/components/ui/
recipes: packages/panda-preset/src/theme/recipes/
updates: https://github.com/cschroeter/park-ui/releases
```

---

## Chakra UI v3

Zag 기반으로 전면 재작성된 버전. recipe/slot recipe 시스템을 정식 채택했다.

**볼 때**: 대규모 컴포넌트 세트에서 recipe를 실제로 어떻게 조직하는지, prop 네이밍 관례(size/variant/colorPalette).
**안 볼 때**: 가벼운 API — Chakra는 prop 표면이 넓다.

```
repo: chakra-ui/chakra-ui
branch: main
components: packages/react/src/components/<component>/
recipes: packages/react/src/theme/recipes/<component>.ts   ← 단일·슬롯 recipe가 한 디렉토리에 공존
exports: packages/react/src/theme/{recipes,slot-recipes}.export.ts
tokens: packages/react/src/theme/tokens/, semantic-tokens/
updates: https://github.com/chakra-ui/chakra-ui/releases
```

훔칠 포인트: `packages/react/src/theme/recipes/` — 여러 파트를 가진 컴포넌트의 스타일을 하나의 slot recipe로 묶는 실제 사례가 수십 개 있다. 어떤 게 단일이고 어떤 게 슬롯인지는 `slot-recipes.export.ts`가 목록으로 보여준다(`accordionSlotRecipe`처럼 `./recipes/<name>`에서 재수출). qvism recipe 작성 시 비교 대상.

---

## Radix Themes

Radix Primitives 위에 공식 스타일을 얹은 것.

**유지 상태**: 2026-04 이후 정체.
**볼 때**: 색상 스케일 시스템(radix-colors의 1~12단계 의미론 — 배경/경계/텍스트 역할이 번호에 고정)이 특히 참고할 만하다.

```
repo: radix-ui/themes
branch: main
components: packages/radix-ui-themes/src/components/
tokens: packages/radix-ui-themes/src/styles/tokens/
updates: https://github.com/radix-ui/themes/releases
```

훔칠 포인트: **radix-colors의 스케일 의미론.** 1=앱 배경, 3=컴포넌트 배경, 6=경계, 9=솔리드, 11=저대비 텍스트 식으로 번호마다 역할이 고정돼 있어서 다크모드 전환이 기계적으로 된다. 토큰 설계 시 비교할 가치가 크다.

---

## HeroUI

Tailwind 기반 완성형. tailwind-variants를 만든 팀.

```
repo: heroui-inc/heroui
branch: v3              ← main 아님, 주의
updates: https://github.com/heroui-inc/heroui/releases
```

**볼 때**: Tailwind만으로 완성형 시스템을 만들 때의 variant 조직 방식.

---

## Mantine

React 컴포넌트 세트 중 커버리지가 가장 넓은 편(100+). CSS Modules 기반.

```
repo: mantinedev/mantine
branch: master          ← main 아님, 주의
components: packages/@mantine/core/src/components/<Component>/
updates: https://github.com/mantinedev/mantine/releases
```

**볼 때**: "이 컴포넌트를 사람들이 실제로 어떤 API로 쓰나"의 넓은 표본. 흔치 않은 컴포넌트(Spotlight, Dropzone, RichTextEditor 등)의 API 참고.
**안 볼 때**: 헤드리스 설계 (Mantine은 스타일과 로직이 붙어 있다).

---

## SEED react

```
repo: daangn/seed-design
branch: dev             ← main 아님, 주의
components: packages/react/src/components/<Component>/     (84개)
lynx: packages/lynx-react/src/components/<Component>/       (13개)
registry: docs/registry/{react,lynx}/ui/
cli: packages/cli/src/
```

구조: `react-headless`(로직) + `qvism-preset`(recipe) + `rootage`(토큰) 3층 위에 얹힌 스타일드 레이어. shadcn식 snippet registry로도 배포하며, framework 스코핑(`react`/`lynx`)이 추가돼 있다.
