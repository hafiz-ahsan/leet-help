# leet-help

LeetCode study workbook generator - download problems, generate solutions, create PDF workbooks.

## Installation

```bash
# From source with uv
git clone https://github.com/yourusername/leet-help
cd leet-help
uv sync
```

## Usage

### Download Problems

```bash
# Download all problems from CSV
uv run leet-help download --csv grind75.csv

# Download specific problems
uv run leet-help download --csv grind75.csv --problems 1 --problems 20

# Skip already downloaded problems
uv run leet-help download --csv grind75.csv --skip-existing
```

## Prerequisites

- macOS with Safari
- Safari must have "Allow Remote Automation" enabled in Develop menu
