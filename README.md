# leet-help

A CLI tool suite to create a LeetCode study workbook from a CSV file containing problem metadata. Download problems, generate AI-powered solutions, create PDF workbooks, and build Anki flash cards.

## Features

- **Download** LeetCode problems using Playwright/Chromium
- **Generate solutions** using multiple LLMs via Simon Willison's `llm` CLI tool
- **Create markdown index** with links to all problems and solutions
- **Generate PDFs** for each problem with solutions, plus a combined workbook
- **Build Anki decks** for spaced repetition study

## Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- [llm](https://github.com/simonw/llm) CLI tool (for solution generation)
- Homebrew (macOS) for PDF dependencies

### Setup

```bash
# Clone the repo
git clone https://github.com/hafiz-ahsan/leet-help.git
cd leet-help

# Install dependencies
uv sync

# Install Playwright browsers
uv run playwright install chromium

# Install PDF dependencies (macOS)
brew install pango
```

### API Keys

Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

Install LLM plugins for the models you want to use:

```bash
llm install llm-anthropic
```

## Usage

### CSV Format

Create a CSV file with your problem list:

```csv
Number,Title,Acceptance,Difficulty,URL
1,Two Sum,56.9%,Easy,https://leetcode.com/problems/two-sum/
3,Longest Substring Without Repeating Characters,38.3%,Medium,https://leetcode.com/problems/longest-substring-without-repeating-characters/
```

### 1. Download Problems

Download LeetCode problem descriptions and save as markdown.

```bash
# Download all problems from CSV
uv run leet-help download --csv grind75.csv

# Download specific problems
uv run leet-help download --csv grind75.csv -p 1 -p 3

# Skip already downloaded problems
uv run leet-help download --csv grind75.csv --skip-existing
```

Output: `problems/{number}-{slug}/problem.md`

### 2. Generate Solutions

Generate AI-powered solutions with pseudocode and heavily-commented code.

```bash
# Generate solutions using models from config.yaml
uv run leet-help solve --csv grind75.csv

# Use specific models
uv run leet-help solve --csv grind75.csv -m gpt-5 -m claude-opus-4.5

# Generate for specific problems
uv run leet-help solve --csv grind75.csv -p 1 -p 3 -m gpt-5
```

Output: `problems/{number}-{slug}/solution-{model}.md`

### 3. Generate Index

Create a markdown index file with a table linking to all problems and solutions.

```bash
uv run leet-help index --csv grind75.csv
```

Output: `grind75.md` (same basename as CSV)

### 4. Generate PDFs

Create PDF files for each problem containing the problem statement and solutions.

```bash
# Generate PDFs for all problems
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf --csv grind75.csv

# Generate for specific problems
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf --csv grind75.csv -p 1 -p 3

# Force regeneration (ignore timestamps)
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help pdf --csv grind75.csv --force
```

Output:
- `problems/{number}-{slug}/solutions.pdf` (individual PDFs)
- `{problemset}-solutions.pdf` (combined workbook, e.g., `grind75-solutions.pdf`)

### 5. Generate Anki Deck

Create Anki flash cards with problem statements and pseudocode solutions.

```bash
# Generate Anki deck for all problems
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help anki --csv grind75.csv

# Generate for specific problems
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help anki --csv grind75.csv -p 1 -p 3

# Custom output file and deck name
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib uv run leet-help anki --csv grind75.csv -o my-deck.apkg --deck-name "My LeetCode Deck"
```

Output: `{problemset}.apkg` (e.g., `grind75.apkg`)

**Card format:**
- **Front:** Problem statement (without examples/constraints)
- **Back:** Pseudocode from Claude Opus + links to solutions on GitHub

## Configuration

### config.yaml

Configure LLM models and reference directories:

```yaml
llm:
  default_model: "gpt-4o"
  models:
    - name: "gpt-5"
      alias: "gpt5"
    - name: "claude-opus-4.5"
      alias: "claude-opus"

reference_directories:
  - /path/to/existing/solutions

prompt: |
  You are an expert algorithm tutor...
```

## Project Structure

```
leet-help/
├── pyproject.toml           # Package configuration
├── config.yaml              # LLM configuration
├── grind75.csv              # Input problem list
├── grind75.md               # Generated index
├── grind75-solutions.pdf    # Combined PDF workbook
├── src/leet_help/
│   ├── cli.py               # CLI entry point
│   ├── downloader.py        # Problem downloader
│   ├── solver.py            # Solution generator
│   ├── indexer.py           # Markdown index generator
│   ├── pdf_generator.py     # PDF generator
│   ├── models.py            # Data models
│   └── utils.py             # Shared utilities
├── problems/                # Downloaded problems & solutions
│   ├── 1-two-sum/
│   │   ├── problem.md
│   │   ├── solution-gpt5.md
│   │   ├── solution-claude-opus.md
│   │   └── solutions.pdf
│   └── ...
├── templates/
│   └── problem.html         # PDF template
└── plans/
    └── implementation-plan.md
```

## Dependencies

- **click** - CLI framework
- **playwright** - Browser automation for downloading
- **html2text** - HTML to Markdown conversion
- **pyyaml** - Configuration file parsing
- **python-dotenv** - Environment variable loading
- **weasyprint** - HTML to PDF conversion
- **jinja2** - HTML templating
- **markdown** - Markdown to HTML conversion
- **pygments** - Syntax highlighting
- **pypdf** - PDF concatenation
- **genanki** - Anki deck generation

## License

MIT
