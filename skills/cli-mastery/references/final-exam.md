# Final Exam

Present a 10-question comprehensive exam using `ask_user` with 4 choices each. Require 80%+ to pass. Vary the selection each time.

## Question Bank

1. Which command initializes Copilot CLI in a new project? → `/init`
1. What shortcut cycles through modes? → `Shift+Tab`
1. Where are repo-level custom agents stored? → `.github/agents/*.md`
1. What does MCP stand for? → Model Context Protocol
1. Which agent is safe to run in parallel? → `explore`
1. How do you add a file to AI context? → `@filename` (e.g. `@src/auth.ts`)
1. What file has the highest instruction precedence? → `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` (git root + cwd)
1. Which command compresses conversation history? → `/compact`
1. Where is MCP configured at project level? → `.github/mcp-config.json`
1. What does `--yolo` do? → Same as `--allow-all` (skip all confirmations)
1. What does `/research` do? → Run a deep research investigation with sources
1. Which shortcut opens input in $EDITOR? → `Ctrl+G`
1. What does `/reset-allowed-tools` do? → Re-enables confirmation prompts
1. Which command copies the last AI response to your clipboard? → `/copy`
1. What does `/compact` do? → Summarizes conversation to free context

On pass (80%+): Award "CLI Wizard" title, congratulate enthusiastically!
On fail: Show which they got wrong, encourage retry.
