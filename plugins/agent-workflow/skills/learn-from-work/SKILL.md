---
name: learn-from-work
description: "의미 있는 사용자 교정, 예상 밖의 검증 실패, 반복 작업의 마찰을 범위가 명확한 학습으로 바꾼다. 교훈·결정·임시 상태를 분리하고 검증 가능한 재발 방지 장치로 연결할 때 사용하며, 한 프로젝트의 선택을 전역 규칙으로 일반화하지 않는다."
---

# Learn at the right layer

Read only relevant task evidence and existing learning records. Do not mine unrelated private sessions by default. If no meaningful reusable finding exists, do not create a lesson just to complete a ritual.

## Classify the signal

- **Task state**: missing credential, current failing check, next action. Keep in the task checkpoint.
- **Lesson**: observed failure or success, cause, and a conditional next action. Keep distinct from whether its fix was implemented.
- **Decision**: a chosen direction, alternatives, rationale, scope, and exceptions. Acceptance does not prove final implementation or verification.
- **Reusable mechanism**: repeated failure prevented by architecture, types, lint/CI, a behavioral test, or a small deterministic script. Prefer a mechanism to another instruction.
- **Personal workflow preference**: an explicit durable human preference or consistent evidence across independent tasks. A one-project choice does not become a rule for every project.

Use [the learning template](references/learning.md). Project facts belong in the affected project; task-only observations stay in the checkpoint. Keep personal portable skills about workflow. Select relevant knowledge on demand instead of loading every lesson into each prompt.

## Capture, test, then promote

1. Record the specific observable incident and its scope. Treat pasted plans and repeated inherited/subagent transcripts as context, not independent confirmation.
2. For inferred cross-task policy, find at least two independent examples or an explicit durable human instruction. A serious one-off defect can warrant an immediate **scoped** regression test; repetition is not a requirement to fix it.
3. Write the proposed next action and a counterexample where it should not apply. Resolve contradictions with newer human instructions and actual project constraints.
4. Apply the strongest small mechanism appropriate to the authorized change. Exercise the real failure and a legitimate allowed case. Do not add tests that merely mirror implementation.
5. Reconcile the lesson/decision with the final diff and current evidence. Mark candidate, tested in scope, or accepted; never claim automatic invocation or recurrence reduction from file installation alone.
6. Keep the useful rule small. Replace stale/duplicate instructions once the mechanism covers them. Do not delete explanations still needed for judgment or external compatibility.

Do not edit the host's personal memory store without an explicit human memory-update request. Do not automatically publish private session excerpts, promote project facts to a global skill, write to unrelated repositories, or message other agents/people. Write learning records only within the authorized task or project.

## Measure the next tasks

For the first ten comparable goals, record: corrective human interventions, required items omitted at handoff, environment-relevant evidence coverage, repeated unchanged failures, and unnecessary resources/dependencies introduced. Separate task size and environment blockers. Track wall time or cost when available, but do not optimize tokens by dropping required verification.

Change one workflow mechanism at a time, compare similar work, and keep or remove it based on recurrence and overhead. This is the improvement loop; a growing rule file by itself is not improvement.
