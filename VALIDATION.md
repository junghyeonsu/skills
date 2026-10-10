# Validation

2026-10-10 · Agent Workflow 0.1.3 · base `990cda1ed820ec84d2bdff641badf58656393fe5`

| Check | Result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 11 CLI behavior tests passed in 0.1.2; runner and test inputs are unchanged in 0.1.3 |
| Codex skill creator `quick_validate.py` for all three skills | Passed |
| `claude plugin validate --strict ./plugins/agent-workflow` | Passed with Claude Code 2.1.226 |
| `claude plugin validate --strict .` | Marketplace passed |
| `git diff --check` | Passed |
| Codex CLI Git marketplace installation | Version 0.1.2 was verified; 0.1.3 is checked after publishing |

Receipt behavior covers passing checks, failed checks, later source changes, changes during an auto-fix, modified logs, missing/deleted inputs, preserving prior receipts, missing executables, direct argv without shell expansion, and rejected symlink inputs.

The optional Python runner uses standard-library modules only. The basic Codex skill validator itself requires PyYAML; it is a development check, not a plugin runtime dependency.

Not yet verified:

- A fresh agent's automatic execution of the companion verification and learning phases from only a goal-loop invocation, and adherence. See `tests/workflow-scenarios.md` for planned evaluation.
- Grok Build loading/runtime behavior. No Grok CLI was available in this environment.
- GitHub remote CI. This addition does not include a GitHub Actions workflow.
- Reduced correction rate or improved quality in later comparable goals.

Existing `skills/ui-references/` was not modified. Its external pointer sweep was not rerun for this addition.
