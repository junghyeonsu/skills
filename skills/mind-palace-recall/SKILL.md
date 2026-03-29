---
name: mind-palace-recall
description: Obsidian vault의 MindPalace 폴더에 저장된 교훈, 인사이트, 원칙을 대화 맥락에 맞게 검색하고 활용하는 스킬. 사용자가 의사결정을 하고 있거나, 이전에 겪었던 문제와 비슷한 상황을 다루고 있거나, 과거에 정리해둔 지식이 도움이 될 만한 맥락이 보일 때 사용한다. 구체적으로는 코드 리뷰, 일정 추정, API 설계, 디버깅, 팀 커뮤니케이션, 프로젝트 계획, 기술 선택, 에러 처리, 리팩토링, 협업 프로세스 등에 대해 이전에 저장한 레슨런이 있을 수 있다. `/mind-palace-recall`로 직접 호출하거나, `/mind-palace-recall 키워드`로 특정 주제를 검색할 수 있다. "예전에 이거 관련해서 뭔가 정리해뒀는데", "이전에 배운 거 있었는데", "관련 레슨런 있어?", "저번에 이거 어떻게 했더라", "이전에 비슷한 실수 했었는데" 같은 표현에도 반응한다. 또한, 사용자가 명시적으로 요청하지 않더라도, 대화에서 일정 계획, 기술적 의사결정, 설계 논의, 코드 리뷰, 디버깅, 커뮤니케이션 전략 같은 주제가 나올 때 이 스킬을 사용해서 관련 지식이 있는지 확인하면 더 나은 조언을 할 수 있다.
---

# Mind Palace Recall

## 목적

Obsidian vault에 축적된 mind-palace 지식을 대화에 적재적소로 불러와서, 같은 실수를 반복하지 않고 과거의 교훈과 원칙을 실제 행동에 반영하도록 돕는다.

## 아키텍처: 트리거링과 검색의 이해

Claude는 스킬을 단계적으로 로딩한다.

