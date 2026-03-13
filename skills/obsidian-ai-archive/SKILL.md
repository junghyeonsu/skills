---
name: obsidian-ai-archive
description: 로컬 Obsidian vault에 AI 뉴스, 모델 업데이트, 릴리스 노트, 소셜 포스트, 논문, product page, tool discovery, 그리고 거기서 파생된 교훈을 구조적으로 저장하는 스킬. Obsidian CLI를 사용해 외부 signal을 `Inbox`, `News`, `Lessons`로 분류하고, 질문 후 저장 초안을 제안한 뒤 승인된 내용만 저장할 때 사용한다.
---

# Obsidian AI Archive

## 목적

AI 관련 링크, 발표, 제품 출시, 모델 업데이트, 스레드, 글, 논문, tool discovery를 로컬 Obsidian vault에 나중에 다시 찾기 쉬운 형태로 저장한다.

- Obsidian CLI만 사용한다.
- 저장 전에 짧은 후속 질문으로 의미를 구체화한다.
- 질문 뒤에는 바로 저장하지 않고, 에이전트가 저장 초안을 먼저 제안한다.
- 분류는 `Inbox`, `News`, `Lessons` 세 가지로 고정한다.
- `title`, `description`, `content` 중심의 스캔 가능한 구조를 유지한다.
- 태그는 적게 쓰고, 기존 태그를 강하게 재사용한다.
- 긴 원문 복붙보다 압축된 요약을 남긴다.

## 언제 이 스킬을 사용할지

다음 상황에서 이 스킬을 사용한다.

- 사용자가 "Obsidian에 저장해줘", "아카이브해줘", "기억해줘"라고 할 때
- 대화 중 저장 가치가 있는 AI 관련 링크나 signal이 등장할 때
- 사용자가 나중에 다시 찾기 위한 구조화된 저장을 원할 때
- 단순 뉴스 저장이 아니라 "내 관점에서 왜 중요한지"까지 남기고 싶을 때
- 태그를 안정적으로 관리해야 할 때

다음은 저장 대상에서 제외한다.

- 일회성 반응만 있는 단순 채팅
- AI와 무관한 일반 링크
- 이미 같은 의미로 충분히 정리된 노트의 중복 사본
- 질문을 해도 무엇인지와 중요성이 전혀 확보되지 않는 잡음

## 실행 절차

다음 순서를 지킨다.

1. 입력이 외부 signal인지, 기존 saved item에서 파생된 해석인지 빠르게 파악한다.
2. 2-4개의 짧은 후속 질문으로 `무엇`, `왜 중요한지`, `나와 어떤 관련이 있는지`, `나중에 무엇을 판단하려고 다시 볼지`를 채운다.
3. 답변을 바탕으로 에이전트가 저장 초안을 먼저 제안한다.
4. 저장 초안에는 최소한 `category`, `title`, `description`, `tags`를 포함한다.
5. 사용자가 수정하거나 승인하면 그때 저장한다.
6. 저장 직전에 중복 노트와 기존 태그를 확인한다.
7. 새 노트를 만들거나, 같은 항목의 후속 정보면 기존 노트에 덧붙인다.
8. 원본 링크나 소식은 `News`에 남기고, 해석이나 교훈은 필요할 때 별도 `Lessons` 노트로 승격한다.

질문만 하고 끝내지 않는다. 질문 후에는 반드시 저장 초안을 먼저 제안한다.

## 저장 전 확인

Obsidian CLI 예시는 환경 변수 `OBSIDIAN_VAULT`를 기준으로 통일한다.

```sh
obsidian vault="$OBSIDIAN_VAULT" search query="<핵심어>"
obsidian vault="$OBSIDIAN_VAULT" tags counts
obsidian vault="$OBSIDIAN_VAULT" create path="<Category>/<file-name>.md" content="<note-content>"
obsidian vault="$OBSIDIAN_VAULT" read path="<Category>/<file-name>.md"
obsidian vault="$OBSIDIAN_VAULT" append path="<Category>/<file-name>.md" content="<additional-content>"
```

CLI가 동작하지 않으면 설치 절차를 길게 설명하지 말고, `OBSIDIAN_VAULT` 값과 실행 가능한 명령만 확인한 뒤 저장을 보류한다.

## 카테고리 선택 규칙

### `Inbox`

맥락이 부족하거나, 왜 중요한지 아직 정리되지 않은 항목에 사용한다.

적합한 예:

- 링크는 있는데 핵심이 아직 안 잡힘
- 흥미로운 스레드 같지만 지금은 읽을 시간이 없음
- 저장 가치는 느껴지지만 내 관점에서 왜 중요한지 설명이 안 됨

