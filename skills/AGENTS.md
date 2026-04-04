# Skills 디렉토리 가이드

## 스킬 구조

각 스킬은 `skills/<skill-name>/` 디렉토리에 위치한다.

```
<skill-name>/
├── SKILL.md          (필수) YAML frontmatter + 마크다운 본문
├── evals/            (선택) 테스트 케이스
│   └── evals.json
└── references/       (선택) 참조 문서
```

## SKILL.md frontmatter 규칙

```yaml
---
name: <skill-name>       # 디렉토리명과 동일
description: <트리거 설명>  # 한국어, 1-3문장, "언제 사용하는지"를 구체적으로
---
```

- description은 Claude가 스킬을 호출할지 결정하는 핵심 필드다. 모호하면 트리거가 안 된다.
- 한국어 스킬이면 description도 한국어로 쓴다.

## 스킬 간 참조

스킬이 다른 스킬의 포맷을 따를 때는 "X 스킬과 동일한 포맷을 따른다"라고 명시하되, 핵심 필드는 인라인으로 포함한다. 다른 스킬을 읽어야만 실행 가능한 상황을 만들지 않는다.

## Obsidian 연동 스킬 공통 규칙

- vault 이름: `mind palace`
- CLI 경로: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`
- 도메인 구분: 폴더가 아닌 태그 (`mp/*`, `ds/*`, `ai/*`)
- 카테고리 폴더: vault 루트에 직접 위치 (`Lessons/`, `Decisions/` 등)
