---
name: mind-palace
description: 대화 중 얻은 범용 지식, 교훈, 인사이트를 Obsidian vault에 구조적으로 저장하는 스킬. 디자인시스템이나 AI 아카이브 같은 특정 도메인에 한정되지 않고, 엔지니어링, 커뮤니케이션, 의사결정, 생산성, 커리어, 디버깅, 설계, 협업, 글쓰기, 학습 등 모든 주제의 lesson learned를 축적한다. `/mind-palace`만 호출하면 현재 세션의 맥락을 자동 분석해서 저장할 만한 내용을 찾아내고, `/mind-palace 키워드`로 호출하면 해당 키워드에 대한 지식을 정리해서 저장한다. "저장해줘", "기억해둬", "레슨런 남겨줘", "나중에 참고할 수 있게 정리해줘", "이거 옵시디언에 남겨둬", "이거 기록해둬" 같은 표현이 나올 때, 또는 대화 중 재사용 가능한 교훈이나 원칙이 드러날 때 사용한다. 저장된 지식은 mind-palace-recall 스킬이 나중에 검색해서 활용한다.
---

# Mind Palace

## 목적

대화에서 얻은 지식과 교훈을 Obsidian vault에 장기적으로 축적한다. 특정 도메인에 한정하지 않는다.

- Obsidian 공식 CLI를 사용한다.
- vault 이름은 `mind palace`이다.
- 저장 카테고리는 `Inbox`, `Lessons`, `Insights`, `Principles` 네 가지이며, vault 최상위 폴더로 존재한다.
- 도메인 구분은 폴더가 아니라 태그(`mp/*`, `ds/*` 등)로 한다.
- 사용자의 원문을 그대로 저장하지 말고, 질문과 재구성을 통해 검색 가능한 지식으로 바꿔 저장한다.
- 질문 후에는 반드시 저장 초안을 먼저 제안한다.
- 태그는 적게 쓰고 강하게 재사용한다.

## 아키텍처: 저장과 검색의 관계

이 스킬은 지식을 **저장**하는 역할을 맡는다. 저장된 지식을 **검색해서 활용**하는 역할은 `mind-palace-recall` 스킬이 맡는다.

Claude는 스킬을 처음부터 전부 읽지 않는다. 먼저 name과 description만 보고, 관련 있다고 판단할 때 SKILL.md 전체를 읽는다. 이 구조 때문에:

- **description은 트리거다.** 사용자가 어떤 말을 했을 때 이 스킬이 호출될지가 description에 달려 있다.
- **태그는 검색 인덱스다.** `mp/*`는 범용 지식, `ds/*`는 디자인 시스템 등 도메인별 접두사로 구분한다. recall 스킬이 태그를 통해 관련 지식을 찾으므로 일관성이 중요하다.
- **entities는 세부 검색어다.** 태그로 넓게 잡고, entities로 좁힌다.
- **title과 description은 사람과 AI 모두를 위한 요약이다.** recall이 전체 노트를 읽지 않고도 관련성을 판단할 수 있어야 한다.

이 관계를 이해하면, 저장할 때 "나중에 어떻게 찾을 것인가"를 항상 염두에 두게 된다. 태그를 대충 붙이면 나중에 recall이 못 찾고, title이 모호하면 recall이 관련성을 판단 못 한다.

## 두 가지 호출 모드

### 모드 1: 키워드 없이 호출 (`/mind-palace`)

현재 세션의 대화 맥락 전체를 분석한다.

1. 대화에서 재사용 가능한 교훈, 실수에서 배운 점, 의사결정 근거, 반복할 만한 패턴, 앞으로 기억해야 할 원칙을 찾는다.
2. 저장 가치가 있는 항목을 1-3개 정리해서 제안한다.
3. 항목마다 카테고리를 분류하고 후속 질문(2-4개)을 한다.
4. 질문 답변을 바탕으로 저장 초안을 제안한다.
5. 사용자가 승인하면 저장한다.

