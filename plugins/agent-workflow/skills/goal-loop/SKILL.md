---
name: goal-loop
description: "여러 단계의 구현·마이그레이션·디자인·리서치 작업을 목표 중심으로 끝까지 실행하고 verify-outcome과 learn-from-work을 자동으로 함께 수행한다. 명시적인 goal 요청, 야간 작업, 중단 작업 재개에서 범위·권한·실제 검증·체크포인트를 유지하고 추가 전에 삭제와 재사용을 고려할 때 사용한다. 단순 질문과 작은 수정에는 적용하지 않는다."
---

# Goal loop

Use the host's tools and lifecycle. Read [the host adapter](references/hosts.md) for goal operations. This skill defines a workflow; it does not provide a scheduler or tool permissions.

## Run the complete workflow

`goal-loop` is the single entry point for execution, verification, and learning. At the start, read both bundled companions: [verify-outcome](../verify-outcome/SKILL.md) and [learn-from-work](../learn-from-work/SKILL.md), resolving paths from this skill's directory. Apply their instructions within the current workflow automatically; do not wait for separate user invocations or rely on implicit skill discovery. Load their supporting references only when relevant.

Use `verify-outcome` at meaningful implementation checkpoints and before completion. Apply `learn-from-work` when a meaningful correction or unexpected failure occurs, and perform its learning review before the final handoff. If there is no meaningful reusable finding, create no lesson or rule. These phases retain the task's existing scope and authorization.

## Establish the finish line

Recover the latest human instructions and relevant project decisions. Write a short completion contract for substantial work using [this template](references/goal-contract.md). Reuse an existing plan or task record; do not create a second document with the same content. For a short task, keep the contract in the reply.

The contract must identify the result, **every required deliverable**, checks in the actual target environment, exclusions, existing authorization, conditional authorization, and the next unresolved step. Link the plan's items to their evidence. A passing subset is not the original goal's completion.

Observe what the tools can answer before asking the user. Continue authorized, reversible work without repeatedly seeking confirmation. Resolve genuine product preferences or missing authorization only when they affect the next action. Preserve authorization across turns; green CI does not itself authorize commit, push, merge, publish, or messages to other people.

## Execute one observable slice

1. Inspect the existing producer, consumers, reference implementations, and runtime. Reproduce a reported defect before choosing its fix. For an investigation, gather evidence without turning it into an unsolicited implementation.
2. Ask what can be removed or reused before introducing a wrapper, service, table, dependency, compatibility layer, container, or internal versioned filename. Check actual callers and public compatibility. Deletion is a design option, not authorization to destroy data or user changes.
3. Make the smallest slice that reaches the real user flow. Keep the **full agreed scope** visible; slicing is execution order, not scope reduction. Avoid renaming or refactoring unrelated code.
4. Apply the verification workflow in `../verify-outcome/SKILL.md`. Inspect the outcome, not only a successful command. Fix a failed check without hiding the violation or lowering its requirement to obtain green.
5. Checkpoint the observed result, remaining difference, blocker, and exact next step. Continue independent work if one integration is unavailable. Do not keep creating containers or infrastructure for the same missing dependency; inventory and reuse existing resources first.

Use existing domain skills when relevant: project verification and coding guidance; xref and UI/motion skills for interface work. Do not duplicate them here or prescribe one UI stack for every repository.

## Resume and finish

After interruption or compaction, read the checkpoint, then verify current branch/head, dirty files, runtime availability, and pending authorization. Use evidence from the current relevant inputs and deployment. Never restart the entire task merely because the conversation was compacted.

Use native goal tools only when the human explicitly requests a goal. Do not infer a goal registration from a normal task or a mention of the word goal. Do not invent a token budget. Follow the host's rules for pause, completion, blockers, and budgets.

Before marking complete, compare the contract with the final implementation and perform `verify-outcome`, followed by the `learn-from-work` review. If learning changes code, checks, or task artifacts, re-verify the affected final result before completion. Finish only after verification supports the agreed scope and the learning review is done. If the user explicitly excluded unavailable integrations, finish the agreed subset and list those integrations as deferred with requirements. Otherwise they remain outstanding; do not quietly rewrite the goal.

Learning can stay a candidate; writing a rule is not proof that the next agent obeys it. Include relevant verification results and adopted learning in the final report without inventing an empty lesson.

Report concisely in Korean by default: result, meaningful AS IS → TO BE, verified evidence, remaining work or next action. Link the decisive evidence and decisions actually used. PR titles use English Conventional Commit style. Do not include private chain-of-thought; record observable decisions and their consequences.
