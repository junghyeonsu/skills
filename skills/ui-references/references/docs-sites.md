# 문서 사이트 IA 레퍼런스

**문서 구조를 어떻게 짤 것인가**를 참고할 때 보는 축. 컴포넌트 페이지 구성, 가이드라인과 API의 분리, 파운데이션 문서화, 그리고 에이전트가 읽을 수 있는 형태(llms.txt / MCP)를 정리한다.

llms.txt 유무는 2026-08-02 실측이다.

---

## 요약 표

| 사이트 | llms.txt | 문서 소스 | 두드러진 점 |
| --- | --- | --- | --- |
| astryx.atmeta.com | ✅ | `facebook/astryx` → `apps/docsite/src/` | agent-ready 표방, CLI가 문서를 낸다 |
| base-ui.com | ✅ | `mui/base-ui` → `docs/src/` | API 레퍼런스가 자동 생성·매우 정밀 |
| ui.shadcn.com | ✅ | `shadcn-ui/ui` → `apps/v4/content/` | 문서 = 설치 지시서. registry와 일체 |
| chakra-ui.com | ✅ | `chakra-ui/chakra-ui` → `apps/www/` | **MCP 서버 제공** (`apps/mcp/`) |
| seed-design.io | ✅ | `daangn/seed-design` → `docs/content/` | 영역별 llms.txt + 컴포넌트별 개별 txt |
| spectrum.adobe.com | ❌ | (사이트는 비공개, 코드 문서는 레포) | 디자인 가이드와 구현 문서가 분리된 두 사이트 |
| m3.material.io | ❌ | (비공개) | 디자인 사양 중심. 코드 문서는 별도 |
| polaris.shopify.com | ❌ | `Shopify/polaris` → `polaris.shopify.com/` | 콘텐츠 가이드라인이 가장 상세 |

---

## astryx.atmeta.com

```
site: https://astryx.atmeta.com
llms: https://astryx.atmeta.com/llms.txt
repo: facebook/astryx
docs-source: apps/docsite/src/
updates: https://github.com/facebook/astryx/releases
```

**볼 것**: "사람과 에이전트가 같은 문서를 쓴다"를 목표로 잡았을 때 실제 산출물이 어떤 모습인지. 레포 루트에 `CLAUDE.md`와 `.claude/`가 있고, CLI가 agent용 문서를 출력한다. 문서·API·CLI를 따로 만들지 않고 **한 소스에서 세 형태로 내보내는** 접근.

같이 볼 것: `apps/storybook/`, `apps/sandbox/`, `apps/template-viewer/`가 문서 사이트와 별개 앱으로 분리돼 있다. 문서/플레이그라운드/템플릿의 역할 분리 사례.

---

## base-ui.com

```
site: https://base-ui.com
llms: https://base-ui.com/llms.txt
repo: mui/base-ui
docs-source: docs/src/
updates: https://github.com/mui/base-ui/releases
```

**볼 것**: 헤드리스 라이브러리의 API 문서가 어디까지 정밀해질 수 있는가. 각 파트(Root/Trigger/Popup/Item…)별로 prop, data attribute, CSS 변수가 표로 정리돼 있다. **data attribute와 CSS 변수를 공개 API로 문서화하는 관행**이 특히 참고할 만하다 — 스타일링 가능 지점을 명시적으로 계약화한 것.

---

## ui.shadcn.com

```
site: https://ui.shadcn.com
llms: https://ui.shadcn.com/llms.txt
repo: shadcn-ui/ui
docs-source: apps/v4/content/
registry: apps/v4/registry/
updates: https://github.com/shadcn-ui/ui/releases
```

**볼 것**: 문서가 곧 설치 절차인 구조. 각 컴포넌트 페이지가 "CLI 한 줄 / 수동 설치 소스"를 나란히 준다. 문서와 registry가 같은 소스에서 나오므로 **문서에 적힌 코드와 실제 배포되는 코드가 어긋날 수 없다.**

SEED 대응: `docs/registry/`와 `docs/content/`의 관계, `BlockCodeTabs`가 registry JSON의 innerDependencies를 읽어 코드 탭을 자동 생성하는 방식이 같은 문제의식이다.

---

## chakra-ui.com

```
site: https://chakra-ui.com
llms: https://chakra-ui.com/llms.txt
repo: chakra-ui/chakra-ui
docs-source: apps/www/
mcp: apps/mcp/
updates: https://github.com/chakra-ui/chakra-ui/releases
```

