---
name: ui-references
description: UI/디자인시스템 구현 레퍼런스 아카이브. 컴포넌트나 헤드리스 훅을 만들 때 어떤 오픈소스를 참고할지 찾고, 그 소스 코드를 바로 fetch해서 읽는다. 문서 사이트 구조(IA) 레퍼런스와 디자인 관련 스킬 컬렉션 카탈로그도 포함하며, 레퍼런스들의 최근 업데이트를 모아보는 기능도 있다. Use when 컴포넌트 구현 참고처를 찾을 때, headless 훅/상태머신 설계를 비교할 때, recipe·토큰 시스템을 설계할 때, 문서 사이트 구조를 참고할 때, 특정 분야(모션 등) 맥락을 빠르게 주입할 때. Triggers on 컴포넌트 구현 참고, 헤드리스 훅 어디 참고, base ui/radix/zag 비교, 레퍼런스 레포, 다른 라이브러리는 어떻게, OTP/Carousel/DatePicker 구현, recipe 시스템 비교, 문서 구조 참고, 문서 사이트 IA, 모션 맥락, 디자인 스킬, 레퍼런스 업데이트, 이번 달 디자인시스템 소식.
---

# UI 레퍼런스 아카이브

**이건 백과사전이 아니라 개인 취향 큐레이션이다.** 목적은 두 가지 — (1) 코딩할 때 참고, (2) 필요한 분야의 맥락을 빠르게 주입. 완전성 의무는 없다. 여기 없는 라이브러리는 그냥 아직 안 담긴 것이고, 억지로 채우지 않는다. 마음에 안 드는 항목은 지워도 된다.

수록된 내용은 **포인터**다. 코드를 복사해 두지 않고 `org/repo` + 경로만 적어두며, 실제 코드는 그때그때 fetch해서 읽는다.

## 1. 어디부터 볼까

| 하려는 일 | 1순위 | 참조 파일 |
| --- | --- | --- |
| 특정 컴포넌트 구현 참고 | (컴포넌트 인덱스에서 찾기) | `lookup-*.md` |
| headless 훅 API 설계 | Base UI | [headless-primitives.md](references/headless-primitives.md) |
| 프레임워크 무관 상태 로직 (Lynx 포팅 등) | Zag | [state-machines.md](references/state-machines.md) |
| ARIA·키보드·i18n 정확도 | React Aria + W3C APG | [behavior-hooks.md](references/behavior-hooks.md) |
| 저수준 유틸 (floating, scroll lock, focus trap) | floating-ui, react-remove-scroll | [behavior-hooks.md](references/behavior-hooks.md) |
| recipe / variant 스타일 시스템 | Panda, Chakra v3 | [styling-recipes.md](references/styling-recipes.md) |
| snippet registry · CLI 배포 | shadcn/ui | [styled-systems.md](references/styled-systems.md) |
| 완성형 컴포넌트 조립 방식 | shadcn, Park UI, Chakra v3 | [styled-systems.md](references/styled-systems.md) |
| 대규모·멀티플랫폼 시스템 운영 | React Spectrum, Astryx | [platform-systems.md](references/platform-systems.md) |
| 토큰 파이프라인 / DTCG | Style Dictionary, DTCG spec | [token-infra.md](references/token-infra.md) |
| 문서 사이트 구조·IA | (사이트별 비교) | [docs-sites.md](references/docs-sites.md) |
| 모션·디자인 원칙 맥락 주입 | **설치된 스킬 우선** | [skill-collections.md](references/skill-collections.md) |
| 레퍼런스들 최근 업데이트 | — | 아래 5번 절차 |

**교차 검증 룰**: 새 컴포넌트를 설계할 때는 최소 2개 소스를 비교한다. 한 라이브러리의 API를 그대로 베끼면 그 라이브러리의 제약까지 함께 들어온다.

## 2. 컴포넌트 인덱스