단순 잡담이나 이미 다른 스킬로 저장된 내용은 제외한다.

### 모드 2: 키워드와 함께 호출 (`/mind-palace 키워드`)

키워드에 해당하는 주제로 범위를 좁힌다.

1. 현재 세션에서 해당 키워드와 관련된 맥락을 추출한다.
2. 해당 주제에 대한 후속 질문(2-4개)을 한다.
3. 질문 답변을 바탕으로 저장 초안을 제안한다.
4. 사용자가 승인하면 저장한다.

## 실행 절차

다음 순서를 따른다.

1. 호출 모드에 따라 저장할 지식을 감지하거나 키워드 범위로 좁힌다.
2. `Inbox`, `Lessons`, `Insights`, `Principles` 중 하나로 분류한다.
3. 바로 저장하지 말고 2-4개의 짧은 후속 질문으로 핵심을 보강한다.
4. 질문 답변을 바탕으로 저장 초안을 만든다.
5. 초안에는 최소한 `category`, `title`, `description`, `tags`를 넣는다.
6. 사용자가 수정하거나 승인하면 그때 저장한다.
7. 저장 직전에 기존 노트 제목, 유사 표현, 기존 태그를 확인한다.
8. 새 노트를 만들거나, 같은 항목의 후속 정보면 기존 노트에 덧붙인다.

질문만 하고 끝내지 않는다. 질문 후에는 반드시 저장 초안을 먼저 제안한다.

## Obsidian CLI 사용법

Obsidian 공식 CLI를 사용한다. macOS 기준 경로는 `/Applications/Obsidian.app/Contents/MacOS/Obsidian`이다. vault 이름은 `mind palace`이다.

### 중복 확인 (저장 전 필수)

```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" search query="<핵심어>"
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" tags counts
```

### 노트 생성

`content`에서 줄바꿈은 `\n`, 탭은 `\t`를 사용한다.

```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" create path="<Category>/<file-name>.md" content="<note-content>"
```

### 노트 읽기

```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="<Category>/<file-name>.md"
```

### 노트에 내용 추가

```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" append path="<Category>/<file-name>.md" content="<additional-content>"
```

### 노트 삭제

```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" delete path="<Category>/<file-name>.md"
```

CLI가 동작하지 않으면 Obsidian 앱 버전이 1.12 이상인지 확인하고 저장을 보류한다.

## 카테고리 선택 규칙

### `Inbox`

아직 정리가 덜 된 상태지만 나중에 다시 꺼내볼 가치가 있는 항목에 사용한다.

예:

- 흥미로운 접근법이 나왔지만 검증이 안 됨
- 누군가의 조언을 들었는데 아직 소화가 안 됨
- 대화 중 떠오른 아이디어인데 정리할 시간이 없음

운영 규칙:

- `Inbox`는 영구 보관소가 아니다.
- 맥락이 보강되면 `Lessons`, `Insights`, 또는 `Principles`로 재분류한다.

### `Lessons`

실제로 경험한 일에서 재사용 가능한 교훈이 나온 항목에 사용한다. "다음에는 이렇게 하겠다"가 핵심이다.

예:

- 코드 리뷰에서 반복적으로 놓치는 패턴을 발견함
- 프로젝트 일정 추정에서 매번 빠뜨리는 요소가 있었음
- 특정 접근법을 시도했다가 실패한 이유를 알게 됨
- 커뮤니케이션에서 효과적이었던 방식을 찾음

### `Insights`

경험이나 정보를 종합해서 나온 이해, 관점, 패턴 인식에 사용한다. Lessons가 "다음에 뭘 하겠다"라면, Insights는 "이제 이걸 이렇게 이해한다"에 가깝다.

예:

- 여러 번의 코드 리뷰 경험에서 공통적으로 보이는 설계 원리를 발견함
- 팀 역학에 대해 새로운 관점이 생김
- 기술 선택의 트레이드오프에 대한 이해가 깊어짐

