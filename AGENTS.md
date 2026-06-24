# Agent Instructions for leet-help

## Solve LeetCode Problems

When the user asks you to solve, regenerate, re-solve, update, or refresh solutions for one or more LeetCode problems, follow the instructions in:

```
.claude/skills/solve-leetcode-problem/SKILL.md
```

Read that file first, then execute its steps. The skill is written for any capable AI agent — it does not require the Claude Code CLI. As Codex, you write solutions to `solution-codex.md` inside each problem's directory.

### Quick reference

- Problem metadata: `problem-index.csv` (columns: `Number,Title,Difficulty,Acceptance,Category,URL`)
- Problem statements: `problems/{Number}-{slug}/problem.md`
- Your output: `problems/{Number}-{slug}/solution-codex.md`
- Verification: `uv run python /tmp/verify_{Number}.py`

### Example requests and what they mean

| User says | Action |
|---|---|
| "solve problem 1" | Generate solution for problem 1, write `problems/1-two-sum/solution-codex.md` |
| "regenerate all Array problems" | Filter `problem-index.csv` by Category=Array, generate each |
| "solve 1, 3, and 21" | Generate solutions for those three problem numbers |
| "regenerate all Easy problems" | Filter by Difficulty=Easy |

## Project overview

`leet-help` is a CLI and web tool for LeetCode study. Key commands (all via `uv run leet-help`):

| Command | Purpose |
|---|---|
| `download --csv problem-index.csv` | Download problem statements from LeetCode |
| `serve` | Launch web UI at `http://127.0.0.1:8000` |
| `pdf --csv problem-index.csv` | Generate per-problem PDFs + combined workbook |
| `index --csv problem-index.csv` | Generate a markdown index |

On macOS, prefix PDF/serve commands with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`.

## Key files

```
problem-index.csv                    # 75 Grind 75 problems
grind75-solutions.pdf                # Combined PDF workbook
problems/{N}-{slug}/problem.md       # Problem statement
problems/{N}-{slug}/solution-*.md    # AI-generated solutions
.claude/skills/solve-leetcode-problem/SKILL.md  # Solve skill (read this)
src/leet_help/server.py              # FastAPI web server
templates/browser.html               # Web UI
```
