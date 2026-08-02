# 입력 계열 컴포넌트

Select/Combobox, DatePicker, OTP, NumberField, Slider, FileUpload, Field.

각 항목은 자급자족이다 — 판정과 **직접 파일 포인터**까지 여기 있으므로 레포 축 파일을 거치지 않아도 fetch할 수 있다. 브랜치가 `main`이 아닌 곳은 표시했다. 포인터가 404면 [headless-primitives.md](headless-primitives.md) 등 레포 축 파일의 맵으로 재발견한다.

---

## Select / Combobox / Autocomplete

**1순위: Base UI.** 이 셋을 별개 컴포넌트로 분리한 설계가 가장 정돈돼 있다. Select(선택 전용) / Combobox(입력+선택) / Autocomplete(입력 보조)의 경계가 명확하다.

갈리는 지점 — **Select와 Combobox를 하나로 볼 것인가**:
- Base UI: 셋 다 분리. 각각의 키보드 모델이 다르다는 입장
- Radix: Select만 제공, Combobox 없음 (사람들이 cmdk로 때움)
- Zag: `select` / `combobox` 머신 분리 + `listbox`를 별도 primitive로 추출
- React Aria: `combobox` 하나에 `allowsCustomValue` 등 옵션으로 흡수

필터링·비동기 로딩을 다룰 거면 Zag `async-list` 머신을, i18n 정렬(로케일별 문자열 비교)이 중요하면 React Aria를 본다.

포인터:
- `mui/base-ui` (**branch: master**) — `packages/react/src/select/`, `packages/react/src/combobox/`, `packages/react/src/autocomplete/`
- `chakra-ui/zag` — `packages/machines/select/src/select.machine.ts`, `packages/machines/combobox/src/`, `packages/machines/listbox/src/`
- `radix-ui/primitives` — `packages/react/select/src/`
- `adobe/react-spectrum` — `packages/react-aria/src/combobox/useComboBox.ts`, `packages/react-stately/src/combobox/`

SEED: `daangn/seed-design` (**branch: dev**) — `packages/react-headless/select/src/`. Radix FocusScope 연계와 floating 처리에 주석이 많다.

---

## DatePicker / Calendar / DateInput

**1순위: React Aria.** 논쟁의 여지가 거의 없다. 달력은 캘린더 시스템(그레고리력 외), 타임존, 로케일별 주 시작일, 세그먼트 입력 등이 얽혀서 직접 만들면 반드시 틀린다. `@internationalized/date`가 사실상 이 분야의 표준 라이브러리다.

갈리는 지점 — **날짜 값 타입**: React Aria는 `CalendarDate`/`ZonedDateTime` 같은 자체 불변 타입을 쓴다(Date 객체의 타임존 함정 회피). Zag는 같은 `@internationalized/date`를 의존으로 가져다 쓴다. Base UI는 아직 없다.

포인터:
- `adobe/react-spectrum` — `packages/@internationalized/date/src/` (**여기가 핵심**), `packages/react-aria/src/calendar/useCalendar.ts`, `packages/react-aria/src/datepicker/useDateField.ts`, `packages/react-stately/src/datepicker/`
- `chakra-ui/zag` — `packages/machines/date-picker/src/`, `packages/machines/date-input/src/`

SEED: 없음. 만든다면 `@internationalized/date`를 의존으로 쓸지부터 정해야 한다 (번들 크기 vs 정확성).

---

## OTP / PinInput

**1순위: Base UI `otp-field` + Radix `one-time-password-field`** (둘을 나란히). 서로 독립적으로 만들어졌는데 API가 거의 겹친다 — 이 수렴 자체가 신호다.

갈리는 지점 — **입력 요소를 몇 개 둘 것인가**:
- **input-otp = 1개.** 진짜 `<input>` 하나를 투명하게 깔고 그 위에 칸을 그린다. 칸은 순수 표시물이라 커서/선택 영역을 `selectionchange`로 미러링해 직접 계산한다.
- **Base UI / Radix / Zag = 칸마다 1개.** 자동완성은 포기하지 않는다 — 첫 칸에만 `autoComplete="one-time-code"` + `maxLength={length}`를 걸어 iOS SMS 자동완성이 전체 코드를 0번 칸에 쏟게 두고, `onChange`에서 다중 문자를 각 칸으로 분배한다(`replaceOTPValue`). Zag는 `otp: true`일 때 모든 칸에 건다.

즉 "칸마다 input이면 SMS 자동완성이 깨진다"는 건 사실이 아니다. **진짜 대가는 스타일 결합 쪽**이다 — input-otp는 `color/caretColor: transparent`, `letterSpacing: -.5em`, document에 주입하는 `<style>`, iOS 전용 `transform: scale(0.1)` + `text-indent` 리빌 로직까지 스타일과 로직이 분리 불가능하게 얽혀 있다. 스타일 없는 headless 패키지로 뽑아낼 수 없는 구조다.

세 라이브러리가 합의한 prop 이름 (그대로 가져다 쓸 만함): `length`, `validationType: 'numeric' | 'alpha' | 'alphanumeric' | 'none'`, 정규화 escape hatch(Base UI `normalizeValue` / Radix `sanitizeValue`), `autoSubmit`, 완료 콜백(`onValueComplete` / `onAutoSubmit`), `mask`. 폼 제출용 **숨은 input을 따로 둔다**는 것도 공통(칸 input들은 `name`을 갖지 않는다).

