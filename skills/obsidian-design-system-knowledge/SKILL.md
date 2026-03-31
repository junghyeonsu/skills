---
name: obsidian-design-system-knowledge
description: 로컬 Obsidian vault에 디자인 시스템 지식을 구조적으로 저장하는 스킬. Obsidian CLI를 사용해 디자인 시스템 관련 결정, 교훈, 참고 링크, 미해결 항목을 개별 노트로 축적한다. 사용자가 "저장해줘", "기억해줘", "Obsidian에 남겨줘"라고 하거나, 대화 중 컴포넌트 API 기준, 토큰 규칙, 문서 동기화 방식, 접근성 리뷰 교훈, 릴리스 회고, 마이그레이션 제약, 참고 문서 링크, 미해결 항목이 드러날 때 사용한다.
---

# Obsidian Design System Knowledge

## 목적

디자인 시스템 지식을 Obsidian vault에 장기적으로 축적한다.

- Obsidian 공식 CLI를 사용한다.
- vault 이름은 `mind palace`이다. 다른 스킬(mind-palace, obsidian-ai-archive)과 같은 vault를 공유한다.
- 저장 카테고리는 `Inbox`, `Lessons`, `Links`, `Decisions` 네 가지이며, vault 최상위 폴더로 존재한다.
- 도메인 구분은 폴더가 아니라 태그(`ds/*`)로 한다. 같은 `Lessons/` 폴더에 범용 지식(`mp/*`)과 디자인 시스템 지식(`ds/*`)이 함께 있지만 태그로 구분된다.
- 사용자의 원문을 그대로 저장하지 말고, 질문과 재구성을 통해 검색 가능한 지식으로 바꿔 저장한다.
- 질문 후에는 반드시 저장 초안을 먼저 제안한다.
- 태그는 적게 쓰고 강하게 재사용한다.
- 컴포넌트 이름이나 세부 대상어는 태그 대신 `entities`에 넣는다.

## 언제 이 스킬을 사용할지

다음 상황에서 이 스킬을 사용한다.

- 사용자가 디자인 시스템 관련 내용을 저장해달라고 요청할 때
- 대화 중 나중에 다시 참고할 가치가 있는 디자인 시스템 지식이 드러날 때
- 컴포넌트 API, 토큰 규칙, 문서 동기화 방식 같은 기준이 정리되었을 때
- 릴리스, QA, 접근성 리뷰, 마이그레이션 과정에서 재사용 가능한 교훈이 나왔을 때
- 참고 링크를 단순 URL이 아니라 "왜 중요한지"까지 함께 남겨야 할 때
- 아직 결론은 없지만 추적할 가치가 있는 미해결 항목이 생겼을 때

다음은 저장하지 않는다.

- 단순한 대화 로그
- 디자인 시스템과 무관한 일반 메모
- 같은 의미의 기존 노트가 이미 있는데 새 정보가 거의 없는 중복 항목
- 실행 중인 임시 잡담이나 방향 탐색 메모

## 실행 절차

다음 순서를 따른다.

1. 저장 가치가 있는 디자인 시스템 지식을 감지한다.
2. `Inbox`, `Lessons`, `Links`, `Decisions` 중 하나로 분류한다.
3. 바로 저장하지 말고 2-4개의 짧은 후속 질문으로 핵심을 보강한다.
4. 질문 답변을 바탕으로 저장 초안을 만든다.
5. 초안에는 최소한 `category`, `title`, `description`, `tags`를 넣는다.
6. 사용자가 수정하거나 승인하면 그때 저장한다.
7. 저장 직전에 기존 노트 제목, 유사 표현, 기존 태그를 확인한다.
8. 새 노트를 만들거나, 같은 항목의 후속 정보면 기존 노트에 덧붙인다.
9. 기존 `Inbox` 항목이 해결되었다면 새 `Decision` 또는 `Lesson`을 만들고 이전 `Inbox` 노트와 연결한다.

질문만 하고 끝내지 않는다. 질문 후에는 반드시 저장 초안을 먼저 제안한다.

## Obsidian CLI 사용법

