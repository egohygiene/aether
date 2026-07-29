# Module 7: Advanced Techniques

1. **`@` file mentions** — Always give precise context, don't rely on the AI finding files
   - `@src/auth.ts` — single file
   - `@src/components/` — directory listing
   - "Fix @src/auth.ts to match @tests/auth.test.ts" — multi-file context

1. **`! shell bypass`** — `!git log --oneline -5` runs instantly, no AI overhead

1. **`/research`** — Run a deep research investigation using GitHub search and web sources

1. **`/resume` + `--continue`** — Session continuity across CLI launches

1. **`/compact`** — Compress history when context gets large (auto at 95%)
   - Check with `/context` first
   - Best used at natural task boundaries
   - Warning signs: AI contradicting earlier statements, token usage >80%

1. **`/context`** — Visualize what's eating your token budget

1. **Custom instructions precedence** (highest to lowest):
   - `CLAUDE.md` / `GEMINI.md` / `AGENTS.md` (git root + cwd)
   - `.github/instructions/**/*.instructions.md` (path-specific!)
   - `.github/copilot-instructions.md`
   - `~/.copilot/copilot-instructions.md`
   - `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` (additional directories via env var)

1. **Path-specific instructions:**
   - `.github/instructions/backend.instructions.md` with `applyTo: "src/api/**"`
   - Different coding standards for different parts of the codebase

1. **LSP config** — `~/.copilot/lsp-config.json` or `.github/lsp.json`

1. **`/review`** — Get code review without leaving terminal

1. **`--allow-all` / `--yolo`** — Full trust mode (use responsibly!)

1. **`Ctrl+T`** — Watch the AI think (learn its reasoning patterns)
