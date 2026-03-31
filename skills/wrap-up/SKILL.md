---
name: wrap-up
description: 세션 마무리 스킬. 대화가 끝나갈 때 `/wrap-up`을 호출하면 현재 세션의 대화 전체를 분석해서, 저장할 가치가 있는 지식을 4가지 목적지별로 추출하고 제안한다. (1) 개인 레슨런은 mind-palace 스킬 형식으로 Obsidian vault에 저장, (2) 디자인 시스템 관련 지식은 obsidian-design-system-knowledge 스킬 형식으로 Obsidian vault에 저장, (3) 레포 전체에서 매 세션마다 알면 좋은 정보는 CLAUDE.md(memory)에 추가, (4) 팀에 공유할 만한 레슨런이나 가이드는 해당 폴더의 AGENTS.md에 추가. 세션 마무리, 대화 정리, 오늘 배운 것 정리, "wrap up", "마무리", "정리하자", "오늘 세션 끝", "세션 정리", "배운 거 정리", "기록 남기자" 같은 표현이 나올 때 사용한다.
---

# Wrap-up

## 목적

세션이 끝날 때 대화에서 나온 지식을 놓치지 않고 적절한 곳에 저장하는 것이 이 스킬의 목적이다. 대화를 한 번 분석해서 4가지 목적지 중 저장할 내용이 있는 곳만 골라 제안하고, 사용자가 승인하면 실제로 저장한다.

## 4가지 목적지

### 1. Mind Palace (개인 레슨런)

특정 도메인에 한정되지 않는 범용 지식, 교훈, 인사이트, 원칙.

- 저장소: Obsidian vault "mind palace"
- 태그: `mp/*`
- 카테고리: `Inbox`, `Lessons`, `Insights`, `Principles`
- mind-palace 스킬과 동일한 노트 포맷을 따른다.

이런 내용이 해당된다:
- 엔지니어링, 디버깅, 설계에서 배운 교훈
- 커뮤니케이션, 협업, 의사결정에서 깨달은 점
- 생산성, 학습, 커리어 관련 인사이트
- 반복 적용 가능한 원칙

### 2. Design System Knowledge (디자인 시스템 지식)

디자인 시스템에 특화된 결정, 교훈, 참고 링크, 미해결 항목.

- 저장소: Obsidian vault "mind palace"
- 태그: `ds/*`
- 카테고리: `Inbox`, `Lessons`, `Links`, `Decisions`
- obsidian-design-system-knowledge 스킬과 동일한 노트 포맷을 따른다.

이런 내용이 해당된다:
- 컴포넌트 API, 토큰 규칙, 네이밍 결정
- 릴리스, 마이그레이션 과정의 교훈
- 접근성 리뷰에서 배운 점
- 디자인 시스템 관련 참고 문서 링크

### 3. CLAUDE.md (레포 메모리)

현재 작업 중인 레포지토리에서 세션마다 Claude가 알면 좋을 컨텍스트. CLAUDE.md는 Claude가 세션 시작 시 자동으로 읽는 파일이므로, 여기에 저장하면 다음 세션부터 자동으로 반영된다.

이런 내용이 해당된다:
- 프로젝트 구조나 아키텍처에 대한 새로운 이해
- 특정 파일이나 모듈의 주의사항
- 자주 실수하거나 잊기 쉬운 컨벤션
- 환경 설정, 빌드, 테스트 관련 팁
- "Claude가 다음에도 이걸 알고 있으면 좋겠다" 싶은 것

### 4. AGENTS.md (팀 공유 가이드)

팀 전체가 공유하면 좋을 가이드라인이나 규칙. AGENTS.md는 특정 폴더 하위에서 Claude가 작업할 때 참고하는 파일이므로, 폴더 수준의 규칙을 저장하기 좋다.

이런 내용이 해당된다:
- 코드 스타일이나 패턴에 대한 합의
- 특정 디렉토리의 파일 구조 규칙
- 공통 컴포넌트 사용법이나 제약
- 테스트 작성 가이드라인
- 팀에서 반복적으로 리뷰 코멘트로 나오는 패턴

## 실행 절차

### 1단계: 대화 분석

대화 전체를 읽고 4가지 목적지 각각에 해당하는 내용이 있는지 판단한다.

