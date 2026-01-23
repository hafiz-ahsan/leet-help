# LeetCode Study Workbook - Implementation Plan

## Project Overview

Build a Python CLI tool suite to create a LeetCode study workbook from a CSV file containing problem metadata. The project consists of five programs and uses `uv` for packaging.

**CSV Structure (grind75_problems.csv):**
```
Number,Title,Acceptance,Difficulty,URL
1,Two Sum,56.9%,Easy,https://leetcode.com/problems/two-sum/
...
```

---

## Directory Structure

```
leet-help/
├── pyproject.toml           # uv/pip package configuration
├── README.md                 # Usage documentation
├── config.yaml               # LLM configuration file
├── grind75_problems.csv      # Input problem list
├── grind75_problems.md       # Generated index (Program 3 output)
├── src/
│   └── leet_help/
│       ├── __init__.py
│       ├── cli.py            # Main CLI entry point
│       ├── downloader.py     # Program 1: Download problems
│       ├── solver.py         # Program 2: Generate solutions
│       ├── indexer.py        # Program 3: Generate markdown index
│       ├── pdf_generator.py  # Program 4: Generate per-problem PDFs
│       ├── anki_generator.py # Program 5: Generate Anki flash cards
│       ├── models.py         # Data models (Problem, Solution)
│       └── utils.py          # Shared utilities (CSV parsing, etc.)
├── problems/                 # Downloaded problem descriptions
│   ├── 1-two-sum/
│   │   ├── problem.md
│   │   ├── solution-gpt-5.md
│   │   ├── solution-claude-opus.md
│   │   └── problem.pdf       # Generated PDF (Program 4 output)
│   ├── 20-valid-parentheses/
│   │   ├── problem.md
│   │   ├── solution-gpt-5.md
│   │   ├── solution-claude-opus.md
│   │   └── problem.pdf
│   └── ...
├── templates/                # Jinja2 templates for PDF generation
│   └── problem.html
└── plans/
    └── implementation-plan.md
```

---

## Program 1: Downloader (COMPLETED)

### Purpose
Download LeetCode problem descriptions using Playwright/Chromium and extract problem content.

### Implementation
- Uses Playwright with Chromium browser
- Extracts problem description via CSS selectors
- Converts HTML to Markdown using `html2text`
- Saves to `problems/{number}-{slug}/problem.md`

### CLI Interface
```bash
uv run leet-help download --csv grind75_problems.csv
uv run leet-help download --csv grind75_problems.csv -p 1 -p 3
uv run leet-help download --csv grind75_problems.csv --skip-existing
```

---

## Program 2: Solver (COMPLETED)

### Purpose
Generate pseudocode and heavily-commented solutions using Simon Willison's `llm` CLI tool.

### Implementation
- Reads config from `config.yaml` for model and prompt settings
- Searches reference directories for existing solutions by problem number pattern (`{number}-*`)
- Calls system `llm` CLI tool (must be in PATH)
- Saves solutions to `problems/{number}-{slug}/solution-{model-alias}.md`

### CLI Interface
```bash
uv run leet-help solve --csv grind75_problems.csv
uv run leet-help solve --csv grind75_problems.csv -p 1 -m gpt-5 -m claude-opus-4.5
```

---

## Program 3: Indexer

### Purpose
Generate a markdown index file with a table linking to all problems and their solutions.

### Output Format
Creates `{csv_basename}.md` in the root directory (e.g., `grind75_problems.csv` → `grind75_problems.md`).