찾는 컴포넌트가 있으면 **해당 lookup 파일 하나만** 읽는다.

| 컴포넌트 | 파일 |
| --- | --- |
| Select, Combobox, Autocomplete | [lookup-inputs.md](references/lookup-inputs.md) |
| DatePicker, Calendar, DateInput | [lookup-inputs.md](references/lookup-inputs.md) |
| OTP, PinInput | [lookup-inputs.md](references/lookup-inputs.md) |
| NumberField, 숫자 애니메이션 | [lookup-inputs.md](references/lookup-inputs.md) |
| Slider, RangeSlider | [lookup-inputs.md](references/lookup-inputs.md) |
| FileUpload, Dropzone | [lookup-inputs.md](references/lookup-inputs.md) |
| Field, Form, 유효성 검사 | [lookup-inputs.md](references/lookup-inputs.md) |
| Dialog, AlertDialog, Modal | [lookup-overlays.md](references/lookup-overlays.md) |
| Drawer, BottomSheet | [lookup-overlays.md](references/lookup-overlays.md) |
| Menu, DropdownMenu, ContextMenu | [lookup-overlays.md](references/lookup-overlays.md) |
| Toast, Snackbar | [lookup-overlays.md](references/lookup-overlays.md) |
| Tooltip, Popover, HoverCard | [lookup-overlays.md](references/lookup-overlays.md) |
| focus trap · scroll lock 유틸 | [lookup-overlays.md](references/lookup-overlays.md) |
| Carousel, Slider(캐러셀) | [lookup-collections.md](references/lookup-collections.md) |
| Tabs, SegmentedControl | [lookup-collections.md](references/lookup-collections.md) |
| Accordion, Collapsible, Disclosure | [lookup-collections.md](references/lookup-collections.md) |
| 가상 스크롤 (Virtual), 무한 목록 | [lookup-collections.md](references/lookup-collections.md) |
| Table, DataGrid | [lookup-collections.md](references/lookup-collections.md) |
| Command, CommandPalette | [lookup-collections.md](references/lookup-collections.md) |
| TreeView, Listbox | [lookup-collections.md](references/lookup-collections.md) |

없는 컴포넌트라면 [state-machines.md](references/state-machines.md)의 Zag 머신 목록과 [headless-primitives.md](references/headless-primitives.md)의 Base UI 목록부터 확인한다. 둘의 커버리지가 가장 넓다.

## 3. 코드 가져오는 법

경로는 **패턴이지 보증이 아니다.** 아래 순서로 내려간다.

1. **단일 파일** — raw URL을 WebFetch:
   `https://raw.githubusercontent.com/{org}/{repo}/{branch}/{path}`
   브랜치는 레포마다 다르다. 각 엔트리의 `branch:` 값을 쓸 것 (`main`이 아닌 곳이 많다: base-ui·embla·floating-ui·input-otp는 `master`, seed-design은 `dev`, TanStack/table은 `beta`).
2. **404거나 디렉토리 목록이 필요할 때** — 리스팅으로 재발견:
   `gh api repos/{org}/{repo}/contents/{path} --jq '.[].name'`
3. **본격 탐색 (여러 파일을 훑어야 할 때)** — scratchpad에 부분 클론:
   ```bash
   git clone --depth 1 --filter=blob:none --sparse https://github.com/{org}/{repo}.git
   cd {repo} && git sparse-checkout set {dir}
   ```
4. **크로스 레포 패턴 검색** — `gh search code '<query>' --repo {org}/{repo}`

### Staleness 규칙

경로가 404를 내면 그건 이 문서가 낡은 것이다. 2번으로 재발견한 뒤 **이 스킬의 해당 엔트리를 고쳐라.** 고치지 않으면 다음에 또 같은 404를 만난다.

## 4. seed-design 레포에서 쓸 때