1. **1단계 (항상)**: name + description만 본다. 이것만으로 이 스킬을 호출할지 결정한다.
2. **2단계 (호출 시)**: SKILL.md 전체를 읽는다. 검색 전략과 태그 매핑을 알게 된다.
3. **3단계 (검색)**: Obsidian CLI로 vault를 검색한다. 태그(mp/*), entities, 키워드를 사용한다.

이 구조가 recall의 설계에 미치는 영향:

- **description이 너무 좁으면** 사용자가 관련 주제를 다루고 있어도 스킬이 호출되지 않는다. 저장해둔 지식이 있어도 무용지물이 된다.
- **description이 너무 넓으면** 무관한 대화에서도 매번 vault를 검색하게 되어 노이즈가 된다.
- **태그(`mp/*`)가 검색의 핵심이다.** 대화 주제를 태그로 매핑하면 vault에서 관련 노트만 빠르게 찾을 수 있다.

그래서 이 스킬의 description에는 mind-palace에서 사용하는 태그 영역(engineering, communication, decision, planning, debugging, design, productivity, career, collaboration, learning, writing, review)과 대응하는 구체적인 상황들을 나열해두었다. 이것이 1단계 트리거링의 정확도를 높인다.

## 동작 모드

### 자동 모드 (proactive)

대화 맥락에서 mind-palace 지식이 도움이 될 수 있는 주제가 감지되면 자동으로 검색한다.

자동 검색이 의미 있는 상황:

- 사용자가 일정을 짜고 있다 → `mp/planning` 태그로 관련 교훈 검색
- 사용자가 기술 선택을 고민하고 있다 → `mp/decision` 태그로 관련 원칙 검색
- 사용자가 코드 리뷰를 하고 있다 → `mp/review` + `mp/engineering` 태그로 검색
- 사용자가 팀 커뮤니케이션 문제를 다루고 있다 → `mp/communication` 태그로 검색
- 사용자가 디버깅을 하고 있다 → `mp/debugging` 태그로 검색
- 사용자가 API를 설계하고 있다 → `mp/engineering` + entities 검색

자동 모드의 현실적 제약:

- 이 모드는 Claude가 description을 읽고 "이 대화에서 mind-palace 지식이 도움이 될 수 있겠다"고 판단할 때만 작동한다.
- 모든 대화에서 자동으로 발동하는 것이 아니다. description에 나열된 상황 패턴과 대화 맥락이 매칭될 때만 트리거된다.
- 트리거가 되면 vault를 한 번 검색하고, 관련 있는 노트가 있을 때만 자연스럽게 언급한다.
- 관련 노트가 없거나 관련성이 낮으면 아무 말도 하지 않는다.

### 수동 모드 (explicit)

사용자가 직접 호출한다.

**`/mind-palace-recall`** (키워드 없이):

1. 현재 대화의 주제에서 키워드를 추출한다.
2. 태그와 키워드를 조합해서 관련 노트를 검색한다.
3. 관련 노트를 카테고리별로 정리해서 보여준다.

**`/mind-palace-recall 키워드`** (키워드와 함께):

1. 해당 키워드로 직접 검색한다.
2. 태그, entities, 제목, 본문을 모두 대상으로 검색한다.
3. 검색 결과를 관련도 순으로 보여준다.

## 검색 전략: 태그를 인덱스로 활용

검색의 핵심은 대화 주제를 `mp/*` 태그로 매핑하는 것이다. 이 매핑이 정확할수록 관련 노트를 빠르게 찾을 수 있다.

### 주제 → 태그 매핑 테이블

| 대화 주제 | 1차 태그 | 2차 태그 (선택) |
|---|---|---|
| 코드 구현, 리팩토링, 아키텍처 | `mp/engineering` | |
| 팀 소통, 피드백, 설득 | `mp/communication` | |
| 기술 선택, 방향 결정 | `mp/decision` | |
| 일정, 리소스, 스프린트 | `mp/planning` | |
| 버그 추적, 에러 분석 | `mp/debugging` | |
| UX, UI, 시각적 결정 | `mp/design` | |
| 워크플로우, 도구, 자동화 | `mp/productivity` | |
| 성장, 면접, 역할 | `mp/career` | |
| 팀워크, 프로세스, 역할 분담 | `mp/collaboration` | |
| 새로운 기술, 학습 방법 | `mp/learning` | |
| 문서, 블로그, 기술 글쓰기 | `mp/writing` | |
| 코드 리뷰, PR, 품질 체크 | `mp/review` | |

### Obsidian CLI 사용법

Obsidian 공식 CLI를 사용한다. macOS 기준 경로는 `/Applications/Obsidian.app/Contents/MacOS/Obsidian`이다. vault 이름은 `mind palace`이다.

### 검색 절차

```sh
# 1단계: 키워드로 vault 전체 검색
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" search query="<키워드>"

# 2단계: 특정 카테고리 폴더 내 검색
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" search query="<키워드>" path="Principles/"

# 3단계: 검색 결과 노트 읽기
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="<검색된-파일-경로>"

# 태그 현황 확인
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" tags counts

# 특정 태그 상세 (태그가 붙은 파일 목록)
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" tag name="mp/<태그명>" verbose
```

검색 우선순위:

1. 먼저 매핑된 태그(`mp/*`)로 검색한다 — 가장 빠르고 정확하다.
2. 태그 검색 결과가 없으면 키워드로 전문 검색한다.
3. entities 필드에 해당 키워드가 있는 노트도 함께 찾는다.
4. 필요하면 유사어나 상위 개념으로 한 번 더 검색한다.

### 검색 결과 관련도 판단

검색 결과가 여러 개일 때 관련도 순서:

1. **Principles** — 검증된 행동 원칙은 가장 직접적으로 적용 가능
2. **Lessons** — 구체적 경험에서 나온 교훈은 비슷한 상황에서 유용
3. **Insights** — 관점이나 이해는 판단의 배경으로 참고
4. **Inbox** — 아직 정리 안 된 항목은 참고만

## 검색 결과 제시 방법

### 자동 모드일 때

대화 흐름을 끊지 않는 것이 핵심이다.

좋은 예:

> "참고로, 이전에 비슷한 상황에서 '일정 추정 시 코드 리뷰 시간을 별도로 잡아야 한다'는 교훈을 남기셨어요. 이번에도 리뷰 시간을 따로 잡아두는 게 좋을 것 같습니다."

> "이전에 '불확실할 때는 가장 되돌리기 쉬운 방향을 택한다'는 원칙을 정리하신 적 있는데, 이번 DB 스키마 결정에 적용해볼 만합니다."

나쁜 예:

> "MindPalace에서 검색한 결과 다음 노트를 찾았습니다: [파일 경로]. frontmatter는 다음과 같습니다..."

원칙:

- 파일 경로나 frontmatter를 직접 보여주지 않는다.
- 교훈의 핵심 내용을 자연어로 전달한다.
- 관련 노트가 여러 개면 가장 관련도 높은 1-2개만 언급한다.
- 사용자가 더 보고 싶어하면 그때 상세 내용을 보여준다.

### 수동 모드일 때

구조화된 요약을 제시한다.

```
관련 지식을 찾았습니다:

**Principles**
- "불확실할 때는 가장 되돌리기 쉬운 방향을 택한다"
  → DB 스키마나 public API 같은 되돌리기 어려운 결정에는 시간을 쓰기

**Lessons**
- "일정 추정 시 코드 리뷰 시간을 별도로 잡아야 한다"
  → 다음에는 스프린트 플래닝 때 리뷰 시간을 별도 항목으로 추가

**Insights**
- "좋은 에러 메시지는 사용자의 다음 행동을 알려준다"
  → 에러 메시지를 쓸 때 '그래서 뭘 하라고?'를 먼저 넣기
```

검색 결과가 없을 때:

- "관련된 기존 지식이 아직 없네요. 이번 대화에서 배운 게 있으면 `/mind-palace`로 저장해둘 수 있어요."

## 다른 스킬과의 관계

mind-palace-recall은 `mind palace` vault 전체를 검색한다. 이 vault에는 여러 스킬이 같은 카테고리 폴더(`Lessons/`, `Insights/`, `Principles/`, `Decisions/`, `Links/`, `Inbox/`)에 노트를 저장하되, 도메인은 태그로 구분한다:

- `mp/*` 태그 — mind-palace 스킬이 저장한 범용 지식
- `ds/*` 태그 — obsidian-design-system-knowledge 스킬이 저장한 디자인 시스템 지식
- `ai/*` 태그 — obsidian-ai-archive 스킬이 저장한 AI 아카이브

vault 전체를 검색하면 모든 도메인의 지식이 함께 나온다. 태그로 필터링하면 특정 도메인만 볼 수 있다.

## 실패 사례와 안티패턴

다음을 피한다.

- 매 턴마다 vault를 검색하기 (새로운 주제나 의사결정 맥락이 나올 때만)
- 관련성 낮은 노트를 억지로 끼워 넣기
- 파일 경로나 frontmatter를 사용자에게 그대로 보여주기
- 검색 결과를 전체 노트 내용으로 장황하게 인용하기
- 사용자가 관심 없는 과거 지식을 반복적으로 언급하기
- vault가 비어있거나 CLI가 동작하지 않을 때 에러를 장황하게 설명하기
- 태그 매핑 없이 키워드만으로 검색하기 (태그가 1차 필터, 키워드가 2차 필터)
