# Provenance

- Inspiration: [cursor/plugins pstack](https://github.com/cursor/plugins/tree/main/pstack)
- Reviewed upstream commit: `ccb5507cec1546dc88135c1139c811e6c59115ba`
- Reviewed pstack version: `0.15.15`
- Upstream author and license: Lauren Tan (poteto), MIT
- Upstream concepts adapted: subtract before adding; observable verification; decision trails for substantial work; encode recurring lessons in structure; separate orchestration instructions from runtime execution.
- The new Agent Workflow plugin contains newly written skills and a newly implemented receipt script. It does not vendor pstack's source, watcher, orchestrator, agents, Slack automation, model routing, or personal tone restrictions.
- Supporting personal observations were inspected locally. Raw sessions, internal project documents, and private evidence are excluded from this distribution package.
- The upstream license text is retained in `plugins/agent-workflow/licenses/pstack-MIT.txt` for attribution. Existing unrelated installed skills are not redistributed here.

Packaging references checked on 2026-10-10:

- [OpenAI portable plugins and local marketplaces](https://developers.openai.com/plugins/build/plugins)
- [Codex goals](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)
- [Claude manifest reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Grok Build skills and plugins](https://docs.x.ai/build/features/skills-plugins-marketplaces)

Integration target: `junghyeonsu/skills`, reviewed main `5591357a874441981033b44b720a06b862156f4a`. Existing `skills/ui-references/` files are preserved.
