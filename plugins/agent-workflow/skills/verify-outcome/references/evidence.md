# Evidence record

Prefer the existing task record. Store screenshots/logs outside distributed plugin files and do not include credentials.

```markdown
Item / acceptance behavior:
Subject: repository + head + dirty state, artifact revision, or observed deployed build
Environment / time:
Action or exact command:
Exit code, if a command:
Expected observable result:
Observed result:
Evidence: real file / URL / CI run
Status: passed / failed / skipped / unavailable / unverified
Limits: what this does not establish
Cleanup: test data and resources created by this task, retained or removed
```

Example evidence boundaries:

| Observation | Supported conclusion | Still needs evidence |
| --- | --- | --- |
| Unit tests pass | Tested behavior in that harness | Native rendering |
| Browser plugin preview works | Preview behavior | Real Figma insertion/drag |
| CI is green on head A | Required checks on A passed | New head B, deployment, merge authorization |
| Candidate JSON validates | Schema validation | Canvas apply, interaction, capture |
| Screenshot looks right | That captured state | Submission, restoration, error path |
| Relevant scoped hashes match | Selected file inputs are unchanged | Unselected inputs and semantic correctness |

## Local command receipts

Run from the target project's directory. A scope must be an existing **regular file**; repeat `--input` for the files whose current content matters. Receipts and logs must be outside those inputs.

```sh
python3 /absolute/plugin/skills/verify-outcome/scripts/check_receipt.py run \
  --receipt .agent-loop/example/lint.json \
  --input src/example.ts --input package.json --input lockfile \
  -- npm run lint
python3 /absolute/plugin/skills/verify-outcome/scripts/check_receipt.py verify \
  .agent-loop/example/lint.json
```

The runner executes argv directly, without a shell. It stores combined stdout/stderr in a sibling log and records hashes before and after the command. A changed input is reported as changed, even when the command exits zero. This is useful for catching an auto-fix that changed the file being verified; re-run the final check afterward. Hashes provide consistency, not tamper-proof attestation. The runner does not expand directory scopes, inspect remote systems, classify skipped tests, or decide that a goal is complete.
