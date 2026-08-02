## skills

### MindPalace 지식 체계

Obsidian vault의 `MindPalace/` 폴더 아래에 지식을 구조적으로 축적하고 검색하는 스킬 묶음.

#### mind-palace

대화 중 얻은 범용 지식, 교훈, 인사이트를 저장한다. (`MindPalace/Lessons/`, `Insights/`, `Principles/`, `Inbox/`)

```bash
npx skills add https://github.com/junghyeonsu/skills --skill mind-palace
```

#### mind-palace-recall

저장된 MindPalace 지식을 대화 맥락에 맞게 검색하고 활용한다.

```bash
npx skills add https://github.com/junghyeonsu/skills --skill mind-palace-recall
```

#### linear-collab

```bash
npx skills add https://github.com/junghyeonsu/skills --skill linear-collab
```

#### wrap-up

```bash
npx skills add https://github.com/junghyeonsu/skills --skill wrap-up
```

### Knowledge Lint

```bash
npx skills add https://github.com/junghyeonsu/skills --skill knowledge-lint
```

### UI 레퍼런스

#### ui-references

컴포넌트나 헤드리스 훅을 만들 때 **어떤 오픈소스를 참고할지** 찾고, 그 소스를 바로 fetch해서 읽는다. 코드를 복사해 두지 않고 `org/repo` + 경로 포인터만 담는 방식이다.

- 컴포넌트별 판정 — Select/DatePicker/OTP/Carousel/Toast 등, 1순위와 "갈리는 지점"
- 레포 맵 — Base UI, Radix, Zag, React Aria, Panda, shadcn, Spectrum, Astryx, Style Dictionary 등 38개
- 문서 사이트 IA — llms.txt 유무와 문서 구조 비교
- 디자인 스킬 카탈로그 + 레퍼런스들의 최근 업데이트 모아보기

```bash
npx skills add https://github.com/junghyeonsu/skills --skill ui-references
```

포인터가 낡지 않았는지는 스크립트로 확인한다 (레포 브랜치 대조 + URL 200 + 코드 경로 실존):

```bash
bash skills/ui-references/evals/verify-refs.sh
```