# Skills 레포

여러 에이전트용 커스텀 스킬과 플러그인 레포.

## 구조

```
skills/
├── AGENTS.md                       스킬 작성 컨벤션
└── ui-references/                  UI 구현 레퍼런스 아카이브
    ├── SKILL.md                    라우터 (결정표 + 컴포넌트 인덱스 + fetch 프로토콜)
    ├── references/                 컴포넌트 축(lookup-*) + 레포 축 + 문서/스킬 카탈로그
    └── evals/                      라우팅 시나리오 + 포인터 회귀 테스트
```

작성 컨벤션은 `skills/AGENTS.md` 참고.

## ui-references

- **코드를 벤더링하지 않는다.** `repo: org/repo` 고정 라인 + 경로 포인터만 담고 실제 코드는 그때그때 fetch한다.
- `repo:` 라인은 업데이트 다이제스트가 grep으로 수집하므로 **형식을 바꾸지 않는다** (뒤에 주석 금지).
- 레포 구조는 예고 없이 바뀐다. 포인터 404를 만나면 리스팅으로 재발견하고 **문서를 고친다.** 고치지 않으면 다음에 또 만난다.
- 브랜치가 `main`이 아닌 레포가 많다(base-ui·embla·floating-ui는 `master`, HeroUI는 `v3` 등). 엔트리의 `branch:` 값을 신뢰하고, 바뀌면 검증 스크립트가 잡는다.
- **판정 근거("왜 이게 1순위인가")는 추측으로 쓰지 않는다.** 경로 오류는 `evals/verify-refs.sh`가 잡지만 근거 오류는 소스를 읽어야 잡힌다. 실제로 라우팅 eval이 사실 오류 2건을 반증한 적이 있다.
- 수록 기준은 취향이다. 완전성 의무가 없으므로 억지로 채우지 않는다.

## 스킬 수정 시

- SKILL.md 수정 후 description 트리거 정확도 확인
- evals/ 디렉토리에 테스트 케이스가 있으면 검증
- 다른 스킬을 참조하는 부분이 있으면 양쪽 동기화 확인


## Agent Workflow 플러그인

- 공통 원본은 `plugins/agent-workflow/skills/`에 둔다. 다른 호스트용 스킬 사본을 만들지 않는다.
- `goal-loop`, `verify-outcome`, `learn-from-work`은 실행·완료 검증·학습을 담당한다. UI 레퍼런스가 필요하면 기존 `ui-references`를 선택적으로 사용한다.
- 플러그인 안의 `AGENTS.md`와 각 스킬의 설명·eval 시나리오를 참고한다.
- 세션 원문·개인 분석·회사 코드·런타임 근거는 이 배포 저장소에 넣지 않는다.
- 새 스킬 문법 검사, receipt CLI 테스트, 플러그인 manifest 검증을 수행한다. 설치 검증을 새 에이전트의 행동 검증으로 보고하지 않는다.