### Table Structure
| # | Title | Difficulty | LC | Problem | GPT-5 | Claude |
|---|-------|------------|----|---------| ------|--------|
| 1 | Two Sum | Easy | [LC](https://leetcode.com/problems/two-sum/) | [Problem](problems/1-two-sum/problem.md) | [Solution](problems/1-two-sum/solution-gpt-5.md) | [Solution](problems/1-two-sum/solution-claude-opus.md) |

### Implementation Details

```python
def generate_index(csv_path: Path, problems_dir: Path) -> Path:
    """
    1. Read CSV file
    2. For each problem:
       a. Get problem directory name (number-slug from URL)
       b. Check which solution files exist
       c. Build table row with links
    3. Write markdown file with same basename as CSV
    """
```

### CLI Interface
```bash
# Generate index from CSV
uv run leet-help index --csv grind75_problems.csv

# Specify problems directory
uv run leet-help index --csv grind75_problems.csv --problems-dir problems/
```

### Dependencies
- None additional (uses standard library)

---

## Program 4: PDF Generator

### Purpose
Generate a compact 2-page PDF for each problem, containing the problem statement and both LLM solutions side-by-side.

### Output
- Creates `problem.pdf` in each problem subdirectory
- Skips generation if PDF is newer than all solution files

### Layout Specifications
- **Maximum 2 pages**
- **Font size: 10pt**
- **Page 1: Problem Statement**
  - Two-column layout
  - Condensed problem description
  - Examples and constraints
- **Page 2: Solutions**
  - Two-column layout
  - Left column: Claude Opus solution
  - Right column: GPT-5 solution
  - Code properly formatted with syntax highlighting

### Implementation Details

```python
def generate_problem_pdf(problem_dir: Path, skip_if_current: bool = True) -> Path | None:
    """
    1. Check if PDF exists and is newer than solutions (skip if so)
    2. Read problem.md
    3. Read solution-claude-opus.md and solution-gpt-5.md
    4. Render HTML template with two-column layout
    5. Convert to PDF using WeasyPrint
    6. Save as problem.pdf in the problem directory
    """

def generate_all_pdfs(problems_dir: Path, skip_if_current: bool = True) -> list[Path]:
    """
    Iterate through all problem directories and generate PDFs.
    """
```

### Template Structure
```html
<!-- templates/problem.html -->
<html>
<head>
  <style>
    @page { size: letter; margin: 0.5in; }
    body { font-size: 10pt; font-family: 'SF Pro', sans-serif; }
    .two-column { column-count: 2; column-gap: 20px; }
    .problem-section { page-break-after: always; }
    .solutions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .solution-col { font-size: 9pt; }
    pre { font-size: 8pt; background: #f5f5f5; padding: 5px; overflow-wrap: break-word; }
    h1 { font-size: 14pt; margin: 0 0 10px 0; }
    h2 { font-size: 11pt; margin: 10px 0 5px 0; }
  </style>
</head>
<body>
  <!-- Page 1: Problem -->
  <div class="problem-section">
    <h1>{{ number }}. {{ title }} ({{ difficulty }})</h1>
    <div class="two-column">
      {{ problem_content | safe }}
    </div>
  </div>

  <!-- Page 2: Solutions -->
  <div class="solutions">
    <div class="solution-col">
      <h2>Claude Opus Solution</h2>
      {{ claude_solution | safe }}
    </div>
    <div class="solution-col">
      <h2>GPT-5 Solution</h2>
      {{ gpt_solution | safe }}
    </div>
  </div>
</body>
</html>
```

### CLI Interface
```bash
# Generate PDFs for all problems
uv run leet-help pdf --csv grind75_problems.csv

# Generate PDF for specific problems
uv run leet-help pdf --csv grind75_problems.csv -p 1 -p 3

# Force regeneration (ignore timestamps)
uv run leet-help pdf --csv grind75_problems.csv --force
```

### Dependencies
- `weasyprint` (HTML to PDF)
- `jinja2` (templating)
- `markdown` (MD to HTML)
- `pygments` (syntax highlighting)

---

## Program 5: Anki Flash Card Generator

### Purpose
Generate Anki-importable flash cards for each problem, containing both LLM solutions.

### Output Format
- Creates an `.apkg` file (Anki package) that can be imported directly into Anki
- Or creates a text file in Anki-importable format (tab-separated)

### Card Structure
- **Front**: Problem statement (condensed)
- **Back**:
  - Claude Opus solution
  - GPT-5 solution
  - Key patterns/insights
- **Tags**: difficulty, problem number, category

### Implementation Details

```python
def create_anki_deck(csv_path: Path, problems_dir: Path, output_path: Path) -> Path:
    """
    1. Read CSV file for problem metadata
    2. For each problem:
       a. Read problem.md (extract condensed version for front)
       b. Read both solution files
       c. Create flash card with front/back
       d. Add tags (Easy/Medium/Hard, problem number)
    3. Export as .apkg file using genanki
    """
```

### Anki Card Template
```
Front:
-----------------
**{{ number }}. {{ title }}** ({{ difficulty }})

{{ problem_summary }}

Back:
-----------------
## Claude Opus Solution
{{ claude_solution }}

## GPT-5 Solution
{{ gpt_solution }}

**Key Insight:** {{ key_insight }}
**Time:** {{ time_complexity }} | **Space:** {{ space_complexity }}
```

### CLI Interface
```bash
# Generate Anki deck from CSV
uv run leet-help anki --csv grind75_problems.csv --output grind75.apkg

# Generate for specific problems
uv run leet-help anki --csv grind75_problems.csv -p 1 -p 3 --output selected.apkg

# Export as text file instead of .apkg
uv run leet-help anki --csv grind75_problems.csv --format text --output grind75.txt
```

### Dependencies
- `genanki` (Anki deck generation)

---

## Package Configuration

### Updated `pyproject.toml`
```toml
[project]
name = "leet-help"
version = "0.1.0"
description = "LeetCode study workbook generator"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
keywords = ["leetcode", "algorithms", "study", "workbook", "anki"]

dependencies = [
    "click>=8.1.0",
    "pyyaml>=6.0",
    "html2text>=2024.2.0",
    "playwright>=1.40.0",
    "python-dotenv>=1.0.0",
    "weasyprint>=60.0",
    "jinja2>=3.1.0",
    "markdown>=3.5.0",
    "pygments>=2.17.0",
    "genanki>=0.13.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
]

[project.scripts]
leet-help = "leet_help.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/leet_help"]
```

---

## Implementation Phases

### Phase 1: Project Setup (COMPLETED)
1. ✅ Update `pyproject.toml` with configuration
2. ✅ Create package structure (`src/leet_help/`)
3. ✅ Set up CLI framework with Click
4. ✅ Create shared utilities (CSV parsing, problem model)
5. ✅ Create default `config.yaml`

### Phase 2: Downloader - Program 1 (COMPLETED)
1. ✅ Implement Playwright/Chromium browser automation
2. ✅ Implement HTML parsing and content extraction
3. ✅ Implement Markdown conversion
4. ✅ Add CLI commands for download
5. ✅ Test with all 75 problems

### Phase 3: Solver - Program 2 (COMPLETED)
1. ✅ Implement config file loading
2. ✅ Implement reference directory search by problem number
3. ✅ Implement `llm` CLI wrapper (uses system llm)
4. ✅ Implement solution storage
5. ✅ Add CLI commands for solve
6. ✅ Test with GPT-5 and Claude Opus 4.5 on all 75 problems

### Phase 4: Indexer - Program 3
1. Implement index generation
2. Create markdown table with links
3. Add CLI command
4. Test output

### Phase 5: PDF Generator - Program 4
1. Create HTML template with compact two-column layout
2. Implement PDF generation with WeasyPrint
3. Implement timestamp-based skip logic
4. Add CLI commands
5. Test PDF output quality

### Phase 6: Anki Generator - Program 5
1. Design card template
2. Implement deck generation with genanki
3. Add tag support (difficulty, category)
4. Add CLI commands
5. Test import into Anki

### Phase 7: Polish & Release
1. Update README.md with all commands
2. Add error handling and logging
3. Add progress bars for long operations
4. Prepare for PyPI release

---

## CLI Command Summary

```bash
# Program 1: Download problems
uv run leet-help download --csv grind75_problems.csv [--skip-existing] [-p NUMBER]

# Program 2: Generate solutions
uv run leet-help solve --csv grind75_problems.csv [-m MODEL] [-p NUMBER]

# Program 3: Generate markdown index
uv run leet-help index --csv grind75_problems.csv

# Program 4: Generate PDFs
uv run leet-help pdf --csv grind75_problems.csv [--force] [-p NUMBER]

# Program 5: Generate Anki deck
uv run leet-help anki --csv grind75_problems.csv --output grind75.apkg
```

---

## Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| CLI Framework | Click | Industry standard, good UX, easy subcommands |
| Browser Automation | Playwright | More reliable than Selenium, bundled browsers |
| PDF Generation | WeasyPrint | Pure Python, good CSS support |
| Anki Generation | genanki | Standard library for Anki deck creation |
| LLM CLI | System `llm` | User's existing installation, not bundled |
| Config Format | YAML | Human-readable, standard for configs |
| Package Manager | uv | Fast, modern, user's preference |

---

## Current Status

**Completed:**
- 75 problems downloaded
- 75 GPT-5 solutions generated
- 75 Claude Opus 4.5 solutions generated
- Total: 150 solution files

**Next Steps:**
1. Implement Phase 4: Indexer (Program 3)
2. Implement Phase 5: PDF Generator (Program 4)
3. Implement Phase 6: Anki Generator (Program 5)
4. Phase 7: Polish & Release