포인터:
- `mui/base-ui` (**branch: master**) — `packages/react/src/otp-field/root/OTPFieldRoot.tsx`, `input/OTPFieldInput.tsx`(키보드·paste 전량), **`utils/otp.ts`**(normalize/replace/remove 순수 함수 — 여기부터 읽으면 빠르다). 파트는 Root + Input 둘뿐이고 Separator는 공용 컴포넌트를 재사용
- `radix-ui/primitives` — `packages/react/one-time-password-field/src/one-time-password-field.tsx` (roving tabindex를 `@radix-ui/react-roving-focus`로 위임, `HiddenInput`을 별도 파트로 노출)
- `chakra-ui/zag` — `packages/machines/pin-input/src/pin-input.machine.ts`, `pin-input.connect.ts`. anatomy = `root/label/input/control`. `blurOnComplete`, `selectOnFocus` 같은 부가 옵션이 여기만 있다
- `guilhermerodz/input-otp` (**branch: master**) — `repo: guilhermerodz/input-otp` — `packages/input-otp/src/input.tsx`. **차용용이 아니라 iOS/PWM 함정 카탈로그로 읽을 것** — 주석에 실측 근거(edit menu가 400ms엔 죽고 1500ms엔 살더라 등)가 남아 있다. `use-pwm-badge.tsx`는 비밀번호 관리자 배지 회피

SEED: 없음. `packages/react-headless/`의 "스타일 로직 금지" 규칙 때문에 input-otp 방식은 채택 불가 — Base UI/Radix 계열이 사실상 유일한 선택지다.

---

## NumberField / 숫자 표시

**1순위: React Aria** (`useNumberField`). 숫자 입력은 로케일마다 소수점·천 단위 구분자·아라비아 숫자 표기가 달라서 `Intl.NumberFormat` 파싱이 필수다. 스테퍼 버튼의 길게 누르기 반복도 여기 구현이 정석.

값이 바뀔 때 자릿수 애니메이션이 필요하면 **number-flow**가 별개 답이다 (구현이 아니라 표시 레이어).

포인터:
- `adobe/react-spectrum` — `packages/react-aria/src/numberfield/useNumberField.ts`, `packages/react-stately/src/numberfield/useNumberFieldState.ts` (파싱 로직)
- `chakra-ui/zag` — `packages/machines/number-input/src/`
- `mui/base-ui` (master) — `packages/react/src/number-field/`
- `barvian/number-flow` — `repo: barvian/number-flow` — 숫자 전환 애니메이션 전용

SEED: `daangn/seed-design` (dev) — `packages/react-headless/quantity-picker/src/` (수량 조절 UI, 범용 NumberField와는 다름)

---

## Slider / RangeSlider

**1순위: Radix** (SEED가 이미 포팅한 계보). 다중 thumb, 스텝 스냅, 키보드 증감, RTL 처리가 검증돼 있다.

갈리는 지점 — **다중 thumb 지원 방식**: Radix는 `value` 배열로 thumb 개수를 결정. React Aria는 `useSliderThumb`를 thumb마다 호출하는 구조. 후자가 thumb별 라벨/제약을 다르게 주기 쉽다.

포인터:
- `radix-ui/primitives` — `packages/react/slider/src/slider.tsx`
- `adobe/react-spectrum` — `packages/react-aria/src/slider/useSlider.ts`, `useSliderThumb.ts`
- `chakra-ui/zag` — `packages/machines/slider/src/`, `packages/machines/angle-slider/src/` (원형 슬라이더)
- `mui/base-ui` (master) — `packages/react/src/slider/`

SEED: `daangn/seed-design` (dev) — `packages/react-headless/slider/src/useSlider.ts` — **Radix 포팅 + 확장**. 파일 1행에 귀속 헤더가 있고, `useElementSizesMap.ts`는 Radix `useSize`를 여러 요소용으로 확장한 것이다. 여기 손대기 전에 원본과 대조할 것.

---

## FileUpload / Dropzone

**1순위: Zag** `file-upload` 머신. 드래그앤드롭 상태, 파일 검증(크기/타입/개수), 거부 사유 분류가 머신으로 정리돼 있다.

갈리는 지점 — **검증 실패를 어떻게 알릴 것인가**: Zag는 `rejectedFiles`에 사유 코드(`FILE_TOO_LARGE` 등)를 담아 넘긴다. 직접 만들면 이 분류를 빠뜨리기 쉽다.

포인터:
- `chakra-ui/zag` — `packages/machines/file-upload/src/file-upload.connect.ts`, `file-upload.machine.ts`
- `chakra-ui/ark` — `packages/react/src/components/file-upload/`

SEED: `daangn/seed-design` (dev) — `packages/react-headless/file-upload/src/useFileUpload.ts` — **Zag 참조 이력이 주석에 명시**돼 있다(`// see: .../zag/.../file-upload.connect.ts`). 관련 컴포넌트로 `attachment-display`도 있다.

---

## Field / Form / 유효성 검사

**1순위: Base UI** `Field` + `Form`. 라벨·설명·에러 메시지와 컨트롤의 연결(`aria-describedby`, `aria-invalid`)을 컴포넌트 레벨에서 자동화한 설계가 가장 깔끔하다. 이걸 각 컴포넌트가 개별로 처리하면 반드시 어긋난다.

갈리는 지점 — **에러 상태의 소유자**: Base UI는 Field가 소유하고 자식 컨트롤이 구독. Radix `Form`은 네이티브 제약 검증(`ValidityState`)에 붙는다. React Aria는 각 훅이 `validationState`를 받는 분산형.

포인터:
- `mui/base-ui` (master) — `packages/react/src/field/`, `packages/react/src/form/`, `packages/react/src/fieldset/`
- `radix-ui/primitives` — `packages/react/form/src/`
- `adobe/react-spectrum` — `packages/react-aria/src/form/`

SEED: `daangn/seed-design` (dev) — `packages/react-headless/field/src/`, `fieldset/`, `text-field/`, `field-button/`
