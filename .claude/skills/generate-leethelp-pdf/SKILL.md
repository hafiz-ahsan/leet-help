---
name: generate-leethelp-pdf
description: Generate solutions.pdf for one or more problems, and regenerate all-solutions.pdf. Use when the user asks to generate, regenerate, rebuild, or export PDFs.
version: 1.0.0
---

# Generate PDFs

Use the `leet-help pdf` CLI command to generate per-problem `solutions.pdf` files and the combined `all-solutions.pdf` workbook.

On macOS, WeasyPrint requires native libraries. Always prefix with:

```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf [options]
```

## Step 1 — Determine scope

Parse the user's request:

- Specific problem numbers → use `-p` for each
- All problems → no `-p` flag
- Force rebuild even if PDFs are current → add `--force`

## Step 2 — Run the command

Generate PDFs for specific problems:
```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf -p 1 -p 3
```

Generate all PDFs (skips up-to-date ones):
```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf
```

Force regeneration of everything:
```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf --force
```

Force regeneration of specific problems:
```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf -p 37 --force
```

### All options

| Option | Default | Description |
|---|---|---|
| `--csv` | `problem-index.csv` | Path to problem index CSV |
| `-p` / `--problems` | (all) | Specific problem numbers; repeat for multiple |
| `--force` | false | Regenerate even if PDF is newer than source files |

## Step 3 — Confirm

The command outputs progress as it runs. After completion, report:
- How many PDFs were generated
- The location of the combined workbook (`all-solutions.pdf`)
- Any problems that were skipped (up-to-date) or failed
