# Skills 레포

Claude Code용 커스텀 스킬 모음 레포.

## 구조

```
skills/
├── mind-palace/                    범용 지식 → Obsidian (mp/* 태그)
├── mind-palace-recall/             저장된 지식 검색 및 활용
├── obsidian-design-system-knowledge/  디자인 시스템 지식 → Obsidian (ds/* 태그)
├── obsidian-ai-archive/            AI 뉴스/교훈 → Obsidian (ai/* 태그)
├── linear-collab/                  Linear 이슈 협업
└── wrap-up/                        세션 마무리 → 위 4가지 목적지로 분배
```

## Obsidian vault

- vault 이름: `mind palace`
- CLI: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`
- 세 도메인(mp, ds, ai)이 같은 vault의 같은 카테고리 폴더를 공유하고 태그로 구분

## 스킬 수정 시

- SKILL.md 수정 후 description 트리거 정확도 확인
- evals/ 디렉토리에 테스트 케이스가 있으면 검증
- 다른 스킬을 참조하는 부분이 있으면 양쪽 동기화 확인