### `Principles`

반복적으로 적용 가능한 행동 원칙이나 기준에 사용한다. 충분히 검증되어서 규칙처럼 적용할 수 있는 것들이다.

예:

- "API 설계 시 항상 backward compatibility를 먼저 확인한다"
- "피드백을 줄 때 구체적인 예시를 반드시 포함한다"
- "불확실할 때는 작게 시작해서 빠르게 검증한다"

결론이 아직 없으면 `Principles`가 아니라 `Inbox` 또는 `Lessons`에 둔다.

## 후속 질문 전략

질문은 짧고 구체적으로 유지한다.

- 한 질문에는 한 가지 사실만 묻는다.
- 이미 대화에서 확정된 내용은 다시 묻지 않는다.
- 최소한 `무엇`, `왜 중요한지`, `나중에 어떻게 찾을지`가 채워지게 묻는다.
- 질문 수는 보통 2-4개로 제한한다.

### `Inbox` 질문

- 이 아이디어의 핵심은 뭔가요?
- 나중에 다시 꺼내볼 때 어떤 상황에서 유용할까요?
- 아직 빠진 맥락이 있나요?

### `Lessons` 질문

- 어떤 상황에서 이걸 배웠나요?
- 핵심 교훈은 뭔가요?
- 다음에는 무엇을 다르게 하실 건가요?

### `Insights` 질문

- 어떤 경험들이 이 이해로 이어졌나요?
- 이전에는 어떻게 생각했는데 바뀐 건가요?
- 이 관점이 앞으로 어떤 판단에 영향을 줄까요?

### `Principles` 질문

- 이 원칙을 만들게 된 경험은 뭔가요?
- 이 원칙이 적용되지 않는 예외가 있나요?
- 구체적으로 어떤 상황에서 이 원칙을 적용하나요?

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

- category: Lessons
- title: "일정 추정 시 코드 리뷰 시간을 별도로 잡아야 한다"
- description: "프로젝트 일정을 잡을 때 코드 리뷰와 피드백 반영 시간을 빠뜨려서 매번 일정이 밀렸던 교훈이다."
- tags:
  - mp/engineering
  - mp/planning
- entities:
  - 일정 추정
  - 코드 리뷰
```

사용자가 수정하거나 승인하면 저장한다.

## 파일명 규칙

파일명은 slug로 유지하고, 제목은 사람이 읽기 쉽게 쓴다.

- 파일명 패턴: `YYYY-MM-DD-short-searchable-title.md`
- 파일명은 소문자와 하이픈만 사용한다.
- 카테고리명은 경로로만 표현하고 파일명에 반복하지 않는다.
- 제목은 파일명과 같게 쓰지 않는다. 제목은 사람 친화적으로, 파일명은 검색과 정렬 친화적으로 유지한다.

좋은 조합:

- `title: "일정 추정 시 코드 리뷰 시간을 별도로 잡아야 한다"`
- `path: "Lessons/2026-03-30-schedule-estimation-code-review.md"`

## 노트 포맷

필수 frontmatter는 아래 다섯 필드를 정확히 유지한다.

```yaml
---
title: "<human-readable sentence-style title>"
description: "<one-sentence why it matters>"
category: "<Inbox|Lessons|Insights|Principles>"
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

- `title`: 사람도 읽기 쉽고 검색도 가능한 제목을 쓴다. 한국어와 영어를 자연스럽게 섞어도 된다.
- `description`: 1-2문장으로 "무엇에 대한 지식인가"와 "어떤 상황에서 다시 찾게 될지"를 모두 담는다. recall이 title과 description만 보고 관련성을 판단하므로, 구체적인 대상어와 검색 맥락을 포함한다.
- `category`: `Inbox`, `Lessons`, `Insights`, `Principles` 중 하나만 사용한다.
- `tags`: 1-3개만 사용한다.
- `captured_at`: ISO-8601 타임스탬프를 넣는다.
- `source`: 선택 필드다. 넣는다면 URL만 허용한다.
- `entities`: 태그로 만들지 않을 대상어를 1-3개까지 넣는다.
- `related`: 관련 노트가 있을 때만 넣고, 값은 Obsidian wiki-link 형식으로 넣는다.

