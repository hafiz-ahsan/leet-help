"""CLI entry point for leet-help."""

import click
from pathlib import Path

from .downloader import download_problems
from .indexer import generate_index
from .pdf_generator import generate_all_pdfs
from .utils import load_problems_from_csv, filter_problems_by_numbers
from .server import app, configure as configure_server


@click.group()
@click.version_option()
def main():
    """LeetCode study workbook generator."""
    pass


@main.command()
@click.option(
    "--csv",
    "csv_path",
    type=click.Path(exists=True, path_type=Path),
    default="problem-index.csv",
    show_default=True,
    help="Path to CSV file containing problems",
)
@click.option(
    "--problems",
    "-p",
    multiple=True,
    type=int,
    help="Specific problem numbers to download (can be repeated)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default="problems",
    help="Output directory for problems (default: problems/)",
)
@click.option(
    "--skip-existing",
    is_flag=True,
    help="Skip problems that already have a problem.md file",
)
@click.option(
    "--delay",
    type=float,
    default=2.0,
    help="Delay between downloads in seconds (default: 2.0)",
)
def download(csv_path, problems, output, skip_existing, delay):
    """Download LeetCode problems using a browser."""
    all_problems = load_problems_from_csv(csv_path)

    # Filter by problem numbers if specified
    if problems:
        all_problems = filter_problems_by_numbers(all_problems, list(problems))
        if not all_problems:
            click.echo(f"No problems found matching numbers: {problems}")
            return

    # Create output directory
    output.mkdir(parents=True, exist_ok=True)

    # Download
    download_problems(
        all_problems,
        output,
        skip_existing=skip_existing,
        delay_between=delay,
    )


@main.command()
@click.option(
    "--csv",
    "csv_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Path to CSV file containing problems",
)
@click.option(
    "--problems-dir",
    type=click.Path(path_type=Path),
    default="problems",
    help="Directory where problems are stored (default: problems/)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="Output path for index file (default: {csv_basename}.md)",
)
def index(csv_path, problems_dir, output):
    """Generate a markdown index of problems and solutions."""
    # Load problems from CSV
    all_problems = load_problems_from_csv(csv_path)

    # Determine output path
    if output is None:
        output = csv_path.with_suffix(".md")

    # Generate index
    result_path = generate_index(all_problems, problems_dir, output)
    click.echo(f"Generated index at {result_path}")


@main.command()
@click.option(
    "--csv",
    "csv_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Path to CSV file containing problems",
)
@click.option(
    "--problems",
    "-p",
    multiple=True,
    type=int,
    help="Specific problem numbers to generate PDFs for (can be repeated)",
)
@click.option(
    "--problems-dir",
    type=click.Path(path_type=Path),
    default="problems",
    help="Directory where problems are stored (default: problems/)",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force regeneration even if PDF is newer than source files",
)
def pdf(csv_path, problems, problems_dir, force):
    """Generate PDF files for problems with solutions."""
    # Load problems from CSV
    all_problems = load_problems_from_csv(csv_path)

    # Filter by problem numbers if specified
    if problems:
        all_problems = filter_problems_by_numbers(all_problems, list(problems))
        if not all_problems:
            click.echo(f"No problems found matching numbers: {problems}")
            return

    generate_all_pdfs(all_problems, problems_dir, force=force)


@main.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to (default: 127.0.0.1)")
@click.option("--port", default=8000, type=int, help="Port to listen on (default: 8000)")
@click.option(
    "--problems-dir",
    type=click.Path(path_type=Path),
    default="problems",
    help="Directory where problems are stored (default: problems/)",
)
@click.option(
    "--index",
    "index_csv",
    type=click.Path(path_type=Path),
    default="problem-index.csv",
    help="Path to problem-index.csv (default: problem-index.csv)",
)
def serve(host, port, problems_dir, index_csv):
    """Start the web browser for viewing problems and solutions."""
    import uvicorn

    templates_dir = Path(__file__).parent.parent.parent / "templates"
    configure_server(problems_dir, index_csv, templates_dir)
    click.echo(f"Starting leet-help browser at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    main()