판단 기준:
- **재사용 가능한가?** — 이번 세션에만 유효한 일회성 정보가 아니라, 앞으로도 참고할 가치가 있는가
- **구체적인가?** — "좋은 코드를 쓰자" 같은 뻔한 내용이 아니라, 실제 경험에서 나온 구체적인 교훈이나 결정인가
- **이미 저장되어 있는가?** — 세션 중에 mind-palace나 obsidian-design-system-knowledge를 이미 호출해서 저장한 내용은 제외한다

각 목적지에 해당하는 내용이 없으면 그 목적지는 건너뛴다. 4가지 모두 해당하는 세션은 드물다 — 보통 1-2개에만 해당하는 내용이 있다.

### 2단계: 레포 컨텍스트 감지

CLAUDE.md나 AGENTS.md에 추가할 내용이 있다고 판단되면, 현재 작업 디렉토리에서 레포 루트를 찾는다.

```sh
# 레포 루트 찾기
git rev-parse --show-toplevel

# 기존 CLAUDE.md 확인
cat <repo-root>/CLAUDE.md

# AGENTS.md 파일들 확인
find <repo-root> -name "AGENTS.md" -maxdepth 3
```

기존 내용을 읽어서 중복을 피하고, 기존 스타일과 톤에 맞춰서 추가 내용을 제안한다.

레포가 감지되지 않거나 CLAUDE.md/AGENTS.md가 없는 경우에는 새로 만들지 말고, 내용만 텍스트로 제안한다. 사용자가 어디에 넣을지 결정할 수 있게 한다.

### 3단계: 제안 요약 보여주기

먼저 추출한 항목들을 텍스트로 간략히 보여준다. 각 항목마다 목적지, 카테고리, 제목, 핵심 요약을 한눈에 볼 수 있게 정리한다.

제안 포맷:

```
이번 세션에서 저장할 만한 내용을 정리했습니다.

1. 🧠 [Lessons] "useEffect 클린업 함수 누락 패턴"
   → mp/engineering, mp/debugging | Mind Palace

2. 🎨 [Decisions] "Button 토큰 네이밍 규칙"
   → ds/naming, ds/token | Design System

3. 📁 CLAUDE.md: "Jest WebSocket 테스트 시 --forceExit 필요"

4. 👥 AGENTS.md (src/components/): "useEffect cleanup 체크리스트"
```

해당 없는 목적지는 표시하지 않는다.

### 4단계: 멀티셀렉트로 저장할 항목 선택받기

제안을 보여준 직후, AskUserQuestion 도구를 사용해서 어떤 항목을 저장할지 선택받는다. multiSelect를 true로 설정해서 여러 개를 동시에 고를 수 있게 한다.

질문 구성 원칙:
- 추출한 항목 수에 따라 옵션을 구성한다 (최대 4개).
- 각 옵션의 label은 짧은 제목, description은 저장될 위치와 내용 요약.
- "수정 후 저장"이라는 옵션을 항상 마지막에 추가한다. 이 옵션을 고르면 사용자가 텍스트로 수정사항을 알려줄 수 있다.

예시:

```
AskUserQuestion:
  question: "어떤 항목을 저장할까요? (여러 개 선택 가능)"
  header: "저장 항목"
  multiSelect: true
  options:
    - label: "useEffect 클린업 패턴"
      description: "🧠 Mind Palace > Lessons | mp/engineering, mp/debugging"
    - label: "Button 토큰 네이밍 규칙"
      description: "🎨 Design System > Decisions | ds/naming, ds/token"
    - label: "CLAUDE.md: Jest --forceExit"
      description: "📁 레포 메모리에 추가"
    - label: "수정이 필요해요"
      description: "선택하면 어떤 부분을 수정할지 알려주세요"
```

사용자 응답 처리:
- 선택된 항목만 저장한다. 선택되지 않은 항목은 무시한다.
- "수정이 필요해요"가 선택되면 저장을 보류하고, 사용자의 수정 지시를 기다린 뒤 수정된 내용으로 다시 제안한다.
- "Other"가 선택되면 사용자의 자유 입력을 반영한다.

항목이 1개뿐이면 멀티셀렉트 대신 간단히 "이거 저장할까요?" 형태로 물어봐도 된다.

### 5단계: 저장

사용자가 선택한 항목만 각 목적지에 맞는 방법으로 저장한다.

**Mind Palace / Design System** — Obsidian CLI로 저장한다.