## 본문 구조

frontmatter 아래 본문은 바로 `## Content`부터 시작한다. 제목과 description은 본문에서 반복하지 않는다.

### `Inbox` 본문 템플릿

```md
## Content

{아직 정리가 덜 된 핵심 아이디어나 맥락}

## Open Questions

- {아직 모르는 점}
- {나중에 확인할 점}

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

### `Insights` 본문 템플릿

```md
## Content

{관찰이나 경험에서 도출한 이해}

## Shift

{이전 생각 → 바뀐 생각}

## Implication

{이 이해가 앞으로 어떤 판단에 영향을 줄지}

## Related

- [[{related-note}]]
```

### `Principles` 본문 템플릿

```md
## Content

{원칙의 내용과 배경}

## When to Apply

{어떤 상황에서 이 원칙을 적용하는지}

## Exceptions

{이 원칙이 적용되지 않는 경우}

## Related

- [[{related-note}]]
```

`## Related`는 관련 노트가 있을 때만 추가한다.

## 태깅 전략

태그는 recall을 위한 **검색 인덱스**다. 단순 분류가 아니라, 나중에 `mind-palace-recall`이 관련 지식을 빠르게 찾기 위한 통로다.

태그 설계의 핵심 원리:

- 태그는 "이 지식을 나중에 어떤 맥락에서 다시 찾을 것인가"를 기준으로 붙인다.
- `mp/*` 태그는 recall 스킬이 대화 주제를 태그로 매핑해서 검색하는 첫 번째 필터다.
- 태그가 일관적이지 않으면 recall이 관련 지식을 놓친다. 그래서 controlled vocabulary가 중요하다.
- entities는 태그보다 구체적인 두 번째 필터다. "mp/engineering으로 좁히고, entities에서 '코드 리뷰'로 한 번 더 좁힌다"는 식이다.

운영 규칙:

- 모든 태그는 `mp/` 접두사로 시작한다. (mind-palace의 약자)
- 기본은 2개, 최대 3개까지만 사용한다.
- 새 태그를 만들기 전에 기존 태그를 먼저 재사용할 수 있는지 확인한다.
- 구체적인 기술 이름이나 도구 이름은 태그로 만들지 않는다. 그건 entities가 맡는다.
- 태그보다 제목, description, entities의 품질을 우선한다.

### 시작 controlled vocabulary

- `mp/engineering`
- `mp/communication`
- `mp/decision`
- `mp/planning`
- `mp/debugging`
- `mp/design`
- `mp/productivity`
- `mp/career`
- `mp/collaboration`
- `mp/learning`
- `mp/writing`
- `mp/review`

### 태그 선택 우선순위

첫 태그는 "어떤 영역의 지식인가"를 표현한다.

- 예: `mp/engineering`, `mp/communication`, `mp/design`

두 번째 태그는 "어떤 활동에서 나온 지식인가"를 표현한다.

- 예: `mp/debugging`, `mp/review`, `mp/planning`

세 번째 태그는 특수 맥락이 꼭 필요할 때만 사용한다.

### 경합 규칙

- `mp/engineering` vs `mp/design`: 코드나 구현이 핵심이면 engineering, 사용자 경험이나 시각적 결정이 핵심이면 design
- `mp/planning` vs `mp/decision`: 일정이나 리소스 배분이면 planning, 기술적/전략적 선택이면 decision
- `mp/communication` vs `mp/collaboration`: 메시지 전달이나 설득이면 communication, 팀 워크 프로세스면 collaboration

## 예시

### 예시 1: Lessons 저장

