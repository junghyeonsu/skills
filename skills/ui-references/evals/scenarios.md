# ui-references 라우팅 eval

스킬이 **의도대로 읽히는지** 검증한다. 핵심 실패 모드는 두 가지다.

- **과소 라우팅**: 스킬이 아예 안 걸리거나, 엉뚱한 파일로 감
- **과잉 로딩**: 답에 필요 없는 참조 파일까지 읽음 (retrieval 분할이 무의미해짐)

`references/`를 고치거나 파일을 쪼갤 때마다 돌린다.

## 실행 방법

각 시나리오의 프롬프트를 **서브에이전트**에 그대로 준다. 스킬을 쓸 수 있게 하되, 어떤 파일을 읽으라고 지시하지 말 것 — 라우팅 자체가 검사 대상이다.

```
Task(subagent_type: "general-purpose", prompt: "<시나리오 프롬프트>")
```

끝나면 트랜스크립트에서 **실제로 Read한 파일 목록**과 **fetch한 URL**을 뽑아 아래 기대치와 대조한다.

## 채점 기준 (3개 전부 통과해야 pass)

| # | 기준 |
| --- | --- |
| A | 기대 파일을 읽었는가 |
| B | **기대 외 참조 파일을 읽지 않았는가** (1개라도 추가로 읽으면 fail) |
| C | 답의 근거가 스킬 내용인가 (모델의 사전지식으로 때우지 않았는가) |

SKILL.md는 라우터이므로 어느 시나리오에서든 읽어도 된다. B의 카운트 대상은 `references/` 파일이다.

---

## 시나리오

### S1. OTP — lookup 단일 파일 도달

> OTP 입력 컴포넌트를 헤드리스로 만들려고 해. 어디를 참고하면 좋을까?

- 기대 읽기: `references/lookup-inputs.md`
- 금지: 다른 lookup 파일, `headless-primitives.md`, `state-machines.md`
- 기대 내용: input-otp가 1순위이고 **투명 input 1개 vs 칸마다 input** 트레이드오프가 언급될 것
- 기대 포인터: `guilhermerodz/input-otp` `packages/input-otp/src/input.tsx`

### S2. Carousel — 다른 패밀리로 안 새는지

> Carousel 패턴 구현 참고할 만한 곳 알려줘.

- 기대 읽기: `references/lookup-collections.md`
- 금지: `lookup-inputs.md`, `lookup-overlays.md`
- 기대 내용: embla 1순위 + **"scroll-snap으로 충분한지 먼저 확인"** 이 나올 것 (이게 빠지면 C 실패로 본다)

### S3. recipe 시스템 — 레포 축 라우팅

> recipe 기반 스타일 시스템을 설계하려는데, 다른 라이브러리들은 어떻게 하고 있어?

- 기대 읽기: `references/styling-recipes.md`
- 금지: lookup 파일들
- 기대 내용: Panda 1순위, CVA는 slot 없음, "recipe가 원천인가 생성물인가" 축이 나올 것

### S4. 문서 구조 — 문서 축 라우팅

> 디자인시스템 문서 사이트 구조 참고할 만한 곳 있어?

- 기대 읽기: `references/docs-sites.md`
- 기대 내용: llms.txt 보유 여부가 사이트별로 갈린다는 점, MCP를 제공하는 chakra 사례
- 기대 포인터: 실제 llms.txt URL 최소 1개 제시

### S5. 모션 — 스킬 컬렉션으로 위임

> 모션 작업할 건데 맥락 좀 잡아줘.

- 통과 조건 (둘 중 하나):
  - 설치된 모션 스킬(`emil-design-eng`, `apple-design` 등)을 직접 호출, **또는**
  - `references/skill-collections.md`를 읽고 어느 스킬을 쓸지 안내
- 실패: `behavior-hooks.md`만 읽고 라이브러리 목록만 답하는 경우 (모션 판단은 이 스킬 소유가 아니다)

### S6. 업데이트 다이제스트 — 절차 실행