운영 규칙:

- `Inbox`는 영구 보관소가 아니다.
- 맥락이 충분해지면 `News` 또는 `Lessons`로 재분류한다.
- 오래된 `Inbox` 항목은 정리 대상으로 본다.
- 링크 무덤처럼 쌓아두지 않는다.

### `News`

외부에서 들어온 저장 가치 있는 signal 대부분을 여기에 저장한다. 제품성은 별도 카테고리로 두지 않고, 태그, `entities`, 본문으로 표현한다.

적합한 예:

- 모델 업데이트
- 제품 출시
- 기능 출시
- 릴리스 노트
- 벤치마크
- 연구 발표
- policy announcement
- industry announcement
- X/Twitter/Threads/LinkedIn post
- write-up
- paper
- product page
- tool discovery

핵심은 "외부에서 들어온 worth-saving item"인지 여부다. 제품 링크든 모델 업데이트든, 원본 signal은 기본적으로 `News`에 둔다.

### `Lessons`

`News` 또는 여러 saved item에서 추출한 상위 해석, 재사용 가능한 교훈, 관점, 전략적 시사점, 앞으로의 추적 기준을 저장한다.

적합한 예:

- 여러 제품 출시를 보다 보니 반복되는 패턴이 드러남
- 모델 업데이트를 보며 장기적으로 더 중요하게 봐야 할 축이 생김
- 앞으로 어떤 카테고리를 계속 추적할지 기준이 정리됨

운영 원칙:

- `Lessons`는 원본 링크를 대체하지 않는다.
- 원본 링크/소식은 `News`에 남긴다.
- 교훈은 별도 `Lessons` 노트로 분리해 저장한다.
- 필요하면 `related`로 연결한다.
- archive와 insight를 한 노트에서 섞어 처리하지 않는다.

## 후속 질문 전략

질문은 짧고 구체적으로 유지한다. 보통 2-4개면 충분하다.

기본 질문 예:

1. "이 링크는 정확히 무엇인가요? 업데이트, 출시, 글, 스레드, 논문 중 무엇에 가깝나요?"
2. "무엇이 새롭거나 중요해 보였나요?"
3. "이게 내 일, 내 제품 아이디어, 내 콘텐츠 관점에서 왜 중요한가요?"
4. "나중에 다시 찾을 때 무엇을 판단하려고 보려는가요?"

필요하면 아래 보조 질문을 사용한다.

### `News` 보조 질문

- "이건 일반 뉴스라기보다 나에게 어떤 signal인가요?"
- "나중에 다시 보면 확인하고 싶은 포인트가 무엇인가요?"
- "이 항목의 핵심은 변화 자체인가요, 아니면 특정 주제를 계속 추적할 이유인가요?"

### `Lessons` 보조 질문

- "이 항목들에서 남겨야 할 교훈 한 줄은 무엇인가요?"
- "앞으로 무엇을 더 주목하거나 무시해야 하나요?"
- "이 교훈과 이어지는 기존 노트가 있나요?"

### `Inbox` 보조 질문

- "지금 빠진 맥락은 무엇인가요?"
- "나중에 다시 볼 때 꼭 답해야 할 질문은 무엇인가요?"

질문의 목적은 긴 감상을 받는 것이 아니다. 아래 네 가지가 확보되면 충분하다.

- 무엇인지
- 왜 중요한지
- 나에게 어떤 signal인지
- 나중에 무엇을 판단하려고 다시 볼지

## 저장 초안 제안 규칙

질문이 끝나면 에이전트는 저장 초안을 먼저 제안한다. 사용자가 수정하거나 승인하면 그때 저장한다.

저장 초안에는 최소한 아래 네 가지를 포함한다.

- `category`
- `title`
- `description`
- `tags`

필요하면 아래도 함께 제안한다.

- `entities`
- `related`
- `source`

기본 초안 예:

```md
저장 초안

- category: News
- title: "OpenAI reasoning model update"
- description: "This matters because it may change how I judge current coding and agent workflows."
- tags:
  - area/model
  - signal/update
- entities:
  - OpenAI
```

초안 제시 원칙:

- 사용자의 원문을 그대로 복사하지 않는다.
- 검색 가능하고 재사용 가능한 형태로 다시 쓴다.
- title은 사람이 읽기 쉬운 문장형으로 쓴다.
- description은 왜 중요한지 한 문장으로 정리한다.

## 파일명 규칙

파일명은 slug로 유지한다.