```md
---
title: "일정 추정 시 코드 리뷰 시간을 별도로 잡아야 한다"
description: "프로젝트 일정을 잡을 때 코드 리뷰와 피드백 반영 시간을 빠뜨려서 매번 일정이 밀렸던 교훈이다."
category: "Lessons"
tags:
  - mp/engineering
  - mp/planning
captured_at: "2026-03-30T10:00:00+09:00"
entities:
  - "일정 추정"
  - "코드 리뷰"
---

## Content

최근 3번의 스프린트에서 구현은 예정대로 끝났지만 코드 리뷰와 피드백 반영 시간을 빠뜨려 매번 1-2일씩 밀렸다. 리뷰 라운드가 최소 2회 필요한 경우가 대부분이었다.

## Takeaway

일정에 구현 외에 리뷰 2라운드 + 피드백 반영 시간을 기본으로 잡아야 한다.

## Next Time

스프린트 플래닝 때 각 태스크에 리뷰 시간을 별도 항목으로 추가한다.
```

### 예시 2: Insights 저장

```md
---
title: "좋은 에러 메시지는 사용자의 다음 행동을 알려준다"
description: "에러 메시지를 개선하면서 '무엇이 잘못됐는지'보다 '다음에 뭘 해야 하는지'가 더 중요하다는 걸 깨달았다."
category: "Insights"
tags:
  - mp/engineering
  - mp/design
captured_at: "2026-03-30T11:00:00+09:00"
entities:
  - "에러 메시지"
  - "UX writing"
---

## Content

에러 메시지를 개선하는 작업을 하면서, 기술적으로 정확한 에러 원인을 보여주는 것보다 사용자가 다음에 취할 수 있는 구체적 행동을 알려주는 것이 지원 문의를 줄이는 데 훨씬 효과적이었다.

## Shift

이전: 에러 메시지는 기술적으로 정확해야 한다
이후: 에러 메시지는 다음 행동을 안내해야 한다 (정확성은 로그에)

## Implication

앞으로 에러 메시지를 쓸 때 "그래서 뭘 하라고?"를 항상 먼저 넣는다.
```

### 예시 3: Principles 저장

```md
---
title: "불확실할 때는 가장 되돌리기 쉬운 방향을 택한다"
description: "되돌리기 어려운 결정일수록 신중해야 하고, 되돌리기 쉬운 결정은 빠르게 해도 괜찮다는 원칙이다."
category: "Principles"
tags:
  - mp/decision
captured_at: "2026-03-30T12:00:00+09:00"
entities:
  - "의사결정"
  - "reversibility"
---

## Content

Amazon의 one-way door / two-way door 프레임워크에서 착안했지만, 실제 프로젝트에서 여러 번 적용해보니 효과적이었다. DB 스키마 변경이나 public API 설계 같은 되돌리기 어려운 결정에는 시간을 쓰고, 내부 구현 방식이나 도구 선택 같은 건 빠르게 결정해서 시도했다.

## When to Apply

기술적 또는 조직적 결정을 내려야 하는데 불확실성이 높을 때.

## Exceptions

시간 제약이 극단적으로 클 때는 되돌리기 비용과 상관없이 빠르게 결정해야 할 수도 있다.
```

## 실패 사례와 안티패턴

다음을 피한다.

- 질문 없이 바로 저장하기
- 질문만 하고 초안을 제안하지 않기
- 사용자의 원문을 거의 그대로 저장하기
- 파일명, frontmatter, 본문 구조를 매번 다르게 쓰기
- 태그 대신 구체적인 기술 이름을 남발하기
- `related`에 path 문자열을 넣기
- URL이 아닌 값을 `source`에 넣기
- 본문 첫 줄에 제목과 description을 다시 반복하기
- 디자인 시스템 전용 지식을 `mp/*` 태그로 저장하기 (그건 `ds/*` 태그로 obsidian-design-system-knowledge 스킬 사용)
- AI 뉴스나 외부 signal을 `mp/*` 태그로 저장하기 (그건 `ai/*` 태그로 obsidian-ai-archive 스킬 사용)
