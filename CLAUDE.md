# Skills 레포

Claude Code용 커스텀 스킬 모음 레포.

## 구조

```
skills/
├── mind-palace/                    통합 지식 저장 → Obsidian (mp/*, ds/*, ai/* 태그)
├── mind-palace-recall/             저장된 지식 검색 및 활용 + 활동 로그 기록
├── knowledge-lint/                 vault 지식 건강검진 + 정리
├── linear-collab/                  Linear 이슈 협업
├── wrap-up/                        세션 마무리 → 3가지 목적지로 분배 + 기존 노트 연결/업데이트
└── ui-references/                  UI 구현 레퍼런스 아카이브 (레포 포인터 + fetch, 문서 IA, 업데이트 다이제스트)
```

## Obsidian vault

- vault 이름: `mind palace`
- CLI: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`
- 모든 지식이 같은 vault의 같은 카테고리 폴더에 저장되고 태그로 구분
- 공유 인프라: vault 루트에 `_index.md`(지식 카탈로그)와 `_log.md`(활동 로그) 파일
  - `_index.md`: 태그별/카테고리별 전체 노트 목록. 노트 저장/수정/삭제 시 자동 갱신.
  - `_log.md`: 시간순 활동 기록 ([SAVE], [RECALL], [RECALL-USED], [RECALL-STALE], [LINT], [LINK]).
  - mind-palace, wrap-up, knowledge-lint, mind-palace-recall 스킬이 공유.

## ui-references

- 코드를 벤더링하지 않는다. `repo: org/repo` 고정 라인 + 경로 포인터만 담고 실제 코드는 그때그때 fetch한다.
- `repo:` 라인은 업데이트 다이제스트가 grep으로 수집하므로 형식을 바꾸지 않는다 (뒤에 주석 금지).
- 레포 구조는 예고 없이 바뀐다. 포인터 404를 만나면 리스팅으로 재발견하고 **문서를 고친다.**
- 판정 근거("왜 이게 1순위인가")는 추측으로 쓰지 않는다. 경로 오류는 `evals/verify-refs.sh`가 잡지만 근거 오류는 소스를 읽어야 잡힌다.

## 스킬 수정 시

- SKILL.md 수정 후 description 트리거 정확도 확인
- evals/ 디렉토리에 테스트 케이스가 있으면 검증
  - `ui-references`는 `evals/scenarios.md`(라우팅 시나리오, 서브에이전트로 실행) + `evals/verify-refs.sh`(포인터 회귀 테스트) 형태를 쓴다
- 다른 스킬을 참조하는 부분이 있으면 양쪽 동기화 확인