> 지난 한 달간 레퍼런스 레포들에 어떤 업데이트가 있었는지 정리해줘.

- 기대 동작: SKILL.md 4번 절차 실행 — `grep '^repo:'`로 목록 추출 → `gh api releases`(또는 커밋 폴백)
- 금지: 참조 파일들을 전부 통독하는 것 (grep으로 충분)
- 기대 내용: **변경 없는 레포는 생략**. Radix처럼 릴리스를 안 쓰는 레포에서 커밋으로 폴백하는지 확인

### S7. 미수록 컴포넌트 — 폴백 경로

> Signature Pad 같은 컴포넌트 만들려는데 참고할 데 있어?

- 기대 동작: 컴포넌트 인덱스에 없음을 확인 → `state-machines.md`(Zag 머신 목록)로 폴백
- 기대 내용: Zag에 `signature-pad` 머신이 있다는 사실 도달
- 실패: "없다"고만 답하는 경우 (SKILL.md 2번의 폴백 지시를 따르지 않은 것)

---

---

## 실행 기록

### 2026-08-02 (최초 작성 직후)

**S1 / S2 / S5 / S6 실행 — 4건 전부 pass. S3·S4·S7 미실행.**

| # | A 기대파일 | B 노이즈없음 | C 스킬근거 |
| --- | --- | --- | --- |
| S1 OTP | `lookup-inputs.md` ✓ | ✓ | ✓ |
| S2 Carousel | `lookup-collections.md` ✓ | ✓ | ✓ (scroll-snap 우선 확인 전달됨) |
| S5 모션 | `skill-collections.md` ✓ | ✓ | ✓ (설치된 스킬로 위임 안내) |
| S6 다이제스트 | grep만 사용 ✓ | ✓ (통독 안 함) | ✓ (Radix는 릴리스 없어 npm/커밋으로 폴백) |

B 판정 대상은 이 스킬의 `references/` 파일이다. 에이전트가 작업 중인 프로젝트의 파일을 읽은 것은 노이즈로 세지 않았다.

**eval이 문서의 사실 오류 2건을 잡았고, 소스로 반증된 뒤 수정됨:**

1. **OTP** — "칸마다 `<input>`을 두면 SMS 자동완성이 깨진다"는 서술이 **틀렸다.** Base UI/Radix는 첫 칸에만 `autoComplete="one-time-code"` + `maxLength={length}`를 걸어 자동완성을 살린다(Base UI `OTPFieldInput.tsx`에 주석까지 있음). 진짜 트레이드오프는 자동완성이 아니라 input-otp의 스타일-로직 결합이었다. → 1순위를 Base UI+Radix로 바꾸고 근거를 교체
2. **Carousel** — embla 핵심 파일로 적어둔 `SnapPoint`가 **실재하지 않았다.** 실제 파일명은 `ScrollSnaps`/`ScrollSnapList`. 기억으로 쓴 파일명은 그럴듯해도 틀린다.

교훈: **검증 없이 쓴 "왜"는 틀릴 수 있다.** 포인터(경로)는 스크립트가 잡지만 판정 근거는 eval이 소스를 읽어야 잡힌다. 새 항목을 추가할 때 근거를 추측으로 쓰지 말 것.

## 포인터 유효성 검사

라우팅과 별개로, 문서에 적힌 경로/URL이 살아 있는지는 스크립트로 본다.

```bash
bash <이 스킬 디렉토리>/evals/verify-refs.sh
```

검사 항목: `repo:` 레포 실존과 선언 브랜치 일치 / raw URL 200 / llms.txt가 진짜 text-plain인지 / 대표 코드 경로 실존. **실패 0이어야 한다.**

레포 구조는 예고 없이 바뀐다 (실제로 2026-08 검증에서 react-spectrum이 `@react-aria/*` → `react-aria/src/*`로, shadcn이 `apps/www` → `apps/v4`로, input-otp가 모노레포로 이동한 것을 잡았다). 분기에 한 번 정도 돌리면 충분하다.
