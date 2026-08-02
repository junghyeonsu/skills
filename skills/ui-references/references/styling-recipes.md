# 스타일 · recipe 레이어

variant를 어떻게 정의하고 CSS로 내보낼 것인가. **컴포넌트의 스타일 API를 설계할 때** 보는 축.

핵심 축 세 개: (1) 런타임인가 빌드타임인가, (2) 여러 파트(slot)를 한 recipe로 묶을 수 있는가, (3) variant 조합(compound)을 어떻게 표현하는가.

---

## Panda CSS — 1순위

Chakra 팀의 빌드타임 CSS-in-JS. **slot recipe 개념의 참조 구현**이고, SEED의 qvism과 가장 가까운 물건이다.

**볼 때**: recipe/slot recipe 스키마를 설계할 때, 정적 추출(빌드타임에 CSS를 뽑아내는) 방식이 궁금할 때, 토큰→유틸리티 생성 파이프라인을 볼 때.
**안 볼 때**: 런타임 조건부 스타일이 많이 필요할 때 (빌드타임 추출의 한계).

```
repo: chakra-ui/panda
branch: main
core: packages/core/src/
generator: packages/generator/src/
presets: packages/preset-base/src/, packages/preset-panda/src/
types: packages/types/src/
updates: https://github.com/chakra-ui/panda/releases
```

fetch 예시:
`https://raw.githubusercontent.com/chakra-ui/panda/main/packages/core/src/recipes.ts`

훔칠 포인트:
- `packages/core/src/recipes.ts` + `packages/core/src/slot-recipe.ts` — recipe 해석 로직. base/variants/compoundVariants/defaultVariants가 어떻게 CSS로 펼쳐지는가
- `packages/types/src/recipe.ts` — recipe 타입 정의. **variant 스키마에서 타입을 유도하는 방식**이 핵심
- `packages/generator/src/artifacts/` — 설정에서 코드/타입을 생성하는 구조 (rootage codegen과 비교)
- `packages/preset-base/src/` — 유틸리티 정의 방식

SEED와 비교할 점: qvism도 `defineRecipe({ name, base, variants, compoundVariants, defaultVariants })` 형태로 같은 개념을 쓴다. 다른 점은 SEED가 **rootage YAML을 원천으로 두고 recipe를 생성**하는 층이 하나 더 있다는 것. Panda는 recipe 자체가 원천이다.

---

## CVA (class-variance-authority)

클래스 문자열 조합만 하는 최소 라이브러리. Tailwind + shadcn 조합의 사실상 기본값.

**볼 때**: variant API의 가장 작은 형태가 궁금할 때. 코드가 짧아서 30분이면 전부 읽는다.
**안 볼 때**: slot(여러 파트)이 필요할 때 — CVA는 단일 요소용이다.

```
repo: joe-bell/cva
branch: main
core: packages/class-variance-authority/src/index.ts
updates: https://github.com/joe-bell/cva/releases
```

훔칠 포인트: `src/index.ts` 하나. compound variant 매칭 로직이 어떻게 이렇게 짧을 수 있는지.

---

## tailwind-variants

CVA + slot + Tailwind 충돌 해결(tailwind-merge)을 합친 것. HeroUI가 관리한다.

**볼 때**: CVA로 부족한데 Panda까지 가긴 무거울 때. slot을 클래스 기반으로 다루는 방식.

```
repo: heroui-inc/tailwind-variants
branch: main
core: src/index.ts
updates: https://github.com/heroui-inc/tailwind-variants/releases
```

---

## vanilla-extract

TypeScript로 CSS를 쓰고 빌드타임에 정적 CSS를 뽑는다. 타입 안전한 테마 컨트랙트가 특징.

**볼 때**: 테마를 타입으로 강제하는 방법(`createThemeContract`), zero-runtime 접근이 궁금할 때, sprinkles(원자적 유틸 생성)를 볼 때.
**안 볼 때**: 동적 값이 많은 스타일.

```
repo: vanilla-extract-css/vanilla-extract
branch: master          ← main 아님, 주의
packages: packages/{css,recipes,sprinkles,dynamic}/src/
updates: https://github.com/vanilla-extract-css/vanilla-extract/releases
```

훔칠 포인트:
- `packages/css/src/theme.ts` — 테마 컨트랙트. **"토큰 구조를 타입으로 고정하고 값만 갈아끼운다"**는 아이디어가 rootage 다중 테마와 비교할 만하다
- `packages/recipes/src/` — recipe의 또 다른 구현 (Panda와 비교)
- `packages/sprinkles/src/` — 유틸리티 클래스를 설정에서 생성

---

## StyleX

Meta의 스타일 시스템. Astryx가 이걸로 작성됐다.

**볼 때**: 대규모(수만 컴포넌트) 환경에서의 스타일 병합·우선순위 전략이 궁금할 때. **스타일 충돌을 "나중 것이 이긴다"로 결정론적으로 만드는 방식**이 핵심 아이디어.
**안 볼 때**: 소규모 프로젝트 — 도입 비용이 크다.

```
repo: facebook/stylex
branch: main
packages: packages/@stylexjs/stylex/src/
updates: https://github.com/facebook/stylex/releases
```

Astryx가 흥미로운 이유: **StyleX로 작성했지만 소비자에겐 그게 안 보인다.** 미리 빌드된 CSS를 import하고 `className`으로 덮어쓰는 구조라, 사용자는 Tailwind든 CSS Modules든 자기 것을 쓴다. "우리는 X로 만들었지만 너희는 X를 몰라도 된다"는 경계 설정이 참고할 만하다 → [platform-systems.md](platform-systems.md)

---

## SEED qvism-preset

SEED의 recipe 레이어. Panda와 같은 개념을 쓰되 rootage를 원천으로 둔다.

```
repo: daangn/seed-design
branch: dev             ← main 아님, 주의
recipes: packages/qvism-preset/src/recipes/
vars: packages/qvism-preset/src/vars/     ← rootage 생성물, 직접 수정 금지
utils: packages/qvism-preset/src/utils/   ← define, pseudo 등
output: packages/css/recipes/             ← 생성물, 직접 수정 금지
```

주의: `packages/css/vars/`, `packages/css/recipes/`, `packages/qvism-preset/src/vars/`는 **생성물**이다. 고칠 때는 원천(rootage YAML 또는 preset recipe)을 고치고 생성 명령을 돌린다.

pseudo 선택자 규약(`active`가 hover/pressed를 겸함 — 모바일 우선)처럼 제품 맥락에서 나온 결정들이 있어서, 범용 라이브러리와 다른 부분은 그 이유를 먼저 확인할 것.
