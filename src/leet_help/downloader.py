
"""Download LeetCode problems using Playwright."""

import time
from pathlib import Path

import html2text
from playwright.sync_api import sync_playwright, Page

from .models import Problem


def create_browser() -> tuple:
    """Create and return a Playwright browser instance."""
    playwright = sync_playwright().start()
    # Use Chromium with stealth-like settings
    browser = playwright.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
        ],
    )
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1920, "height": 1080},
    )

    # Add script to remove webdriver flag
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

    return playwright, browser, context


def extract_problem_html(page: Page, timeout: int = 60000) -> str:
    """Extract problem description HTML from the current page."""
    # Selectors to try for the problem description
    selectors = [
        '[data-track-load="description_content"]',
        '.elfjS',
        '.xFUwe',
        '._1l1MA',
        '.question-content',
        '.content__u3I1',
    ]

    # Try each selector
    for selector in selectors:
        try:
            page.wait_for_selector(selector, timeout=10000)
            element = page.query_selector(selector)
            if element:
                return element.inner_html()
        except Exception:
            continue

    # Fallback: try to find a div containing "Example 1:" and "Constraints:"
    try:
        divs = page.query_selector_all("div")
        for div in divs:
            text = div.inner_text()
            if "Example 1:" in text and "Constraints:" in text:
                return div.inner_html()
    except Exception:
        pass

    raise RuntimeError("Could not find problem description on page")


def html_to_markdown(html: str) -> str:
    """Convert HTML to clean Markdown."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True
    return h.handle(html)


def download_problem(
    problem: Problem,
    output_dir: Path,
    page: Page,
    skip_existing: bool = False,
) -> Path:
    """
    Download a single problem using Playwright.

    Returns the path to the saved problem.md file.
    """
    problem_dir = problem.get_problem_dir(output_dir)
    problem_file = problem_dir / "problem.md"

    # Skip if already exists
    if skip_existing and problem_file.exists():
        print(f"  Skipping {problem.number}. {problem.title} (already exists)")
        return problem_file

    print(f"  Downloading {problem.number}. {problem.title}...")

    # Navigate to the problem page with longer timeout, use domcontentloaded instead of networkidle
    page.goto(problem.url, wait_until="domcontentloaded", timeout=60000)

    # Wait for the content to be visible
    time.sleep(5)

    # Extract the HTML content
    html_content = extract_problem_html(page)

    if not html_content:
        raise RuntimeError(f"Could not extract content for problem {problem.number}")

    # Convert to Markdown
    markdown_content = html_to_markdown(html_content)

    # Create the problem directory
    problem_dir.mkdir(parents=True, exist_ok=True)

    # Create the full markdown document with metadata
    full_content = f"""# {problem.number}. {problem.title}

**Difficulty:** {problem.difficulty}
**Acceptance Rate:** {problem.acceptance}
**Source:** <{problem.url}>

---

{markdown_content}
"""

    # Save to file
    problem_file.write_text(full_content, encoding="utf-8")
    print(f"  Saved to {problem_file}")

    return problem_file


def download_problems(
    problems: list[Problem],
    output_dir: Path,
    skip_existing: bool = False,
    delay_between: float = 2.0,
) -> list[Path]:
    """
    Download multiple problems.

    Args:
        problems: List of problems to download
        output_dir: Base directory for problem storage
        skip_existing: Skip problems that already have a problem.md file
        delay_between: Delay in seconds between downloads (to avoid rate limiting)

    Returns:
        List of paths to saved problem files
    """
    saved_files = []
    total = len(problems)

    print(f"Downloading {total} problems to {output_dir}")
    print("Starting browser...")

    playwright = None
    browser = None
    try:
        playwright, browser, context = create_browser()
        page = context.new_page()

        for i, problem in enumerate(problems, 1):
            print(f"[{i}/{total}]", end="")
            try:
                path = download_problem(problem, output_dir, page, skip_existing)
                saved_files.append(path)
            except Exception as e:
                print(f"  ERROR: Failed to download {problem.number}. {problem.title}: {e}")

            # Delay between downloads
            if i < total:
                time.sleep(delay_between)

    finally:
        if browser:
            browser.close()
        if playwright:
            playwright.stop()

    print(f"\nDownloaded {len(saved_files)}/{total} problems successfully")
    return saved_files
