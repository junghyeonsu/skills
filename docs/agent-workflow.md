# Agent Workflow

Goal로 끝까지 실행하고, 실제 사용자 결과를 확인하고, 반복 실수에서 배웁니다. pstack의 유용한 원칙과 개인 작업에서 관찰한 반복 문제를 바탕으로 만든 워크플로우입니다. v0.1.3에서는 `goal-loop`를 호출하면 검증과 학습도 함께 수행합니다.

## 구성

| 스킬 | 역할 |
| --- | --- |
| `goal-loop` | 목표·범위·권한·체크포인트를 유지하며 실행 |
| `verify-outcome` | 실제 환경에서 완료 조건 확인, 오래된 근거 감지 |
| `learn-from-work` | 교훈·결정·임시 상태를 분리하고 재발 방지 장치로 연결 |

`goal-loop`는 큰 작업을 시작하거나 재개할 때 사용합니다. 시작할 때 `verify-outcome`과 `learn-from-work`도 읽고 같은 작업 흐름에서 자동 수행합니다. 완료할 결과와 검증 조건을 정하고, 기존 코드·자원을 삭제하거나 재사용할 수 있는지 검토한 뒤 작은 단위로 진행합니다. 중단되면 결과·남은 작업·다음 행동을 checkpoint로 남깁니다. 실행 중·완료 전에는 검증을 하고, 의미 있는 교정·실패 시점과 최종 인계 전에는 학습을 검토합니다. 학습에서 코드를 변경하면 해당 부분을 다시 검증한 뒤 완료합니다. 두 스킬을 따로 호출할 필요는 없습니다.

`verify-outcome`은 완료 보고나 배포 전에 사용합니다. 최초 요청의 실제 사용자 흐름을 다시 확인하고, 로컬 테스트·원격 CI·배포·네이티브 실행 근거를 구분합니다. 선택적 receipt 도구는 명령 결과와 지정한 파일의 해시를 기록해 검증 후 파일 변경이나 실패한 검사 결과를 감지합니다. 실제 사용자 동작의 정확성은 별도 확인합니다.

`learn-from-work`은 사용자 교정, 예상 밖의 실패, 반복 마찰에서 배울 내용이 있을 때 사용합니다. 임시 상태·교훈·결정을 구분하고 프로젝트 지식은 해당 프로젝트에 둡니다. 반복 문제는 구조·타입·lint/CI·행동 테스트 같은 재발 방지 장치로 연결하고, 근거가 있는 공통 작업 원칙만 개인 스킬에 반영합니다. 호스트 메모리 수정과 private 기록 공개에는 별도 명시적 요청이 필요합니다.

공통 내용은 `plugins/agent-workflow/skills/` 한 곳에 있습니다. root `plugin.json`은 portable Agent Plugins manifest, `.claude-plugin/plugin.json`은 Claude 호환 manifest입니다. 두 marketplace 파일은 같은 플러그인을 가리킵니다. 모델 이름이나 전용 MCP 서버, 자동 실행 훅은 필요 없습니다. 선택적 근거 도구는 Python 3 표준 라이브러리만 사용합니다.

이 패키지는 스킬을 제공합니다. 무인 실행 지속·goal 수명주기·권한은 각 호스트가 담당합니다. 설치만으로 에이전트 행동 준수가 입증되지는 않습니다.

## Codex 설치

GitHub 저장소에서 설치합니다.

```sh
codex plugin marketplace add junghyeonsu/skills --ref main
codex plugin add agent-workflow@agent-workflows
codex plugin list --json
```

로컬 수정본을 사용할 때는 첫 번째 명령의 `junghyeonsu/skills`를 저장소 루트의 절대 경로로 바꾸고 `--ref main`을 생략합니다. `main`은 새 업데이트를 받는 채널이고, 안정화 뒤 tag/ref로 고정할 수 있습니다.

새 대화 또는 앱 재로드 후 스킬 목록에서 확인합니다. 현재 대화가 생성 이후의 스킬 목록을 자동 갱신한다고 가정하지 않습니다.

