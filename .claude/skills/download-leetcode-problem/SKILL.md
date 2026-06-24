---
name: download-leetcode-problem
description: Download a LeetCode problem statement, update problem-index.csv with its metadata, and save it as problem.md. Use when the user asks to download, fetch, or pull one or more problems from LeetCode.
version: 2.0.0
---

# Download LeetCode Problems

Given one or more problem numbers, fetch their metadata from LeetCode, update `problem-index.csv`, then download the problem statement via the CLI.

## Step 1 — Fetch metadata from LeetCode

For each problem number, query the LeetCode API to get the title, slug, difficulty, and acceptance rate:

```bash
curl -s 'https://leetcode.com/api/problems/all/' | python3 -c "
import json, sys
data = json.load(sys.stdin)
p = next((x for x in data['stat_status_pairs'] if x['stat']['frontend_question_id'] == {NUMBER}), None)
if not p:
    print('NOT FOUND')
    sys.exit(1)
difficulty = {1: 'Easy', 2: 'Medium', 3: 'Hard'}[p['difficulty']['level']]
total = p['stat']['total_submitted']
acs = p['stat']['total_acs']
acceptance = f'{acs/total*100:.1f}%' if total else 'N/A'
slug = p['stat']['question__title_slug']
print(json.dumps({
    'number': p['stat']['frontend_question_id'],
    'title': p['stat']['question__title'],
    'slug': slug,
    'difficulty': difficulty,
    'acceptance': acceptance,
    'url': f'https://leetcode.com/problems/{slug}/'
}))
"
```

## Step 2 — Infer the category

Using the problem title, difficulty, and your knowledge of LeetCode problems, infer the most appropriate category. Use one of these standard categories where possible:

`Array`, `String`, `Hash Table`, `Linked List`, `Stack`, `Queue`, `Tree`, `Binary Tree`, `Binary Search`, `Graph`, `Dynamic Programming`, `Backtracking`, `Greedy`, `Heap`, `Trie`, `Sliding Window`, `Two Pointers`, `Math`, `Bit Manipulation`, `Design`

Pick the single best-fit category. If uncertain, choose the most prominent data structure or algorithm pattern the problem is known for.

## Step 3 — Update problem-index.csv

Read `problem-index.csv`. The columns are: `Number,Title,Difficulty,Acceptance,Category,URL`

- If the problem number already exists in the CSV, update its row.
- If it does not exist, append a new row in ascending order by Number.

Write the updated CSV back to disk.

## Step 4 — Download the problem statement

Now that the problem is in the CSV, call the CLI:

```bash
uv run leet-help download -p {NUMBER}
```

This opens a browser, navigates to the problem page, and saves the content to `problems/{Number}-{slug}/problem.md`. Already-downloaded problems are skipped unless `--force` is passed.

## Step 5 — Confirm

Report for each problem:
- ✅ Downloaded — `problems/{Number}-{slug}/problem.md` created
- ⏭️ Skipped — already existed
- ❌ Failed — note the error

## Notes

- The LeetCode API call in Step 1 returns all problems in one payload. Cache the result if downloading multiple problems in one session to avoid repeated large fetches.
- The browser opened by the CLI is real (non-headless). If LeetCode shows a login wall, the user must log in manually.
- Default delay between downloads is 2 seconds. Do not remove it.
