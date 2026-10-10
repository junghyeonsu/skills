# Host adapters

These instructions use capabilities actually available in the running host. A model name does not determine those capabilities.

## Codex

- Use `create_goal` only on an explicit human request to start a goal, or the host's `/goal` command. Set a budget only if requested.
- The native goal owns status, continuation, tokens, and interruption. A local checkpoint records task progress; it is not a second native goal database.
- Call `update_goal` complete only after the full agreed finish line is satisfied. A budget stopping execution is not completion.
- Pause only on the user's explicit pause request. Under the current Codex tool contract, blocked requires the same blocking condition in at least three consecutive goal turns and no meaningful independent work. A resumed previously blocked goal starts a fresh audit. Follow live tool instructions if they change.
- Do not register scheduled work merely because an active goal is lengthy. Use the host's automation tool when the human requests later or recurring work.
- Installed skills are invoked as `$goal-loop`, `$verify-outcome`, `$learn-from-work`. Plugin discovery can require a fresh session or client reload.

## Claude Code

- Load the same skills from the plugin's `skills/` directory. Invocation is `/agent-workflow:goal-loop`, `/agent-workflow:verify-outcome`, or `/agent-workflow:learn-from-work`.
- Use the available task/checkpoint and execution tools. This package does not assume a Codex-compatible `/goal`, `create_goal`, or automatic continuation.
- Continue authorized work within the running session; on interruption, resume from the checkpoint. A durable unattended runner is a separate host capability.

## Grok Build

- The official Grok Build documentation describes Claude Code plugin compatibility and discovery of `SKILL.md`. Use the same Claude package without model-specific prompts or `Task` schemas.
- Confirm actual discovery with Grok's extension inventory. Native runtime invocation was not tested in the initial release.
- Follow Grok's available lifecycle rather than simulating Codex goal tools. Grok chat or Grok Bot is a different surface; support is not implied by Grok Build compatibility.

## Other hosts

Read the skill directly or install through the host's Agent Skills support. Map tool availability, authorization, persistence, and stop conditions explicitly. Without an unattended runner, "continue later" needs the user or a separately authorized scheduler. Instruction portability is not a promise of identical automation.