**폴더 규칙**: 도메인 구분은 폴더가 아니라 태그(`mp/*`, `ds/*`)로 한다. Mind Palace와 Design System 노트 모두 같은 카테고리 폴더(`Decisions/`, `Lessons/` 등)에 직접 저장한다. `DesignSystem/Decisions/`처럼 도메인별 하위 폴더를 만들지 않는다.

```sh
# 중복 확인
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" search query="<핵심어>"

# 노트 생성 — path는 항상 "<Category>/<file-name>.md" 형식
# 올바른 예: "Decisions/2026-03-31-button-token-alignment.md"
# 잘못된 예: "DesignSystem/Decisions/2026-03-31-button-token-alignment.md"
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" create path="<Category>/<file-name>.md" content="<note-content>"
```

Obsidian 노트 포맷은 각 스킬의 포맷을 그대로 따른다:
- Mind Palace: mind-palace 스킬의 frontmatter + 본문 템플릿
- Design System: obsidian-design-system-knowledge 스킬의 frontmatter + 본문 템플릿

**CLAUDE.md** — 파일 끝에 내용을 추가한다. 기존 섹션 구조가 있으면 적절한 위치에 넣는다.

**AGENTS.md** — 해당 폴더의 AGENTS.md에 내용을 추가한다. 파일이 없으면 새로 만들어도 되는지 사용자에게 확인한다.

### 6단계: 저장 완료 확인

모든 선택 항목의 저장이 끝나면 간단한 완료 메시지를 보여준다.

```
저장 완료!
- 🧠 Mind Palace: "useEffect 클린업 함수 누락 패턴" → Lessons/2026-03-31-useeffect-cleanup-pattern.md
- 📁 CLAUDE.md: Jest --forceExit 관련 내용 추가됨
```

파일 경로는 Obsidian 노트만 표시하고, CLAUDE.md/AGENTS.md는 "추가됨" 정도로 간결하게 마무리한다.

## description 작성 가이드

`description`은 recall 스킬이 노트의 관련성을 판단하는 핵심 필드다. title과 description만 읽고 전체 본문을 읽을지 결정하므로, description이 빈약하면 관련 지식이 있어도 못 찾는다.

작성 원칙:
- 1-2문장으로 쓰되, "무엇에 대한 지식인가"와 "어떤 상황에서 다시 찾게 될지"를 모두 담는다.
- "왜 중요한지"만 쓰지 말고, 검색 맥락(어떤 작업을 할 때 이 노트가 떠올라야 하는지)을 포함한다.
- 구체적인 대상어(컴포넌트 이름, 기술 용어 등)를 description에 자연스럽게 넣는다.

좋은 예:
- "MenuSheet의 CloseButton을 deprecated 유지 대신 breaking change로 즉시 제거한 배경. sheet 컴포넌트의 닫기 UX 패턴을 결정할 때 참고."
- "일정 추정 시 코드 리뷰 2라운드 + 피드백 반영 시간을 별도로 잡아야 한다는 교훈. 스프린트 플래닝에서 태스크 시간을 산정할 때 참고."

나쁜 예:
- "중요한 결정이다" (무엇에 대한 건지 모름)
- "나중에 참고할 것" (언제 찾아볼지 모름)
- "MenuSheet 관련" (너무 모호해서 recall이 관련성 판단 불가)

## Mind Palace 노트 포맷

mind-palace 스킬과 동일한 포맷을 따른다.

```yaml
---
title: "<human-readable title>"
description: "<1-2문장: 무엇에 대한 지식이고, 어떤 상황에서 다시 찾게 될지>"
category: "<Inbox|Lessons|Insights|Principles>"
tags:
  - <mp/tag-1>
  - <mp/tag-2>
captured_at: "<ISO-8601 timestamp>"
---
```

선택 필드: `source`, `entities`, `related`

본문은 카테고리별 템플릿을 따른다:
- Lessons: Content → Takeaway → Next Time
- Insights: Content → Shift → Implication
- Principles: Content → When to Apply → Exceptions
- Inbox: Content → Open Questions

