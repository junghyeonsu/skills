# Validation

2026-10-10 · Agent Workflow 0.1.2 · base `5591357a874441981033b44b720a06b862156f4a`

| Check | Result |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | 11 CLI behavior tests passed |
| Codex skill creator `quick_validate.py` for three new skills | Passed |
| `claude plugin validate --strict ./plugins/agent-workflow` | Passed with Claude Code 2.1.226 |
| `claude plugin validate --strict .` | Marketplace passed |
| `git diff --check` | Passed |
| Codex CLI 0.146.1 local marketplace + plugin installation | Installed and enabled, 0.1.2 |
| Installed source comparison after the rename | All 16 plugin files match; the previous plugin identifier was removed |

Receipt behavior covers passing checks, failed checks, later source changes, changes during an auto-fix, modified logs, missing/deleted inputs, preserving prior receipts, missing executables, direct argv without shell expansion, and rejected symlink inputs.

The optional Python runner uses standard-library modules only. The basic Codex skill validator itself requires PyYAML; it is a development check, not a plugin runtime dependency.

Not yet verified:

- A fresh agent's automatic invocation and adherence. See `tests/workflow-scenarios.md` for planned evaluation.
- Grok Build loading/runtime behavior. No Grok CLI was available in this environment.
- GitHub remote CI. This addition does not include a GitHub Actions workflow.
- Git marketplace installation. This record covers the local source; published Git installation is checked separately at release.
- Reduced correction rate or improved quality in later comparable goals.

Existing `skills/ui-references/` was not modified. Its external pointer sweep was not rerun for this addition.
