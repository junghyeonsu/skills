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

자체 파이프라인과 비교할 축: Style Dictionary는 **플랫폼 다양성**(웹뿐 아니라 iOS/Android/Flutter)에 최적화돼 있다. 웹만 대상이면 과한 반면, 네이티브 확장을 검토하는 시점엔 이쪽 transform 목록이 그대로 체크리스트가 된다.

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

자체 포맷을 쓰다가 상호 변환을 검토할 때 첫 관문은 보통 **테마를 어디에 두는가**다. DTCG는 테마를 파일/그룹 분리로 표현하는 쪽인데, 토큰 하나의 값 안에 모드별 값을 내장하는 포맷(`{ light: …, dark: … }`)과는 구조가 어긋난다.

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

훔칠 포인트: `packages/parser/src/` — DTCG 문서를 파싱·검증하는 구현. 토큰 검증 계층을 직접 짤 때 참고할 만하다.

---

## Tokens Studio (Figma 플러그인)

Figma에서 토큰을 관리하고 코드로 내보내는 도구.

**볼 때**: 디자인 툴 ↔ 코드 동기화 워크플로를 설계할 때, Figma 변수와 토큰 파일을 매핑하는 방식.

```
repo: tokens-studio/figma-plugin
branch: main
updates: https://github.com/tokens-studio/figma-plugin/releases
```

Figma 변수를 직접 읽어 자체 동기화 경로를 만든 경우엔 대체재가 아니지만, **동기화 충돌 해결 UX**(디자인과 코드가 동시에 바뀌었을 때 무엇을 이기게 할 것인가)를 어떻게 다루는지가 참고 지점이다.

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

