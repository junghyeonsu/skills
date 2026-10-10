---
name: verify-outcome
description: "구현·리서치가 끝났다고 보고하기 전에 합의한 완료 조건과 실제 대상 환경을 검증한다. goal 체크포인트, 런타임 버그, 여러 소비 경로 변경, UI·네이티브·플러그인 작업, PR·배포 인계, 최종 코드와 교훈·결정 대조에 사용한다."
---

# Verify the observable result

Read the existing task contract and project verification instructions. Prefer the project's established harness. This skill fills completion gaps; it does not replace domain checks.

## Match the claim to the evidence

- Separate implementation, verification, and shipping. Local test success is local test success; it does not establish remote CI, deployment, native rendering, or Figma insertion.
- Re-run the original user scenario. A runtime rendering bug requires that runtime; unit tests and compilation do not close it. Cover relevant failures and boundaries, not only the happy path.
- For producer/consumer changes, trace the actual server/data contract and affected web, admin, plugin, or native paths. Do not patch one schema solely to silence TypeScript.
- For UI comparison, record reference, actual artifact, viewport, DPR/capture size, theme, font/runtime version, and important interactions. Differing conditions cannot support a pixel-equality claim. A screenshot alone does not establish click, persistence, permissions, or submission behavior.
- For deployment, record the observed build/SHA, URL, time, and representative target flow. A health endpoint alone does not establish a protected claim or write flow.
- For research, deliver all requested axes and the readable artifact with attributable sources. Mark observed, reported, and inferred results separately. A later slide deck does not substitute for an unfinished requested report.

Use [the evidence template](references/evidence.md). Attach real paths or URLs, commands, exit codes, subjects, and observations. Mark failed, skipped, unavailable, and unverified checks honestly. Do not broaden/repeat passing tests without a new change or unresolved concern.

## Preserve evidence validity

Tie evidence to the relevant inputs: git head plus dirty state, scoped source content, document revision, capture conditions, or deployed SHA. Re-check affected evidence after those inputs change. Do not treat a successful earlier run as a check of a new final diff.

For local commands, optionally use `scripts/check_receipt.py` to run a command and record scoped input hashes. Run `verify` afterward to catch stale or failed receipts. Read its `--help` first. It is a mechanical freshness guard, **not** a validator of the application, evidence coverage, or human authorization. It checks only the explicitly selected files and an exit code; screenshot meaning, remote builds, environment settings, and dependencies need separate checks. Never use it to capture credentials or secrets.

## Close the contract

Compare every required item against final evidence. Compare affected decisions and lessons with the final diff: accepted direction, implementation, and validation are separate facts. Record the current PR head in the final review or check output; avoid committing a file that attempts to contain its own final commit SHA.

For a shipping action already authorized by the human, verify its actual conditions against the current head. Report any unresolved required check, review, or mergeability state as unresolved. Green checks are not a replacement for merge authorization.

Report what changed, what actually passed, material limits, and remaining items. Only then can the host's goal be marked complete for the agreed scope.
