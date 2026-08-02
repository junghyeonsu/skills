## skills

Claude Code용 커스텀 스킬 모음.

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
