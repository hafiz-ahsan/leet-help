# Agent Instructions for leet-help

## Skills

Each skill has a `SKILL.md` with full instructions. Read the relevant file before acting.

### Solve LeetCode Problems

When the user asks you to solve, regenerate, re-solve, update, or refresh solutions, follow:

```
.claude/skills/solve-leetcode-problem/SKILL.md
```

As Codex, write solutions to `solution-codex.md` inside each problem's directory.

| User says | Action |
|---|---|
| "solve problem 1" | Generate solution for problem 1, write `problems/1-two-sum/solution-codex.md` |
| "regenerate all Array problems" | Filter `problem-index.csv` by Category=Array, generate each |
| "solve 1, 3, and 21" | Generate solutions for those three problem numbers |
| "regenerate all Easy problems" | Filter by Difficulty=Easy |

### Download LeetCode Problems

When the user asks you to download, fetch, or pull problem statements, follow:

```
.claude/skills/download-leetcode-problem/SKILL.md
```

Uses `uv run leet-help download`. `problem-index.csv` is the default — no `--csv` needed.

| User says | Action |
|---|---|
| "download problem 1" | `uv run leet-help download -p 1` |
| "download problems 1, 3, and 21" | `uv run leet-help download -p 1 -p 3 -p 21` |
| "download all problems" | `uv run leet-help download` |
| "download only new problems" | `uv run leet-help download --skip-existing` |

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
