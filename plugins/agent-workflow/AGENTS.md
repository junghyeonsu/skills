# Working on this package

- Keep one copy of each skill under `plugins/agent-workflow/skills/`.
- Preserve host-specific goal and permission semantics in the host adapter.
- Keep portable plugin metadata and Claude metadata names/versions aligned.
- Do not introduce a scheduler, MCP server, model-specific delegation schema, hook, or dependency without a demonstrated need.
- Keep raw sessions, project facts, private paths, screenshots, and runtime receipts out of the distributed package.
- Test receipt changes with the public CLI tests. Validate the plugin and marketplace with the installed clients; do not label schema checks as behavioral agent evaluations.
- Keep user-facing changes small and explain the observed problem, resulting behavior, evidence, and limits.
