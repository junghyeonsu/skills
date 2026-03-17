---
name: linear-collab
description: |
  Linear 이슈와 개발 대화를 연결하는 협업 스킬. 구현 논의 중 결정사항, 발견사항, 스펙 변경을
  Linear 이슈 코멘트에 기록하고, 최신 스펙을 이슈 본문에 반영하며, 상태를 동기화한다.

  다음 상황에서 사용:
  (1) /linear-collab DES-XXXX 로 이슈 작업 세션 시작
  (2) 대화 중 설계/구현 결정을 Linear 코멘트로 기록할 때
  (3) 현재 구현 스펙을 이슈 본문에 반영할 때
  (4) 이슈 상태 전환 (In Progress, In Review 등)
  (5) 세션 마무리 시 기록 누락 확인

  또한 대화 중 결정/발견 패턴을 자동 감지하여 기록을 제안한다:
  "~로 결정", "~하기로 함", "~가 낫겠다" → 결정 기록 제안
  "~를 발견", "~가 안 됨", "~제약이 있음" → 메모 기록 제안
---

# Linear Collab

개발 대화와 Linear 이슈를 연결한다.

## 핵심 규칙

- 모든 코멘트와 이슈 내용은 **한국어**로 작성한다.
- 이슈 ID 기본 형식: `DES-XXXX`. 4자리 숫자만 주어지면 `DES-` 접두사를 붙인다.
- `priority`는 사용자가 명시적으로 요청하지 않는 한 변경하지 않는다.
- 이슈를 새로 만들 때 상태는 **Todo**로 설정한다.
- 브랜치명, PR 제목/본문에 Linear 이슈 ID를 포함하지 않는다.

## 세션 상태

세션 시작 시 현재 이슈 ID를 기억한다. 이후 명령에서 이슈 ID 생략 가능.

## 명령어

### `DES-XXXX` — 세션 시작

1. `get_issue`로 이슈 읽기 (description, status, assignee)
2. `list_comments`로 기존 코멘트 확인
3. 사용자에게 이슈 요약 표시 (제목, 상태, 핵심 내용, 최근 코멘트)
4. 상태가 Backlog/Todo이면 → "In Progress로 변경할까요?" 제안

### `decision "내용"` — 결정 기록

대화 맥락에서 결정 배경과 검토한 대안을 자동 추출하여 코멘트로 기록한다.
코멘트 형식: [references/comment-templates.md](references/comment-templates.md)의 Decision 템플릿.

### `note "내용"` — 발견/메모 기록

탐색 결과, 제약사항, 참고사항을 코멘트로 기록한다.
코멘트 형식: [references/comment-templates.md](references/comment-templates.md)의 Note 템플릿.

### `spec` — 이슈 본문에 스펙 업데이트

현재까지의 결정사항을 종합하여 이슈 description에 반영한다.

**이슈 본문 구조:**
```
{원본 설명 — 그대로 유지}

---

## 현재 구현 스펙 (YYYY-MM-DD 업데이트)

### 결정사항
- ...

### API / 인터페이스
- ...

### 미결 사항
- ...
```

**업데이트 규칙:**
- 원본 설명은 `---` 구분선 위에 보존한다.
- `---` 이후의 `## 현재 구현 스펙` 섹션만 교체한다.
- 구분선+스펙 섹션이 없으면 새로 추가한다.
- `save_issue`의 `description` 필드로 전체 본문을 업데이트한다.

### `sync` — 상태 동기화

작업 진행에 맞춰 이슈 상태를 전환한다.
- 구현 시작 → **In Progress**
- PR 생성 → **In Review** + `links`로 PR URL 연결
- 사용자 확인 후 전환한다.

### `wrap` — 세션 마무리

1. 세션 중 내린 결정 목록을 정리한다.
2. 아직 기록하지 않은 결정이 있으면 기록을 제안한다.
3. 이슈 설명 vs 실제 구현 방향 차이를 확인한다.
4. 차이가 있으면 Deviation 코멘트를 기록한다.
   코멘트 형식: [references/comment-templates.md](references/comment-templates.md)의 Deviation 템플릿.
5. 세션 요약 코멘트를 작성한다.
   코멘트 형식: [references/comment-templates.md](references/comment-templates.md)의 Session Wrap-up 템플릿.

## 자동 감지

명시적 명령 없이도 대화에서 다음 패턴을 감지하면 기록을 **제안**한다.
제안만 하고, 사용자가 승인한 후에만 기록한다.

**결정 감지:**
- "~로 결정", "~하기로 함", "~가 낫겠다", "~로 가자", "~로 하자"

**발견 감지:**
- "~를 발견", "~가 안 됨", "~제약이 있음", "~확인함", "~문제가 있음"

**구현 차이 감지:**
- 구현이 이슈 설명과 다른 방향으로 진행될 때

## 이슈 라이프사이클

- 작업 시작 시 → **In Progress**
- PR 생성 또는 리뷰 준비 → **In Review** + PR URL 링크
- 서브이슈는 커밋 완료 시 done 처리 가능
- 부모 이슈는 PR 머지 시 done (직접 마킹하지 않음)
