# Skills 레포

Claude Code용 커스텀 스킬 모음 레포.

## 구조

```
skills/
├── mind-palace/                    통합 지식 저장 → Obsidian (mp/*, ds/*, ai/* 태그)
├── mind-palace-recall/             저장된 지식 검색 및 활용 + 활동 로그 기록
├── knowledge-lint/                 vault 지식 건강검진 + 정리
├── linear-collab/                  Linear 이슈 협업
└── wrap-up/                        세션 마무리 → 3가지 목적지로 분배 + 기존 노트 연결/업데이트
```

## Obsidian vault

- vault 이름: `mind palace`
- CLI: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`
- 모든 지식이 같은 vault의 같은 카테고리 폴더에 저장되고 태그로 구분
- 공유 인프라: vault 루트에 `_index.md`(지식 카탈로그)와 `_log.md`(활동 로그) 파일
  - `_index.md`: 태그별/카테고리별 전체 노트 목록. 노트 저장/수정/삭제 시 자동 갱신.
  - `_log.md`: 시간순 활동 기록 ([SAVE], [RECALL], [RECALL-USED], [RECALL-STALE], [LINT], [LINK]).
  - mind-palace, wrap-up, knowledge-lint, mind-palace-recall 스킬이 공유.

## 스킬 수정 시

- SKILL.md 수정 후 description 트리거 정확도 확인
- evals/ 디렉토리에 테스트 케이스가 있으면 검증
- 다른 스킬을 참조하는 부분이 있으면 양쪽 동기화 확인