**볼 것**: **MCP 서버를 문서 전달 채널로 제공**한다(`apps/mcp/`). llms.txt가 정적 텍스트 덤프라면 MCP는 질의 가능한 인터페이스다. 에이전트 대상 문서 제공의 두 번째 형태이고, SEED가 llms.txt 다음 단계를 고민한다면 참고 지점.

`apps/compositions/`도 흥미롭다 — 문서에 나오는 조합 예제를 별도 앱으로 관리한다.

---

## seed-design.io

```
site: https://seed-design.io
llms: https://seed-design.io/llms.txt
repo: daangn/seed-design
branch: dev
docs-source: docs/content/
updates: https://github.com/daangn/seed-design/releases
```

**구조**: 영역별 llms.txt(`/react/llms.txt`, `/foundations/llms.txt`, `/components/llms.txt`) + 컴포넌트별 개별 문서(`/llms/react/components/{name}.txt`). CLI로도 접근 가능(`npx @seed-design/cli@latest docs {component}`).

다른 사이트와 비교했을 때 특이한 축: **플랫폼(react/lynx) 분리**가 정보구조에 들어가 있다. 대부분의 시스템은 단일 플랫폼이라 이 축이 없다.

---

## spectrum.adobe.com

```
site: https://spectrum.adobe.com
llms: (없음 — /llms.txt는 SPA 폴백 HTML을 반환)
repo: adobe/react-spectrum
docs-source: packages/dev/docs/
```

**볼 것**: **디자인 가이드라인과 구현 문서를 분리된 두 사이트로 운영**한다. spectrum.adobe.com은 디자이너용 사양(색·타이포·모션·글쓰기), react-spectrum.adobe.com은 개발자용 API. 각각 대상 독자가 다르고 갱신 주기도 다르다.

SEED는 한 사이트에 둘을 합쳐 두는 방식이라(컴포넌트 페이지 안에 가이드라인 + API), 분리/통합의 트레이드오프를 볼 때 대조군이 된다.

---

## m3.material.io

```
site: https://m3.material.io
llms: (없음)
```

**볼 것**: 디자인 사양의 깊이. 색상 역할 체계(primary/on-primary/primary-container…), 동적 색상 생성, 상태 레이어(state layer) 개념처럼 **토큰 이름 자체가 의미를 담도록 설계된** 사례. 코드보다 사양 문서로서의 가치가 크다.

**주의**: 웹 구현체(material-web)는 개발이 축소된 상태이므로 코드 참고처로는 권하지 않는다.

---

## polaris.shopify.com

```
site: https://polaris.shopify.com
llms: (없음)
repo: Shopify/polaris
docs-source: polaris.shopify.com/
guidelines: documentation/
updates: https://github.com/Shopify/polaris/releases
```

**볼 것**: **콘텐츠 가이드라인**이 이 분야에서 가장 상세한 축이다. 컴포넌트마다 "이럴 때 쓴다 / 이럴 때 쓰지 마라"와 함께 문구 작성 규범(대소문자, 톤, 에러 메시지 문형)이 붙는다. 문서에 "하지 말아야 할 것"을 명시하는 관행 자체가 참고 대상.

**주의**: 레포 최근 푸시 2026-01로 조용하다. 코드보다 문서 참고용.

---

## 문서 구조를 짤 때 챙길 축 (위 사례들에서 공통으로 갈리는 지점)

1. **가이드라인과 API를 한 페이지에 둘 것인가, 분리할 것인가** — Spectrum은 사이트를 나눴고, SEED·Polaris는 한 페이지에 둔다. 독자가 디자이너와 개발자로 갈릴수록 분리가 유리하다
2. **코드 예제의 출처** — 문서에 하드코딩할지, registry/소스에서 끌어올지. shadcn과 SEED는 후자라 어긋남이 구조적으로 불가능하다
3. **스타일링 계약을 문서화하는가** — Base UI처럼 data attribute·CSS 변수를 공개 API로 표에 넣으면, 사용자가 무엇에 의존해도 되는지 명확해진다
4. **에이전트 채널** — 없음 / llms.txt(정적) / MCP(질의형). 현재 llms.txt가 사실상 기본값이고 MCP는 chakra 같은 선발 사례가 나오는 단계
5. **플랫폼 축이 IA에 들어가는가** — 멀티플랫폼이면 피할 수 없다(SEED). 단일 플랫폼이면 불필요한 계층