- **차용 여부 판단**은 이 스킬이 아니라 레포 스킬이 정본이다: `skills/create-component/references/external-references.md`. 충돌하면 레포 쪽을 따른다. 이 스킬은 "어디에 무엇이 있고 어떻게 읽는가"만 담당한다.
- 구현 전에 **`packages/react-headless/`의 기존 포팅 귀속 헤더**를 먼저 확인한다. 파일 1행에 `// This code includes portions derived from …` 형식으로 출처가 적혀 있고, 이미 포팅된 것을 다시 설계하면 낭비다.

## 5. 업데이트 다이제스트

"지난 한 달 레퍼런스 업데이트 뭐 있었어?" 같은 요청 절차.

1. 대상 레포 목록 추출 — 각 참조 파일의 `repo:` 고정 라인이 단일 출처다. 이 스킬이 설치된 디렉토리의 `references/`에 대고 실행한다:
   ```bash
   grep -rh '^repo:' <이 스킬 디렉토리>/references/ | sed 's/^repo: *//' | sort -u
   ```
2. 레포별 릴리스 확인 (기본 기간 30일):
   ```bash
   gh api repos/{org}/{repo}/releases --jq '.[] | select(.published_at > "YYYY-MM-DD") | "\(.tag_name) \(.published_at[0:10])"'
   ```
   릴리스를 안 쓰는 레포는 커밋으로:
   `gh api "repos/{org}/{repo}/commits?since=YYYY-MM-DD" --jq 'length'`
3. 문서 사이트는 각 엔트리의 `updates:` URL을 WebFetch.
4. 출력: 레포별 주요 변경 1~2줄. **변경 없는 곳은 생략**한다 (없음을 나열하지 말 것).

기간이 명시되지 않으면 30일. 대상이 많으므로 릴리스 조회는 병렬로 묶어 실행한다.

## 6. 참조 파일

| 파일 | 담는 것 | 언제 읽는가 |
| --- | --- | --- |
| [lookup-inputs.md](references/lookup-inputs.md) | 입력 계열 컴포넌트별 판정+포인터 | Select/DatePicker/OTP/Slider/FileUpload 등을 만들 때 |
| [lookup-overlays.md](references/lookup-overlays.md) | 오버레이 계열 + focus/scroll 유틸 | Dialog/Drawer/Menu/Toast/Tooltip을 만들 때 |
| [lookup-collections.md](references/lookup-collections.md) | 컬렉션 계열 | Carousel/Tabs/Table/Virtual/Command를 만들 때 |
| [headless-primitives.md](references/headless-primitives.md) | 헤드리스 라이브러리 레포 맵 | 훅 API·컴파운드 구조를 설계할 때 |
| [state-machines.md](references/state-machines.md) | Zag 상태머신 | 프레임워크 무관 로직이 필요할 때 (Lynx 등) |
| [behavior-hooks.md](references/behavior-hooks.md) | 저수준 훅·유틸 | ARIA/i18n 정확도, floating·focus·scroll 처리 |
| [styling-recipes.md](references/styling-recipes.md) | recipe/variant 스타일 레이어 | 스타일 API·variant 스키마를 설계할 때 |
| [styled-systems.md](references/styled-systems.md) | 완성형 시스템·registry | 조립 방식·배포(CLI/registry)를 볼 때 |
| [platform-systems.md](references/platform-systems.md) | 대형·멀티플랫폼 시스템 | 시스템 운영·다중 플랫폼 전략을 볼 때 |
| [token-infra.md](references/token-infra.md) | 토큰 파이프라인·DTCG | 토큰 빌드/스펙을 설계할 때 |
| [docs-sites.md](references/docs-sites.md) | 문서 사이트 IA | 문서 구조를 짤 때 |
| [skill-collections.md](references/skill-collections.md) | 디자인 스킬 레포 카탈로그 | 분야 맥락 주입·새 스킬을 찾을 때 |

*실측 기준: 2026-08-02. 별 수·최근 푸시 등은 그때의 값이다.*
