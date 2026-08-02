# 디자인 스킬 컬렉션

디자인·모션 분야의 **에이전트 스킬 레포** 카탈로그. 코드 레퍼런스가 아니라 "맥락을 주입해 주는 스킬"이 어디 있는지 추적한다.

**이 파일의 역할은 카탈로그와 출처 추적까지다.** 설치된 스킬의 내용은 그 스킬 자신이 정본이므로 여기 요약하지 않는다. 모션 판단이 필요하면 이 파일을 읽지 말고 해당 스킬을 직접 호출할 것.

아래 표의 "설치됨" 열은 이 스킬을 쓰는 환경 기준이며 2026-08-02에 확인한 값이다. 현재 상태는 `ls ~/.claude/skills/`로 다시 확인할 것.

---

## emilkowalski/skills

Emil Kowalski(sonner·vaul 제작자). 모션과 UI 크래프트 중심.

```
repo: emilkowalski/skills
branch: main
skills: skills/<name>/SKILL.md
install: npx skills add emilkowalski/skills
updates: https://github.com/emilkowalski/skills/releases
```

| 스킬 | 커버리지 | 설치됨 |
| --- | --- | --- |
| `emil-design-eng` | UI 폴리시·컴포넌트 설계·애니메이션 판단의 철학 | ✅ |
| `apple-design` | Apple식 제스처·스프링·물성을 웹으로 옮기기 | ✅ |
| `animation-vocabulary` | 모션 효과의 이름을 역으로 찾기 ("통통 튀는 그거" → Pop in) | ✅ |
| `find-animation-opportunities` | 애니메이션이 없지만 있어야 할 곳 탐색 (읽기 전용) | ✅ |
| `improve-animations` | 코드베이스 모션 감사 + 실행 계획 산출 | ✅ |
| `review-animations` | 모션 코드 리뷰 (높은 기준으로 flag) | ✅ |
| `prototype` | 여러 버전을 만들어 시각적으로 비교 | ✅ |
| `pick-ui-library` | 작업별 라이브러리 추천 (숫자·OTP·차트·커맨드·가상화 등) | ❌ **미설치** |

**언제 참고**: 모션 작업의 맥락 주입, 애니메이션 값 결정, UI 디테일 판단.

### `pick-ui-library`와 이 스킬의 경계

영역이 겹치므로 구분해 둔다:

- `pick-ui-library` = **무엇을 설치할까** (제품 선택. 큐레이션된 추천)
- `ui-references`(이 스킬) = **어떻게 구현할까** (소스를 어디서 읽고 무엇을 참고할까. 포인터+fetch)

둘 다 유용하고 충돌하지 않는다. 라이브러리를 고르는 단계면 `pick-ui-library`, 고른 뒤(또는 직접 만들기로 한 뒤) 구현을 파는 단계면 이 스킬이다. 설치하려면 `npx skills add emilkowalski/skills --skill pick-ui-library`.

---

## jakubkrehel/skills (interfaces)

인터페이스 크래프트 전 분야를 6개 도메인 + 1개 오케스트레이터로 나눈 컬렉션.

```
repo: jakubkrehel/skills
branch: main
skills: skills/<name>/SKILL.md
install: npx skills add jakubkrehel/skills   (또는 플러그인: /plugin marketplace add jakubkrehel/skills)
updates: https://github.com/jakubkrehel/skills/releases
```

| 스킬 | 커버리지 | 설치됨 |
| --- | --- | --- |
| `better-interface` | 오케스트레이터. 6개 도메인을 순서대로 돌려 하나의 리뷰로 통합 | ❌ |
| `better-accessibility` | 포커스·키보드·ARIA·폼·스크린리더·히트영역·모션 | ❌ |
| `better-layout` | 그룹핑·정렬·간격·반응형·논리 속성·RTL | ❌ |
| `better-writing` | UX 라이팅 (버튼 라벨, 에러, 빈 상태, 설정) | ❌ |
| `better-typography` | 폰트 선택·스케일·줄바꿈·문장부호·가변폰트 | ❌ |
| `better-colors` | OKLCH·팔레트 생성·대비(APCA/WCAG)·gamut·테마 | ❌ |
| `better-ui` | 시각 폴리시 (radius·그림자·아이콘·모션) | ❌ |

전부 미설치. **`better-colors`는 토큰 팔레트를 만들 때, `better-accessibility`는 헤드리스 컴포넌트를 만들 때 특히 맞물린다** — 필요하면 그때 개별 설치하는 게 낫다(`--skill better-colors` 식).

### 구조에서 배울 점

이 레포는 내용보다 **작성 구조**가 참고할 만하다 (`AGENTS.md`에 명문화돼 있음):

- **rule ownership 매트릭스** — 각 규칙은 정확히 한 스킬에만 산다. 경계 케이스를 미리 판정해 둔다(대비는 a11y가 "필요한가"를, colors가 "측정·수정"을 소유하는 식). 교차 참조는 상대 경로가 아니라 스킬 이름으로만
- **값 + 탈출 조건을 같은 자리에** — "scale은 항상 0.96"처럼 정확한 값을 박되, 휴리스틱에는 언제 안 지켜도 되는지를 함께 쓴다("padding이 24px 넘으면 별개 surface로 취급")
- **"스킬이 로드됐다는 이유로 적용하지 마라"** — 프로젝트의 기존 관습을 존중하라는 지시를 반복 주입한다
- **리뷰 산출물 규약** — finding 상한, 근본원인 1개=finding 1개, "검토했지만 기각한 후보" 표 필수, 검증 못 한 건 `Not verified` 라벨(검증 갭을 finding으로 둔갑시키지 않기)

---

## 새 컬렉션 찾기

- **skills.sh** — 스킬 레포 디렉토리. 새 컬렉션 탐색용
- `gh search repos "claude skills" --sort stars` — 레포 검색

수록 기준: **디자인·UI·모션 관련만.** 범용 프로세스 스킬(테스트, 디버깅, 워크플로)은 여기 담지 않는다.
