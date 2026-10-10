# Learning and decision records

Use the repository's existing `.agents/learnings` and `.agents/decisions` conventions when present. Do not introduce a parallel knowledge system. Otherwise keep a small local task record until promotion is justified.

```markdown
Kind: lesson / decision / personal preference / task state
Status: candidate / tested-in-scope / accepted / superseded
Scope and trigger:
Observation: incident + evidence reference, not an invented causal account
Cause: observed / inferred / unknown
Next action or chosen direction:
Alternatives / trade-off, for decisions:
Does not apply when:
Independent support or explicit human instruction:
Mechanism: code / types / lint-CI / behavioral test / skill guidance
Implemented in:
Validated on: subject + command/scenario + result + evidence
Unverified:
Replaces / conflicts with:
```

Do not conflate these claims:

| Claim | Needed evidence |
| --- | --- |
| A lesson is supported | The incident and conditional conclusion |
| A decision is accepted | Human/project decision authority |
| The fix is implemented | The actual final diff |
| The fix works | Relevant current behavior verification |
| A skill is installed | Client discovery/inventory |
| A new agent invokes it | A fresh relevant session actually invoking it |
| The loop improved work | Later comparable tasks with reduced recurrence/overhead |
