---
name: knowledge-lint
description: Obsidian vault "mind palace"의 지식 건강을 점검하는 스킬. Inbox 체류 노트, 태그 drift, 고아 노트, 중복/유사 노트, stale 노트를 감지하고 정리를 제안한다. "vault 점검", "지식 정리", "노트 정리", "knowledge lint", "vault 건강검진", "노트 관리", "지식 베이스 정리" 같은 표현이 나올 때 사용한다. `/knowledge-lint`로 전체 점검을 실행하거나, `/knowledge-lint inbox`처럼 특정 점검만 실행할 수 있다.
---

# Knowledge Lint

## 목적

Obsidian vault에 축적된 지식의 건강 상태를 점검하고 정리를 돕는다. 노트가 쌓이기만 하고 관리되지 않으면 recall 정확도가 떨어지고 중복이 늘어난다. 이 스킬은 LLM에게 유지보수 bookkeeping을 맡겨서, 사용자는 큐레이션 결정에만 집중하게 한다.

- Obsidian 공식 CLI를 사용한다.
- vault 이름은 `mind palace`이다.
- `_index.md`와 `_log.md` 공유 인프라를 참조하고 갱신한다. mind-palace, wrap-up, mind-palace-recall 스킬과 공유.
- 점검 결과를 리포트로 보여주고, 조치할 항목은 사용자가 선택한다.
- 조치 실행 후 _index.md와 _log.md를 갱신한다.

## 호출 모드

### 전체 점검 (`/knowledge-lint`)

5가지 점검 항목을 모두 실행한다.

### 부분 점검 (`/knowledge-lint <항목>`)

특정 점검만 실행한다. 사용 가능한 항목:
- `inbox` — Inbox 체류 점검
- `orphans` — 고아 노트 점검
- `duplicates` — 중복/유사 노트 점검
- `stale` — stale 노트 점검
- `coverage` — 커버리지 리포트

## 점검 항목

### 1. Inbox 체류

Inbox 카테고리에 2주 이상 머문 노트를 감지한다. Inbox는 임시 보관소이므로 오래 머물면 안 된다.

```sh
# Inbox 폴더의 노트 목록
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" search query="" path="Inbox/"
```

각 노트의 `captured_at` frontmatter를 읽어서 현재 날짜와 비교한다.

조치 옵션:
- **분류**: 적절한 카테고리(Lessons, Insights, Principles, Decisions, Links)로 이동. frontmatter의 category 변경 + 파일 이동.
- **삭제**: 더 이상 가치 없는 노트 삭제.
- **유지**: 아직 Inbox에 둘 이유가 있으면 유지.

### 2. 고아 노트

`related` 필드가 비어있고 `_log.md`에서 RECALL 이력도 없는 노트를 감지한다.

```sh
# _log.md에서 RECALL 이력 확인
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="_log.md"
```

조치 옵션:
- **연결 후보 탐색**: 같은 태그를 가진 다른 노트를 찾아 related 링크 추가.
- **아카이브**: `_archived/` 폴더로 이동.
- **유지**: 독립적으로 가치 있는 노트면 그대로 둔다.

### 3. 중복/유사 노트

같은 태그를 가지면서 title이나 description이 유사한 노트 쌍을 감지한다.

_index.md에서 같은 태그 아래 나열된 노트들의 제목과 description을 비교한다. 완전히 동일하지 않더라도 같은 주제를 다루는 것으로 보이면 통합 후보로 제안한다.

조치 옵션:
- **통합**: 두 노트를 합친 새 노트 생성. 원본은 삭제하거나 아카이브.
- **별도 유지**: 다른 관점이니 별도로 유지.
- **연결**: 중복은 아니지만 관련 있으니 related 링크만 추가.

### 4. stale 노트

다음 조건에 해당하는 노트를 감지한다:
- `_log.md`에 `[RECALL-STALE]` 플래그가 있는 노트
- 6개월 이상 RECALL 이력이 없는 노트 (captured_at 기준이 아니라 마지막 참조 기준)

조치 옵션:
- **업데이트**: 내용을 현재 상황에 맞게 수정.
- **아카이브**: `_archived/` 폴더로 이동.
- **삭제**: 완전히 폐기.
- **유지**: 참조 빈도와 무관하게 가치 있는 노트면 유지.

### 5. 커버리지

카테고리별 노트 수 분포를 보여주고, 비어있거나 과밀한 영역을 리포트한다. _index.md를 기반으로 분석한다.

- 노트 수가 0인 카테고리: "이 카테고리에 아직 노트가 없습니다"
- 노트 수가 20개 이상인 카테고리: "종합 노트를 만들면 좋을 수 있습니다" 제안

## 실행 절차

### 1단계: 인프라 읽기

```sh
# _index.md 읽기
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="_index.md"

# _log.md 읽기
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="_log.md"
```

_index.md가 없으면 vault 전체를 스캔해서 초기 index를 먼저 생성한다.

### 2단계: 점검 실행

호출 모드에 따라 전체 또는 선택된 점검을 실행한다. 각 점검 항목에서 문제가 발견되면 목록에 추가한다.

### 3단계: 리포트 출력

