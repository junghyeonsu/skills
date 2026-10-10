## skills

여러 에이전트에서 사용할 커스텀 스킬과 플러그인 모음.

### ui-references

컴포넌트나 헤드리스 훅을 만들 때 **어떤 오픈소스를 참고할지** 찾고, 그 소스를 바로 fetch해서 읽는다. 코드를 복사해 두지 않고 `org/repo` + 경로 포인터만 담는 방식이라 낡지 않는다.

- **컴포넌트별 판정** — Select/Combobox, DatePicker, OTP, Slider, Dialog, Drawer, Toast, Carousel, Table 등. 1순위와 "무엇이 갈리는 지점인가"
- **레포 맵** — Base UI, Radix, Zag, React Aria, Ark, Ariakit, Panda, CVA, vanilla-extract, StyleX, shadcn, Park UI, Chakra, Mantine, Spectrum, Astryx, Fluent, Primer, Polaris, Carbon, Tamagui, Style Dictionary, Terrazzo 등 38개
- **단일목적 라이브러리** — embla, cmdk, vaul, sonner, input-otp, floating-ui, TanStack Virtual/Table 등. 해당 컴포넌트 항목 안에 배치
- **문서 사이트 IA** — llms.txt 유무, 가이드라인/API 분리 여부, 코드 예제의 출처
- **디자인 스킬 카탈로그** — 모션·UI 크래프트 스킬 레포
- **업데이트 다이제스트** — 수록된 레포들의 최근 릴리스를 한 번에 모아보기

```bash
npx skills add https://github.com/junghyeonsu/skills --skill ui-references
```

#### 검증

포인터가 살아 있는지는 스크립트로 확인한다 — 레포 존재와 브랜치 대조, raw URL 200, llms.txt 실제 여부, 대표 코드 경로 실존.

```bash
bash skills/ui-references/evals/verify-refs.sh
```

레포 구조는 예고 없이 바뀐다. 2026-08 검증에서 react-spectrum(`@react-aria/*` → `react-aria/src/*`), shadcn(`apps/www` → `apps/v4`), input-otp(모노레포화)의 이동을 이 스크립트가 잡았다. 분기에 한 번 정도 돌리면 충분하다.

라우팅이 의도대로 되는지는 `skills/ui-references/evals/scenarios.md`의 시나리오를 서브에이전트로 실행해 확인한다.


## Agent Workflow

Goal 실행 → 실제 검증 → 교훈·결정 정리의 개인 작업 루프입니다. 공통 스킬은 `plugins/agent-workflow/skills/` 한 곳에 두고 Codex·Claude에 플러그인으로 등록합니다. 기존 `ui-references`와 역할이 겹치지 않습니다.

| 스킬 | 역할 |
| --- | --- |
| goal-loop | 실행의 진입점: 목표·범위·권한 유지, 삭제·재사용 우선, 검증·학습 자동 연결 |
| verify-outcome | 실제 환경·현재 변경을 기준으로 완료 근거 확인 |
| learn-from-work | 교훈과 결정 분리, 반복 실수를 적절한 검증 장치로 연결 |

Codex:

```sh
codex plugin marketplace add junghyeonsu/skills --ref main
codex plugin add agent-workflow@agent-workflows
```

Claude Code:

```sh
claude plugin marketplace add junghyeonsu/skills
claude plugin install agent-workflow@agent-workflows
```

대화에서 Codex는 `$goal-loop`, Claude는 `/agent-workflow:goal-loop`를 사용합니다. 로컬 수정본을 검토할 때는 `junghyeonsu/skills` 대신 이 저장소의 절대 경로를 사용하고 Codex의 `--ref main`은 생략합니다.

`goal-loop`를 한 번 호출하면 `verify-outcome`과 `learn-from-work`을 함께 읽고 수행합니다. 완료 전 검증 → 학습 검토 → 학습에서 변경한 부분 재검증까지 이어집니다. 별도 검증이나 회고만 필요할 때는 두 스킬을 개별 호출할 수 있습니다. 학습할 내용이 없으면 불필요한 교훈 파일을 만들지 않습니다.

[설치·사용·검증 안내](docs/agent-workflow.md) · [출처](PROVENANCE.md)