Obsidian 공식 CLI를 사용한다. macOS 기준 경로는 `/Applications/Obsidian.app/Contents/MacOS/Obsidian`이다. vault 이름은 `mind palace`이다.

```sh
# 중복 확인 (저장 전 필수)
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" search query="<핵심어>"
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" tags counts

# 노트 생성 (content에서 줄바꿈은 \n)
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" create path="<Category>/<file-name>.md" content="<note-content>"

# 노트 읽기
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="<Category>/<file-name>.md"

# 노트에 내용 추가
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" append path="<Category>/<file-name>.md" content="<additional-content>"

# 노트 삭제
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" delete path="<Category>/<file-name>.md"
```

CLI가 동작하지 않으면 Obsidian 앱 버전이 1.12 이상인지 확인하고 저장을 보류한다.

## 카테고리 선택 규칙

### `Inbox`

아직 결론이 없고 후속 확인이나 액션이 필요한 항목에 사용한다.

예:

- 접근성 이슈는 확인되었지만 해결 기준이 아직 정해지지 않음
- 마이그레이션 리스크가 보이지만 영향 범위 검증이 남아 있음
- 체크리스트 보강이 필요하지만 어떤 조건을 표준화할지 정리되지 않음

### `Lessons`

실제로 있었던 일에서 재사용 가능한 교훈이나 다음 행동 원칙이 나온 항목에 사용한다.

예:

- 릴리스 중 토큰 회귀가 발생했고, 다음번 점검 방식이 달라져야 함
- 접근성 리뷰에서 반복되는 실수가 드러남
- 구현 과정에서 놓치기 쉬운 제약이 발견됨

### `Links`

문서, 스펙, 참고 자료 그 자체보다도 "왜 중요한지"와 "언제 다시 봐야 하는지"를 함께 남겨야 하는 항목에 사용한다.

예:

- 토큰 명세 문서
- 디자인 시스템 접근성 가이드
- 컴포넌트 API 기준 문서

### `Decisions`

무엇을 결정했는지와 왜 그렇게 결정했는지를 장기적으로 남겨야 하는 항목에 사용한다.

예:

- 컴포넌트 API 기준을 정함
- 토큰 이름 규칙을 바꿈
- 문서와 코드의 동기화 책임을 정함

결론이 아직 없으면 `Decisions`가 아니라 `Inbox`에 둔다.

## 후속 질문 전략

질문은 짧고 구체적으로 유지한다.

- 한 질문에는 한 가지 사실만 묻는다.
- 이미 대화에서 확정된 내용은 다시 묻지 않는다.
- 최소한 `무엇`, `왜`, `나중에 어떻게 찾을지`가 채워지게 묻는다.
- 질문 수는 보통 2-4개로 제한한다.

### `Inbox` 질문

- 아직 무엇이 미해결인가요?
- 왜 중요한가요?
- 다음 액션이나 확인 조건은 무엇인가요?

### `Lessons` 질문

- 무슨 일이 있었나요?
- 핵심 교훈은 무엇인가요?
- 다음에는 무엇을 다르게 해야 하나요?

### `Links` 질문

- 이 링크는 무엇에 대한 자료인가요?
- 왜 중요한가요?
- 어떤 상황에서 다시 봐야 하나요?

### `Decisions` 질문

- 무엇을 결정했나요?
- 왜 그렇게 결정했나요?
- 어떤 대안이나 트레이드오프가 중요했나요?

## 저장 초안 제안 규칙

질문 후에는 사용자의 원문을 그대로 저장하지 말고, 아래 항목을 먼저 구조화해서 제안한다.

- `category`
- `title`
- `description`
- `tags`

필요하면 아래도 함께 제안한다.

- `entities`
- `related`
- `source`

초안 제안 예:

```md
저장 초안

- category: Decisions
- title: "Button size token alignment decision"
- description: "버튼 size prop과 사이즈 토큰을 같은 기준으로 맞춘 이유와 제약을 다시 찾기 위한 결정이다."
- tags:
  - ds/token
  - ds/implementation
- entities:
  - button
  - size token
- related:
  - "[[Inbox/2026-03-11-button-size-token-alignment-open-question]]"
```