mp/* 태그 controlled vocabulary:
`mp/engineering`, `mp/communication`, `mp/decision`, `mp/planning`, `mp/debugging`, `mp/design`, `mp/productivity`, `mp/career`, `mp/collaboration`, `mp/learning`, `mp/writing`, `mp/review`

## Design System 노트 포맷

obsidian-design-system-knowledge 스킬과 동일한 포맷을 따른다.

```yaml
---
title: "<human-readable title>"
description: "<1-2문장: 무엇에 대한 지식이고, 어떤 상황에서 다시 찾게 될지>"
category: "<Inbox|Lessons|Links|Decisions>"
tags:
  - <ds/tag-1>
  - <ds/tag-2>
captured_at: "<ISO-8601 timestamp>"
---
```

선택 필드: `source`, `entities`, `related`

본문은 카테고리별 템플릿을 따른다:
- Lessons: Content → Takeaway → Next Time
- Decisions: Content → Why → Trade-offs
- Links: Content → Why It Matters → Revisit When
- Inbox: Content → Open Questions

ds/* 태그 controlled vocabulary:
`ds/component`, `ds/token`, `ds/spec`, `ds/release`, `ds/docs`, `ds/implementation`, `ds/naming`, `ds/review`, `ds/a11y`, `ds/migration`

## CLAUDE.md 작성 가이드

CLAUDE.md에 추가하는 내용은 짧고 명확해야 한다. Claude가 매 세션 시작 시 읽는 파일이므로, 간결함이 핵심이다.

좋은 예:
- "Obsidian CLI 경로: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`, vault 이름: `mind palace`"
- "이 프로젝트의 테스트는 `pnpm test`로 실행하고, `--watch` 플래그는 CI에서 사용하지 않는다"
- "`src/tokens/` 디렉토리의 파일은 자동 생성되므로 직접 수정하지 않는다"

나쁜 예:
- 3문단 이상의 장문 설명
- 이미 코드에서 명확한 내용의 반복
- 일회성 디버깅 정보

기존 CLAUDE.md의 스타일(마크다운 헤더 사용 여부, 불릿 스타일, 언어 등)을 따른다.

## AGENTS.md 작성 가이드

AGENTS.md는 특정 폴더 컨텍스트에서 Claude가 따라야 할 규칙을 담는다.

좋은 예:
- `src/components/AGENTS.md`: "새 컴포넌트는 `ComponentName/index.tsx` + `ComponentName/ComponentName.test.tsx` 구조를 따른다"
- `src/api/AGENTS.md`: "모든 API 핸들러는 에러 응답에 `error_code`를 포함해야 한다"

AGENTS.md를 제안할 때는 반드시 어떤 폴더에 넣을지를 명시한다.

## 분석 우선순위

대화에서 다음 순서로 저장 가치를 판단한다:

1. **실수에서 배운 교훈** — 가장 저장 가치가 높다. "이걸 몰라서 시간을 썼다", "이렇게 했으면 더 좋았을 텐데"
2. **의사결정과 그 근거** — 왜 A를 선택하고 B를 버렸는지
3. **발견한 패턴이나 규칙** — 반복 적용 가능한 것
4. **환경/도구 관련 팁** — 설정, 명령어, 워크플로우
5. **참고 링크** — 대화 중 유용했던 문서나 자료

단순한 Q&A, 잡담, 이미 코드에 반영된 일회성 수정은 제외한다.

## 실패 사례와 안티패턴

다음을 피한다.

- 4가지 목적지 모두에 억지로 내용을 채우기 — 해당하는 것만 제안한다
- 이미 세션 중에 mind-palace나 design-system-knowledge로 저장한 내용을 중복 제안하기
- CLAUDE.md에 장문을 추가하기 — 한두 줄이 이상적이다
- AGENTS.md의 폴더 위치를 모호하게 남기기 — 정확한 경로를 명시한다
- 멀티셀렉트 질문 없이 바로 저장하기 — 반드시 AskUserQuestion으로 선택을 받은 뒤 저장한다
- 제안 텍스트만 보여주고 선택 질문을 빠뜨리기 — 제안 요약 직후에 반드시 멀티셀렉트 질문을 던진다
- 저장할 내용이 없는데 "저장할 내용이 없습니다"라고 장황하게 설명하기 — 짧게 "이번 세션에서는 따로 저장할 만한 내용이 없네요." 정도면 충분하다
- 도메인별 하위 폴더를 만들어서 저장하기 — `DesignSystem/Decisions/`가 아니라 `Decisions/`에 직접 저장하고 `ds/*` 태그로 구분한다
- 항목이 5개 이상일 때 한 질문에 다 넣기 — AskUserQuestion 옵션은 최대 4개이므로, 항목이 많으면 목적지별로 그룹핑하거나 우선순위가 높은 것만 제안한다
