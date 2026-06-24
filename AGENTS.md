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

Fetches metadata from the LeetCode API, infers category, updates `problem-index.csv`, then calls the CLI. At least one `-p` is required.

| User says | Action |
|---|---|
| "download problem 37" | Fetch metadata → update CSV → `uv run leet-help download -p 37` |
| "download problems 1 and 3" | Fetch metadata for each → update CSV → `uv run leet-help download -p 1 -p 3` |
| "re-download problem 1" | `uv run leet-help download -p 1 --force` |

### Generate PDFs

When the user asks to generate, regenerate, rebuild, or export PDFs, follow:

```
.claude/skills/generate-leethelp-pdf/SKILL.md
```

Requires `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` on macOS. Produces per-problem `solutions.pdf` files and the combined `all-solutions.pdf`.

| User says | Action |
|---|---|
| "generate PDF for problem 37" | `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf -p 37` |
| "regenerate all PDFs" | `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf --force` |
| "generate PDFs for all problems" | `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf` |

## Project overview

`leet-help` is a CLI and web tool for LeetCode study. Key commands (all via `uv run leet-help`):

| Command | Purpose |
|---|---|
| `download -p {N}` | Download problem statement from LeetCode |
| `pdf` | Generate per-problem PDFs + `all-solutions.pdf` |
| `serve` | Launch web UI at `http://127.0.0.1:8000` |
| `index` | Generate a markdown index |

`problem-index.csv` is the default for all commands — no `--csv` needed. On macOS, prefix `pdf` and `serve` with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib`.

## Key files

```
problem-index.csv                                        # Problem list (grows as new problems are added)
all-solutions.pdf                                        # Combined PDF workbook
problems/{N}-{slug}/problem.md                          # Problem statement
problems/{N}-{slug}/solution-claude-opus.md             # Claude solution
problems/{N}-{slug}/solution-codex.md                   # Codex solution
problems/{N}-{slug}/solutions.pdf                       # Per-problem PDF
.claude/skills/solve-leetcode-problem/SKILL.md          # Solve skill
.claude/skills/download-leetcode-problem/SKILL.md       # Download skill
.claude/skills/generate-leethelp-pdf/SKILL.md            # PDF generation skill
src/leet_help/server.py                                  # FastAPI web server
templates/browser.html                                   # Web UI
```