사용자가 수정하거나 승인하면 저장한다.

## 파일명 규칙

파일명은 slug로 유지하고, 제목은 사람이 읽기 쉽게 쓴다.

- 파일명 패턴: `YYYY-MM-DD-short-searchable-title.md`
- 파일명은 소문자와 하이픈만 사용한다.
- 카테고리명은 경로로만 표현하고 파일명에 반복하지 않는다.
- 제목은 파일명과 같게 쓰지 않는다. 제목은 사람 친화적으로, 파일명은 검색과 정렬 친화적으로 유지한다.

좋은 조합:

- `title: "Button size token alignment decision"`
- `path: "Decisions/2026-03-13-button-size-token-alignment.md"`

## 노트 포맷

필수 frontmatter는 아래 다섯 필드를 정확히 유지한다.

```yaml
---
title: "<human-readable sentence-style title>"
description: "<one-sentence why it matters>"
category: "<Inbox|Lessons|Links|Decisions>"
tags:
  - <tag-1>
  - <tag-2>
captured_at: "<ISO-8601 timestamp>"
---
```

선택 필드는 아래 세 개만 허용한다.

```yaml
source: "https://..."
entities:
  - "<searchable entity>"
related:
  - "[[Folder/Note Title]]"
```

필드 규칙:

- `title`: 사람도 읽기 쉽고 검색도 가능한 제목을 쓴다.
- `description`: 1-2문장으로 "무엇에 대한 지식인가"와 "어떤 상황에서 다시 찾게 될지"를 모두 담는다. recall이 title과 description만 보고 관련성을 판단하므로, 구체적인 대상어와 검색 맥락을 포함한다.
- `category`: `Inbox`, `Lessons`, `Links`, `Decisions` 중 하나만 사용한다.
- `tags`: 1-3개만 사용한다.
- `captured_at`: ISO-8601 타임스탬프를 넣는다.
- `source`: 선택 필드다. 넣는다면 URL만 허용한다.
- `entities`: 태그로 만들지 않을 대상어를 1-3개까지 넣는다.
- `related`: 관련 노트가 있을 때만 넣고, 값은 Obsidian wiki-link 형식으로 넣는다. 경로는 `MindPalace/DesignSystem/` 기준으로 쓴다.

`entities`는 태그를 더럽히지 않고 대상 검색성을 확보하기 위한 필드다.

예:

- `button`
- `size token`
- `focus ring`

## 본문 구조

frontmatter 아래 본문은 바로 `## Content`부터 시작한다. 제목과 description은 본문에서 반복하지 않는다.

### 공통 본문 템플릿

```md
## Content

{핵심 맥락, 근거, 설명}
```

### `Inbox` 본문 템플릿

```md
## Content

{아직 미해결인 내용과 현재까지 확인된 맥락}

## Open Questions

- {아직 모르는 점}
- {다음 확인 항목}

## Related

- [[{related-note}]]
```

### `Lessons` 본문 템플릿

```md
## Content

{실제 상황과 교훈이 나온 맥락}

## Takeaway

{재사용 가능한 교훈}

## Next Time

{다음번에 바꿀 행동이나 체크}

## Related

- [[{related-note}]]
```

### `Links` 본문 템플릿

```md
## Content

{자료 설명과 핵심 맥락}

## Why It Matters

{왜 중요한가}

## Revisit When

{다시 봐야 하는 시점이나 조건}

## Related

- [[{related-note}]]
```

### `Decisions` 본문 템플릿

```md
## Content

{결정 내용과 배경}

## Why

{결정 이유}

## Trade-offs

{대안, 포기한 것, 감수한 제약}

## Related

- [[{related-note}]]
```

`## Related`는 관련 노트가 있을 때만 추가한다.

## 태깅 전략

태그는 넓은 분류만 맡고, 대상어 검색은 `entities`가 맡는다.