```
🔍 Knowledge Lint Report (YYYY-MM-DD)

📊 Vault 현황: N notes
📈 최근 30일: N건 저장, M건 참조, K건 활용

⚠️ 조치 필요:
1. [Inbox 체류] "React Server Components 메모" (2026-03-20, 16일)
   → 제안: Lessons로 이동

2. [유사 노트] 통합 후보:
   - "Promise 에러 핸들링" (2026-03-28)
   - "async/await 예외 처리" (2026-03-15)
   → 제안: 통합

3. [고아 노트] "Git rebase 전략" (2026-02-10)
   참조: 0회 | related: 없음
   → 제안: 연결 후보 탐색

4. [stale] "Webpack 설정 가이드" — RECALL-STALE (2026-03-25)
   → 제안: 업데이트 또는 아카이브

✅ 양호:
- 가장 활발: "useEffect 클린업 패턴" (5회 활용)
- related 연결이 가장 풍부: "React 라이프사이클 이해" (4개 연결)

💡 참고:
- News: 아직 노트 없음
- Lessons: 22건 — 종합 노트 생성 고려
```

문제가 없으면 "✅ 모든 점검 통과" 메시지만 짧게 보여준다.

### 4단계: 조치 선택

AskUserQuestion으로 조치할 항목을 선택받는다. multiSelect를 true로 설정.

```
AskUserQuestion:
  question: "어떤 항목을 정리할까요? (여러 개 선택 가능)"
  header: "정리 항목"
  multiSelect: true
  options:
    - label: "RSC 메모 → Lessons"
      description: "[Inbox 체류] React Server Components 메모를 Lessons로 이동"
    - label: "Promise 노트 통합"
      description: "[유사 노트] Promise 에러 핸들링 + async/await 예외 처리"
    - label: "Git rebase 연결"
      description: "[고아 노트] 관련 노트 탐색 후 연결"
    - label: "나중에 할게요"
      description: "이번에는 리포트만 확인하고 넘어간다"
```

항목이 5개 이상이면 우선순위가 높은 것(Inbox 체류 > stale > 중복 > 고아)부터 옵션에 넣고, "나머지 N건도 보기"를 마지막 옵션으로 구성한다.

### 5단계: 조치 실행

선택된 항목에 대해 조치를 실행한다.

**카테고리 이동 (Inbox → Lessons 등)**:
1. 기존 노트 읽기
2. frontmatter의 category 변경
3. 본문 템플릿을 새 카테고리에 맞게 조정 (예: Inbox 템플릿 → Lessons 템플릿)
4. 새 카테고리 폴더에 노트 생성
5. 기존 Inbox 노트 삭제

```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="Inbox/<file>.md"
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" create path="Lessons/<file>.md" content="<updated-content>"
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" delete path="Inbox/<file>.md"
```

**노트 통합**:
1. 두 노트를 모두 읽기
2. 내용을 합쳐서 새 노트 생성 (더 최신 날짜 사용)
3. 양쪽의 entities와 related를 합산
4. 원본 노트 삭제 또는 `_archived/`로 이동

**연결 추가**:
1. 같은 태그를 가진 노트 검색
2. 관련성 높은 노트 2-3개의 related에 양방향 링크 추가

**아카이브**:
```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" read path="<Category>/<file>.md"
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" create path="_archived/<file>.md" content="<content>"
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" delete path="<Category>/<file>.md"
```

**삭제**:
```sh
/Applications/Obsidian.app/Contents/MacOS/Obsidian vault="mind palace" delete path="<Category>/<file>.md"
```

### 6단계: 인프라 갱신

모든 조치가 완료되면:

1. `_index.md`를 재생성한다 (삭제/이동/통합된 항목 반영).
2. `_log.md`에 `[LINT]` 엔트리를 추가한다.

```markdown
- [LINT] Inbox 정리: 1건 → Lessons 이동, 1건 삭제 | 유사 노트: 1쌍 통합 | 고아 노트: 1건 연결
```

### 7단계: 완료 메시지

```
정리 완료!
- "RSC 메모" → Lessons/2026-03-20-react-server-components.md로 이동
- "Promise 에러 핸들링" + "async/await 예외 처리" → 통합: Lessons/2026-03-28-promise-error-handling.md
- "Git rebase 전략" ↔ "브랜치 관리 원칙" 양방향 연결 추가
```

## Obsidian CLI 사용법

macOS 기준 경로: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`, vault 이름: `mind palace`.

CLI가 동작하지 않으면 "Obsidian CLI에 접근할 수 없습니다. Obsidian 앱 버전이 1.12 이상인지 확인해주세요." 메시지를 보여주고 중단한다.

## 실패 사례와 안티패턴

다음을 피한다.

- 사용자 확인 없이 바로 노트를 삭제하거나 이동하기 — 반드시 AskUserQuestion으로 선택을 받는다
- 리포트만 보여주고 조치 선택을 빠뜨리기 — 리포트 직후 반드시 조치 선택 질문을 던진다
- 문제가 없는데 억지로 문제를 만들기 — 모든 점검을 통과하면 짧게 "양호" 메시지만 보여준다
- vault 전체를 한 번에 읽으려 하기 — _index.md와 _log.md를 먼저 읽고, 필요한 노트만 추가로 읽는다
- 아카이브를 삭제와 혼동하기 — 아카이브는 `_archived/` 폴더 이동, 삭제는 완전 제거
- 인프라 갱신을 빠뜨리기 — 조치 실행 후 반드시 _index.md와 _log.md를 갱신한다
