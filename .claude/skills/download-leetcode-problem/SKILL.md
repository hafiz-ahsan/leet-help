---
name: download-leetcode-problem
description: Download LeetCode problem statements and save them as problem.md files. Use when the user asks to download, fetch, or pull one or more problems from LeetCode.
version: 1.0.0
---

# Download LeetCode Problems

Use the `leet-help download` CLI command to fetch problem statements from LeetCode via Playwright/Chromium and save them as `problems/{Number}-{slug}/problem.md`.

## Step 1 — Determine scope

Parse the user's request:

- Specific problem numbers: e.g. "download 1 and 3" → use `-p 1 -p 3`
- All problems: e.g. "download all problems" → use `--csv problem-index.csv` with no `-p` filter
- Skip already downloaded: if the user says "only new" or "skip existing" → add `--skip-existing`

## Step 2 — Run the download command

```bash
uv run leet-help download --csv problem-index.csv [options]
```

### Common invocations

Download specific problems:
```bash
uv run leet-help download --csv problem-index.csv -p 1 -p 3
```

Download all 75 problems (skip ones already present):
```bash
uv run leet-help download --csv problem-index.csv --skip-existing
```

Force re-download everything:
```bash
uv run leet-help download --csv problem-index.csv
```

### All options

| Option | Default | Description |
|---|---|---|
| `--csv` | required | Path to problem index CSV |
| `-p` / `--problems` | (all) | Specific problem numbers; repeat for multiple |
| `-o` / `--output` | `problems/` | Output directory |
| `--skip-existing` | false | Skip problems that already have `problem.md` |
| `--delay` | 2.0s | Delay between downloads (be polite to LeetCode) |

## Step 3 — Confirm

After the command completes, report:
- How many problems were downloaded
- Which problem directories were created or updated (e.g. `problems/1-two-sum/problem.md`)
- Any that were skipped (if `--skip-existing` was used)

## Notes

- Requires Playwright/Chromium: run `uv run playwright install chromium` if it has not been installed yet.
- LeetCode may require a login for premium problems. The downloader opens a real browser window; log in manually if prompted.
- The default 2-second delay between downloads avoids rate limiting. Do not set `--delay 0`.