- 모든 태그는 `ds/` 접두사로 시작한다.
- 기본은 2개, 최대 3개까지만 사용한다.
- 새 태그를 만들기 전에 기존 태그를 먼저 재사용할 수 있는지 확인한다.
- 컴포넌트 이름, 토큰 이름, 세부 대상어는 태그로 만들지 않는다.
- 태그보다 제목, description, entities의 품질을 우선한다.

### 시작 controlled vocabulary

- `ds/component`
- `ds/token`
- `ds/spec`
- `ds/release`
- `ds/docs`
- `ds/implementation`
- `ds/naming`
- `ds/review`
- `ds/a11y`
- `ds/migration`

### 태그 선택 우선순위

첫 태그는 "무엇에 대한 지식인가"를 표현한다.

- 예: `ds/token`, `ds/component`, `ds/docs`, `ds/a11y`

두 번째 태그는 "어떤 상황에서 나온 지식인가"를 표현한다.

- 예: `ds/implementation`, `ds/release`, `ds/review`, `ds/migration`

세 번째 태그는 특수 맥락이 꼭 필요할 때만 사용한다.

- 예: `ds/spec`, `ds/naming`

### 경합 규칙

- `ds/docs`: 문서 자체를 가리키는 참고 항목일 때 쓴다.
- `ds/spec`: 규범적 기준이나 명세 해석이 핵심일 때 쓴다.
- `ds/implementation`: 코드나 실제 동작 차이가 핵심일 때 쓴다.

예:

- 버튼 토큰 정렬 결정 -> `ds/token` + `ds/implementation`
- 릴리스 중 발견한 접근성 회귀 교훈 -> `ds/a11y` + `ds/release`
- 문서 기준 링크 -> `ds/docs` + `ds/spec`

## 예시

### 예시 1: 결정 저장

```md
---
title: "Button size token alignment decision"
description: "버튼 size prop과 사이즈 토큰을 같은 기준으로 맞춘 이유를 다시 찾기 위한 결정이다."
category: "Decisions"
tags:
  - ds/token
  - ds/implementation
captured_at: "2026-03-13T10:00:00+09:00"
entities:
  - "button"
  - "size token"
related:
  - "[[Inbox/2026-03-11-button-size-token-alignment-open-question]]"
---

## Content

버튼의 size prop이 토큰 스케일과 어긋나면 구현과 문서가 동시에 흔들린다. 이번 결정은 prop 이름과 토큰 기준을 같은 축으로 맞춘다.

## Why

구현 차이를 줄이고 문서, 코드, 디자인 사이의 기준 불일치를 막기 위해서다.

## Trade-offs

기존 이름과의 호환 비용이 생기지만 이후 유지보수 비용은 줄어든다.

## Related

- [[Inbox/2026-03-11-button-size-token-alignment-open-question]]
```

### 예시 2: 링크 저장

```md
---
title: "Accessibility checklist reference for component reviews"
description: "컴포넌트 리뷰 때 반복 확인해야 하는 접근성 기준을 빠르게 다시 찾기 위한 링크다."
category: "Links"
tags:
  - ds/docs
  - ds/a11y
captured_at: "2026-03-13T11:00:00+09:00"
source: "https://example.com/a11y-checklist"
entities:
  - "accessibility checklist"
---

## Content

컴포넌트 리뷰 시 반복해서 확인해야 하는 접근성 기준이 정리된 문서다.

## Why It Matters

릴리스 직전이 아니라 구현 중간에 빠르게 확인할 수 있어 회귀를 줄이는 데 도움이 된다.

## Revisit When

새 컴포넌트를 만들거나 기존 컴포넌트의 상호작용을 바꿀 때 다시 본다.
```

## 실패 사례와 안티패턴

다음을 피한다.

- 질문 없이 바로 저장하기
- 질문만 하고 초안을 제안하지 않기
- 사용자의 원문을 거의 그대로 저장하기
- 파일명, frontmatter, 본문 구조를 매번 다르게 쓰기
- 태그 대신 컴포넌트 이름을 남발하기
- `related`에 path 문자열을 넣기
- URL이 아닌 값을 `source`에 넣기
- 본문 첫 줄에 제목과 description을 다시 반복하기

