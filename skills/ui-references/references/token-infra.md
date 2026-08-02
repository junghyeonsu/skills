# 토큰 · 테마 인프라

디자인 토큰을 정의하고 여러 플랫폼용 산출물로 변환하는 도구들. **토큰 파이프라인을 설계할 때** 보는 축.

---

## Style Dictionary — 사실상 표준

Amazon. 토큰(JSON/JS)을 받아 CSS/SCSS/iOS/Android/Flutter 등으로 변환한다. 이 분야에서 가장 오래되고 널리 쓰인다.

**볼 때**: 하나의 토큰 소스에서 여러 플랫폼 산출물을 뽑는 구조, 변환 파이프라인(parser → transform → format)의 설계, 토큰 참조(`{color.base.blue}`) 해석 방식.
**안 볼 때**: 웹만 대상이고 변환이 단순할 때 (설정 비용이 더 클 수 있다).

```
repo: amzn/style-dictionary
branch: main
core: lib/
transforms: lib/common/transforms.js
formats: lib/common/formats.js
updates: https://github.com/amzn/style-dictionary/releases
```

fetch 예시:
`https://raw.githubusercontent.com/amzn/style-dictionary/main/lib/common/transforms.js`

훔칠 포인트:
- `lib/common/transforms.js` — 이름 변환(kebab/camel/PascalCase), 단위 변환(px→rem→dp→pt), 색상 변환이 각각 독립 transform으로 등록되는 구조
- `lib/common/formats.js` — 같은 토큰을 CSS 변수/SCSS 맵/Swift enum/Kotlin object로 내보내는 포맷터들
- 참조 해석 로직 — 토큰이 다른 토큰을 가리킬 때의 순환 참조 검출

rootage와 비교: rootage도 YAML → 여러 산출물(css vars, qvism vars, 타입) 파이프라인이다. Style Dictionary가 **플랫폼 다양성**(iOS/Android까지)에 최적화된 반면 rootage는 **컴포넌트 스펙까지 포함**(단순 토큰이 아니라 ComponentSpec)한다는 차이가 있다. 네이티브 플랫폼 확장을 검토할 때 이쪽 transform 목록이 체크리스트가 된다.

---

## DTCG (Design Tokens Community Group)

W3C 커뮤니티 그룹의 토큰 포맷 표준안. 도구가 아니라 **스펙**이다.

**볼 때**: 토큰 파일 포맷을 새로 정하거나 바꿀 때, 다른 도구(Figma 플러그인, Style Dictionary, Terrazzo)와의 상호운용이 필요할 때.
**안 볼 때**: 내부 전용 포맷으로 충분하고 외부 도구와 주고받을 일이 없을 때.

```
repo: design-tokens/community-group
branch: main
spec: technical-reports/format/
updates: https://github.com/design-tokens/community-group/releases
```

핵심 개념: `$value`/`$type`/`$description`, 그룹 중첩, `{alias.reference}` 참조, composite 토큰(shadow, typography처럼 여러 값을 묶은 것).

rootage YAML은 DTCG와 다른 자체 포맷이다(`values: { theme-light: …, theme-dark: … }` 형태로 테마를 값에 내장). **DTCG는 테마를 파일 분리로 표현**하는 쪽이라 구조가 다르니, 상호 변환을 검토한다면 이 차이가 첫 관문이다.

---

## Terrazzo (구 Cobalt)

DTCG 네이티브 토큰 빌드 도구. Style Dictionary보다 최신이고 DTCG 준수가 목표다.

**볼 때**: DTCG 포맷을 실제로 소비하는 구현이 궁금할 때, 타입 생성이 잘 된 토큰 빌드 도구를 볼 때.
**안 볼 때**: 생태계 성숙도가 중요할 때 (Style Dictionary 대비 사용처가 적다).

```
repo: terrazzoapp/terrazzo
branch: main
core: packages/parser/src/, packages/cli/src/
plugins: packages/plugin-css/src/, packages/plugin-js/src/
updates: https://github.com/terrazzoapp/terrazzo/releases
```

훔칠 포인트: `packages/parser/src/` — DTCG 문서를 파싱·검증하는 구현. rootage core의 검증 계층(hand-written parser/analyzer)과 비교해 읽을 만하다.

---

## Tokens Studio (Figma 플러그인)

Figma에서 토큰을 관리하고 코드로 내보내는 도구.

**볼 때**: 디자인 툴 ↔ 코드 동기화 워크플로를 설계할 때, Figma 변수와 토큰 파일을 매핑하는 방식.

```
repo: tokens-studio/figma-plugin
branch: main
updates: https://github.com/tokens-studio/figma-plugin/releases
```

SEED는 자체 `figma:sync` 경로(Figma 변수 → rootage YAML)를 쓰고 있어 직접 대체재는 아니지만, **동기화 충돌 해결 UX**(양쪽이 동시에 바뀌었을 때)를 어떻게 다루는지가 참고 지점이다.

---

## 색상 스케일 참고

토큰 값 자체를 정할 때 참고할 것들:

| 소스 | 특징 |
| --- | --- |
| `radix-ui/colors` | 1~12 각 단계에 **역할이 고정**돼 있다(1=앱 배경, 3=컴포넌트 배경, 6=경계, 9=솔리드, 11=저대비 텍스트). 다크모드가 기계적으로 대응됨 |
| Tailwind 기본 팔레트 | 50~950, oklch로 정의됨. 가장 익숙한 관례 |
| Material 3 | 색상 역할(primary/on-primary/container 등) 체계. 동적 색상 생성 알고리즘 포함 |

```
repo: radix-ui/colors
branch: main
scales: src/
```

**oklch 등 지각적 색공간으로 팔레트를 만드는 방법**은 이 파일이 아니라 색상 스킬 쪽이 정본이다 — [skill-collections.md](skill-collections.md) 참고.

---

## SEED rootage

```
repo: daangn/seed-design
branch: dev             ← main 아님, 주의
tokens: packages/rootage/*.yaml
component-specs: packages/rootage/components/*.yaml
core: ecosystem/rootage-core/src/
generated: packages/css/vars/, packages/qvism-preset/src/vars/    ← 직접 수정 금지
```

다른 도구와 다른 점: 토큰뿐 아니라 **ComponentSpec**(슬롯·variant·상태별 값)까지 같은 스키마 체계로 기술한다. 즉 "이 컴포넌트의 brandSolid variant에서 root 슬롯의 배경색"까지 YAML에 있고, 거기서 recipe와 타입이 생성된다. Style Dictionary/Terrazzo는 토큰까지만 다룬다.

검증 컨벤션: rootage core는 zod를 쓰지 않고 hand-written parser(throw)/analyzer(ValidationResult) 구조다. 새 스펙 검증을 추가할 때 이 관례를 따른다.