```text
$goal-loop 이 계획을 goal로 끝까지 실행해줘.
기존 producer/consumer 계약을 유지하고, 추가하기 전에 삭제·재사용을 고려해줘.
완료 조건은 구현뿐 아니라 실제 대상 환경에서 흐름 검증과 근거 기록이야.
현재 세션에서 승인한 작업 범위와 조건을 유지해줘.
```

일반 작업에 스킬이 자동 선택될 수 있지만 native goal 등록은 명시적인 goal 요청이 있어야 합니다. Codex `/goal`은 계속 사용하는 기본 실행 루프입니다. 이 패키지는 별도 반복 실행기를 설치하지 않습니다.

## Claude Code 설치

```sh
claude plugin marketplace add junghyeonsu/skills
claude plugin install agent-workflow@agent-workflows
```

대화에서는 `/agent-workflow:goal-loop`, `/agent-workflow:verify-outcome`, `/agent-workflow:learn-from-work`을 사용합니다. 로컬 수정본을 사용할 때는 marketplace 등록에 저장소 루트의 절대 경로를 사용합니다. Claude의 실행 지속 방식은 Codex goal과 동일하다고 가정하지 않습니다.

## Grok Build와 다른 에이전트

[Grok Build 공식 문서](https://docs.x.ai/build/features/skills-plugins-marketplaces)는 Claude Code 플러그인 호환과 `SKILL.md` 검색을 설명합니다. 로컬에서는 `grok --plugin-dir /absolute/path/to/skills/plugins/agent-workflow`로 로드한 뒤 `/skills`에서 확인할 수 있습니다. 초기 버전은 Grok 실행 검증을 하지 않았습니다. 일반 Grok 채팅·Grok Bot 지원을 뜻하지 않습니다.

다른 호스트는 Agent Skills 지원을 사용하거나 해당 `SKILL.md`를 직접 읽습니다. 공통 지침의 이식성과 실행·예약 기능의 이식성은 별도로 확인해야 합니다.

## 작업하면서 좋아지게 만들기

기존 프로젝트의 `.agents/learnings`와 `.agents/decisions`가 있으면 그대로 사용합니다. 작업 내 임시 상태는 checkpoint에 둡니다. 개인 전역 스킬에는 프로젝트 계약·API·비밀정보를 넣지 않습니다.

반복 오류는 구조·타입·lint/CI·행동 테스트·작은 도구 순으로 해결책을 검토합니다. 후보 지침은 실제 실패 사례와 허용 사례를 검증한 뒤 승격합니다. 한 번의 프로젝트 취향으로 전역 규칙을 만들지 않습니다. 호스트 메모리는 별도 명시적인 요청 없이 수정하지 않습니다.

첫 10개의 비슷한 goal에서 누락된 필수 항목, 사람의 재지시, 실제 환경 근거, 같은 실패의 반복, 불필요한 의존성·리소스 추가를 관찰합니다. 후보를 한 번에 하나씩 적용하고 비용과 재발률을 비교합니다. 초기 패키지는 이 수집·분석을 자동 예약하지 않습니다.

## 검증과 배포

```sh
python3 -m unittest discover -s tests -v
claude plugin validate --strict ./plugins/agent-workflow
claude plugin validate --strict .
```

Codex skill creator의 `quick_validate.py`로 각 스킬을 추가 검증할 수 있습니다. 설치·문법 검사, 실제 스킬 호출, 이후 작업 개선은 각각 다른 검증 단계입니다. 검증 결과는 [VALIDATION.md](../VALIDATION.md)에 기록합니다.

업데이트는 source 변경 → 검사 → 플러그인 두 manifest의 동일 version 갱신 → marketplace 업데이트 → 각 클라이언트 inventory 확인 순서입니다. Codex는 `codex plugin marketplace upgrade agent-workflows` 후 설치를 갱신하고, Claude는 `claude plugin update agent-workflow@agent-workflows`를 사용합니다. CLI 옵션은 실행 버전의 도움말로 확인합니다.

배포 레포에는 이 패키지 파일만 등록합니다. 원본 세션·개인 분석·회사 코드·스크린샷·실행 로그는 포함하지 않습니다. 기록에 회사별 결정이 생기면 해당 프로젝트에 남깁니다. 출처는 [PROVENANCE.md](../PROVENANCE.md)에 있습니다.