- 파일명 패턴: `YYYY-MM-DD-short-searchable-slug.md`
- 파일명은 소문자와 하이픈을 사용한다.
- 제목의 핵심 검색어를 남기되, 불필요하게 길게 만들지 않는다.
- title과 파일명은 일치할 필요가 없다.

예:

- `title: "OpenAI reasoning model update"`
- `path: "News/2026-03-13-openai-reasoning-model-update.md"`

- `title: "Button size token alignment decision"`
- `path: "Lessons/2026-03-13-button-size-token-alignment-decision.md"`

## 노트 포맷

기본 frontmatter는 아래 필드를 사용한다.

```yaml
---
title: "<human-readable sentence-style title>"
description: "<one-sentence why it matters>"
category: "<Inbox|News|Lessons>"
tags:
  - <tag-1>
  - <tag-2>
captured_at: "<ISO-8601 timestamp>"
---
```

필요할 때만 아래 선택 필드를 허용한다.

```yaml
source: "https://..."
entities:
  - "<company-or-product-or-model-name>"
related:
  - "[[Folder/Note Title]]"
```

필드 규칙:

- `title`: 사람이 읽기 쉬운 문장형으로 쓴다.
- `description`: 왜 중요한지 한 문장으로 쓴다.
- `category`: `Inbox`, `News`, `Lessons` 중 하나만 사용한다.
- `tags`: 기본 1-3개만 사용한다.
- `captured_at`: ISO-8601 타임스탬프를 넣는다.
- `source`: 선택 필드다. 넣는다면 URL만 허용한다.
- `entities`: 반복 추적 가치가 있는 회사, 제품, 모델, 주제를 plain text로 남긴다.
- `related`: 기존 저장 항목과 직접 연결이 필요할 때만 넣고, 값은 Obsidian wiki-link 형식으로 넣는다.

## 본문 구조

frontmatter 아래 본문은 바로 `## Content`부터 시작한다. 제목과 description은 본문에서 반복하지 않는다.

### 공통 본문 템플릿

```md
## Content

{핵심 맥락, 변화, 의미, 비교 포인트}
```

### `Inbox` 추가 섹션

```md
## Content

{현재까지 파악한 맥락}

## Open Questions

- {아직 모르는 점}
- {나중에 확인할 점}

## Related

- [[{related-note}]]
```

### `Lessons` 추가 섹션

```md
## Content

{원본 signal들에서 공통적으로 보이는 패턴과 맥락}

## Takeaway

{재사용 가능한 교훈 한 줄 또는 짧은 문단}

## Implication

{앞으로 더 볼 것, 써볼 것, 무시할 것, 추적할 것}

## Related

- [[{related-note}]]
```

`## Related`는 관련 노트가 있을 때만 추가한다.

## 태그 전략

태그는 영어만 사용하고, 가능한 한 1-3개로 제한한다.

허용하는 태그 계층은 아래 세 가지뿐이다.

- `area/*`
- `signal/*`
- `entity/*`

시작 controlled vocabulary는 아래로 고정한다.

- `area/model`
- `area/agent`
- `area/coding`
- `area/image`
- `area/video`
- `area/search`
- `area/product`
- `area/infra`
- `area/research`
- `area/workflow`
- `signal/announcement`
- `signal/launch`
- `signal/update`
- `signal/benchmark`
- `signal/thread`
- `signal/writeup`

태그 선택 우선순위:

1. 첫 번째 태그는 반드시 `area/*`
2. 두 번째 태그는 필요하면 `signal/*`
3. 세 번째 태그는 정말 필요할 때만 `entity/*`

태그 재사용 규칙:

- 먼저 `obsidian vault="$OBSIDIAN_VAULT" tags counts`로 기존 태그를 확인한다.
- 의미가 같으면 기존 태그를 무조건 재사용한다.
- 동의어, 복수형, 날짜형, 감정형 태그는 만들지 않는다.
- 새 태그는 현재 어휘로 회수가 불가능하고, 앞으로 반복될 가능성이 높을 때만 허용한다.

## entity 태그 규칙

`entity/*`는 가장 쉽게 늘어나는 태그이므로 더 엄격하게 다룬다.

원칙:

- 반복 추적 가치가 확인된 회사, 제품, 모델에만 사용한다.
- 첫 등장 항목에서는 entity 태그를 생략할 수 있다.
- 처음부터 모든 제품명과 툴명을 entity 태그로 만들지 않는다.
- 가능하면 회사 수준 entity를 먼저 선호한다.
- 제품명과 모델명은 우선 `title`, `description`, `entities`, 본문으로 처리한다.
- 정말 반복적으로 다시 찾는 대상일 때만 entity 태그로 승격한다.

