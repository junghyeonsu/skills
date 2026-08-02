#!/usr/bin/env bash
# ui-references 스킬의 모든 포인터를 실측 검증한다.
#   1) repo: 라인의 레포가 존재하고, 기록된 branch가 실제 기본 브랜치인지
#   2) 문서에 박힌 raw.githubusercontent URL이 200인지
#   3) 코드 경로 패턴(components:/machines: 등)이 실존하는지
# 사용: bash verify-refs.sh
set -uo pipefail
# 스크립트 위치 기준 (설치 경로와 무관하게 동작)
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF="$SKILL/references"
fail=0

echo "===== 1. repo: 라인 / 기본 브랜치 대조 ====="
# "repo: org/repo" 수집
repos=$(grep -rh '^repo: ' "$REF" | sed 's/^repo: *//' | tr -d '\r' | sort -u)
for r in $repos; do
  actual=$(gh api "repos/$r" --jq .default_branch 2>/dev/null)
  if [ -z "$actual" ]; then
    echo "  MISSING REPO: $r"; fail=$((fail+1)); continue
  fi
  # 같은 블록 안에 branch: 가 있으면 대조 (없으면 기본 브랜치 사용 가정)
  declared=$(grep -rA6 "^repo: $r\$" "$REF" | grep -m1 '^[^ ]*[-:]*branch: ' | sed 's/.*branch: *//' | awk '{print $1}' | tr -d '\r')
  if [ -n "$declared" ] && [ "$declared" != "$actual" ]; then
    echo "  BRANCH MISMATCH: $r  문서=$declared  실제=$actual"; fail=$((fail+1))
  else
    printf "  ok  %-42s %s\n" "$r" "$actual"
  fi
done

echo
echo "===== 2. raw.githubusercontent URL ====="
# {org}/{repo} 같은 템플릿 예시는 제외
urls=$(grep -rhoE 'https://raw\.githubusercontent\.com/[^ )`]+' "$SKILL" | tr -d '`' | grep -v '{' | sort -u)
for u in $urls; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 "$u")
  if [ "$code" = "200" ]; then printf "  ok   %s\n" "$u"
  else echo "  FAIL($code) $u"; fail=$((fail+1)); fi
done

echo
echo "===== 3. 문서 사이트 llms.txt ====="
for u in $(grep -rhoE '^llms: https://[^ ]+' "$REF" | sed 's/^llms: *//' | sort -u); do
  code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 "$u")
  ct=$(curl -sI -L --max-time 20 "$u" | grep -i '^content-type' | tail -1 | tr -d '\r')
  case "$ct" in *text/plain*) ok=yes;; *) ok=no;; esac
  if [ "$code" = "200" ] && [ "$ok" = "yes" ]; then printf "  ok   %s\n" "$u"
  else echo "  FAIL($code, $ct) $u"; fail=$((fail+1)); fi
done

echo
echo "===== 4. 핵심 코드 경로 실존 ====="
# "org/repo<TAB>path" 목록. 문서에서 실제로 안내하는 대표 포인터들.
while IFS=$'\t' read -r r p; do
  [ -z "$r" ] && continue
  out=$(gh api "repos/$r/contents/$p" 2>/dev/null | head -c 120)
  case "$out" in
    \[*) printf "  ok(dir)   %s :: %s\n" "$r" "$p" ;;
    \{\"name*|*\"type\":\ \"file\"*) printf "  ok(file)  %s :: %s\n" "$r" "$p" ;;
    *) echo "  FAIL      $r :: $p"; fail=$((fail+1)) ;;
  esac
done <<'PATHS'
mui/base-ui	packages/react/src/combobox
mui/base-ui	packages/react/src/otp-field
mui/base-ui	packages/react/src/use-render
mui/base-ui	packages/react/src/merge-props
radix-ui/primitives	packages/react/roving-focus/src
radix-ui/primitives	packages/react/one-time-password-field/src
radix-ui/primitives	packages/react/dismissable-layer/src
chakra-ui/zag	packages/machines/file-upload/src/file-upload.connect.ts
chakra-ui/zag	packages/machines/tree-view/src
chakra-ui/zag	packages/machines/listbox/src
guilhermerodz/input-otp	packages/input-otp/src/input.tsx
pacocoursey/cmdk	cmdk/src/index.tsx
emilkowalski/vaul	src/index.tsx
emilkowalski/sonner	src/index.tsx
davidjerleke/embla-carousel	packages/embla-carousel/src/components
TanStack/virtual	packages/virtual-core/src/index.ts
floating-ui/floating-ui	packages/core/src/middleware
facebook/astryx	packages/core/src/CommandPalette
facebook/astryx	packages/cli
chakra-ui/panda	packages/core/src/recipes.ts
chakra-ui/chakra-ui	packages/react/src/theme/recipes
shadcn-ui/ui	apps/v4/registry/bases/radix
shadcn-ui/ui	apps/v4/registry/new-york-v4/ui
adobe/react-spectrum	packages/@internationalized/date/src
adobe/react-spectrum	packages/react-aria/src/interactions/usePress.ts
adobe/react-spectrum	packages/react-stately/src/combobox
amzn/style-dictionary	lib/common/transforms.js
PATHS

echo
echo "===== 결과: 실패 $fail 건 ====="
exit $fail
