---
name: download-leetcode-problem
description: Download LeetCode problem statements and save them as problem.md files. Use when the user asks to download, fetch, or pull one or more problems from LeetCode.
version: 1.0.0
---

# Download LeetCode Problems

Use the `leet-help download` CLI command to fetch problem statements from LeetCode via Playwright/Chromium and save them as `problems/{Number}-{slug}/problem.md`.

## Step 1 — Determine scope

Parse the user's request. At least one problem number is required — the command will error without `-p`.

- Specific problem numbers: e.g. "download 1 and 3" → use `-p 1 -p 3`
- If the user says "all problems", ask them to confirm or list the numbers — downloading all 75 at once is slow and hits LeetCode repeatedly.
- Already-downloaded problems are skipped by default. Add `--force` only if the user explicitly wants to re-download.

## Step 2 — Run the download command

```bash
uv run leet-help download [options]
```

`problem-index.csv` is the default — no `--csv` needed unless using a different file.

### Common invocations

Download specific problems (skips already-downloaded ones by default):
```bash
uv run leet-help download -p 1 -p 3
```

Force re-download even if problem.md exists:
```bash
uv run leet-help download -p 1 -p 3 --force
```

### All options

| Option | Default | Description |
|---|---|---|
| `--csv` | `problem-index.csv` | Path to problem index CSV |
| `-p` / `--problems` | required | Specific problem numbers; repeat for multiple |
| `-o` / `--output` | `problems/` | Output directory |
| `--force` | false | Re-download even if `problem.md` already exists |
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