권장 예:

- `entity/openai`
- `entity/anthropic`
- `entity/google`

비권장 예:

- 처음 본 작은 툴 링크마다 새 `entity/*` 태그 만들기
- 제품명과 모델명을 모두 태그로 만들기
- 반복 추적 가치가 확인되지 않았는데도 entity 태그를 남발하기

## 예시

### 예시 1: X에서 본 모델 업데이트를 `News`로 저장

```md
---
title: "OpenAI reasoning model update"
description: "This matters because it may change how I judge current coding and agent workflows."
category: "News"
tags:
  - area/model
  - signal/update
captured_at: "2026-03-13T10:30:00+09:00"
source: "https://x.com/example/status/123"
entities:
  - "OpenAI"
---

## Content

OpenAI 관련 모델 업데이트를 짧게 포착한 링크다. 핵심은 모델 성능이나 활용 기대치에 변화가 있을 수 있다는 점이다. 나중에 다시 볼 이유는 코딩과 에이전트 작업 품질을 판단하는 기준이 바뀌는지 보기 위해서다.
```

### 예시 2: LinkedIn에서 본 제품 출시를 `News`로 저장

```md
---
title: "Browser agent launch with approval-first workflow"
description: "This matters because it may signal where browser-native AI products are converging."
category: "News"
tags:
  - area/product
  - signal/launch
captured_at: "2026-03-13T11:00:00+09:00"
source: "https://www.linkedin.com/posts/example"
entities:
  - "Browser agent"
---

## Content

브라우저 기반 에이전트 제품 출시 링크다. 원본 signal은 제품 출시지만, 이 항목은 `News`로 보관한다. 나중에 다시 볼 이유는 유사 제품군의 UX와 포지셔닝 패턴을 비교하기 위해서다.
```

### 예시 3: 맥락 부족한 스레드를 `Inbox`로 저장

```md
---
title: "Anthropic thread on tool-use evaluation ideas"
description: "This matters because it may contain evaluation ideas worth revisiting once the context is clearer."
category: "Inbox"
tags:
  - area/agent
  - signal/thread
captured_at: "2026-03-13T12:30:00+09:00"
source: "https://threads.net/@example/post/abc"
entities:
  - "Anthropic"
---

## Content

툴 사용 평가에 관한 스레드로 보이지만, 현재는 맥락이 부족하다. 저장 가치는 있지만 핵심 주장과 적용 가능성은 아직 정리되지 않았다.

## Open Questions

- 어떤 평가 프레임을 말하는가?
- 실제 제품 또는 모델 평가에 바로 적용할 수 있는가?
```

### 예시 4: 여러 `News`에서 교훈을 뽑아 `Lessons`로 승격

```md
---
title: "Browser agents need approval-first design"
description: "This matters because trust and control may be a better lens than autonomy for judging browser-native AI products."
category: "Lessons"
tags:
  - area/workflow
  - signal/launch
captured_at: "2026-03-13T13:20:00+09:00"
related:
  - "[[News/2026-03-13-browser-agent-launch]]"
  - "[[News/2026-03-12-web-automation-agent-release]]"
entities:
  - "Browser agents"
---

## Content

여러 브라우저 에이전트 출시를 보다 보니 공통된 UX 패턴이 보였다. 원본 링크는 각각 `News`에 남기고, 여기서는 상위 해석만 따로 저장한다.

## Takeaway

브라우저 에이전트는 "얼마나 자율적인가"보다 "얼마나 통제 가능하게 느껴지는가"가 더 중요하다.

## Implication

앞으로 이 카테고리 제품을 볼 때 승인 UX와 신뢰 설계를 핵심 비교 축으로 본다.

## Related

- [[News/2026-03-13-browser-agent-launch]]
- [[News/2026-03-12-web-automation-agent-release]]
```

## 실패 사례와 안티패턴

다음을 피한다.

- 질문 없이 바로 저장하기
- 질문만 하고 초안을 제안하지 않기
- 사용자의 원문을 거의 그대로 저장하기
- 외부 signal을 쓸데없이 여러 카테고리로 쪼개기
- 원본 `News` 없이 곧바로 `Lessons`만 남기기
- 첫 등장한 제품명마다 새 `entity/*` 태그를 만들기
- `related`에 path 문자열을 넣기
- URL이 아닌 값을 `source`에 넣기
- 본문 첫 줄에 제목과 description을 다시 반복하기
