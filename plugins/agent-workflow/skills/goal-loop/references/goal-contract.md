# Completion contract

Keep this next to the task's existing plan. Use `.agent-loop/<task>/` only when no suitable record exists, keep it local, and exclude runtime artifacts from distribution.

```markdown
Outcome: the user's observable result
Source plan / latest human scope:
Target environment(s): local / CI / alpha / native / production, as applicable
Required deliverables:
| Item | Acceptance behavior | Verification | Evidence / status |
| --- | --- | --- | --- |
| ... | ... | ... | outstanding |

Excluded / explicitly deferred:
Authorization: action, scope, source instruction, conditions
Preserved user changes / existing resources:
Subtraction or reuse considered: what, why retained or removed
Checkpoint: completed / remaining / blocker / exact next action
Resume inputs: branch + head + dirty state, runtime URL/build or document revision
```

Do not build an exhaustive matrix for a one-file change. A migration across web/server/plugin needs the affected consumers; an interface needs actual interaction and relevant capture conditions; research needs requested comparison axes, sources, and a readable artifact.

Example finish line: "The test survey can be created, edited, submitted, and deleted in alpha, with screenshots for each step and CI tied to the deployed SHA. External integrations needing new credentials are deferred as the user instructed." The explicit deferral is part of this goal, not a later excuse for missing work.
