"""CLI entry point for leet-help."""

import click
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .downloader import download_problems
from .solver import solve_problems, load_config
from .indexer import generate_index
from .pdf_generator import generate_all_pdfs
from .utils import load_problems_from_csv, filter_problems_by_numbers


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
    if not csv_path and not problems:
        raise click.UsageError("Either --csv or --problems must be specified")

    # Load problems from CSV if provided
    if csv_path:
        all_problems = load_problems_from_csv(csv_path)
    else:
        raise click.UsageError("--csv is required to get problem metadata")

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
    help="Path to CSV file containing problems",
)
@click.option(
    "--problems",
    "-p",
    multiple=True,
    type=int,
    help="Specific problem numbers to solve (can be repeated)",
)
@click.option(
    "--problems-dir",
    type=click.Path(path_type=Path),
    default="problems",
    help="Directory where problems are stored (default: problems/)",
)
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default="config.yaml",
    help="Path to config file (default: config.yaml)",
)
@click.option(
    "--model",
    "-m",
    multiple=True,
    help="Model(s) to use (can be repeated for multiple models)",
)
@click.option(
    "--timestamp",
    is_flag=True,
    help="Include timestamp in output filename (allows multiple runs)",
)
def solve(csv_path, problems, problems_dir, config_path, model, timestamp):
    """Generate solutions for problems using LLM."""
    if not csv_path and not problems:
        raise click.UsageError("Either --csv or --problems must be specified")

    # Load config
    config = load_config(config_path)

    # Load problems from CSV if provided
    if csv_path:
        all_problems = load_problems_from_csv(csv_path)
    else:
        raise click.UsageError("--csv is required to get problem metadata")

    # Filter by problem numbers if specified
    if problems:
        all_problems = filter_problems_by_numbers(all_problems, list(problems))
        if not all_problems:
            click.echo(f"No problems found matching numbers: {problems}")
            return

    # Convert model tuple to list (or None if empty)
    models = list(model) if model else None

    # Solve
    solve_problems(
        all_problems,
        problems_dir,
        config,
        models=models,
        include_timestamp=timestamp,
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

    # Get problemset name from CSV filename (e.g., "grind75" from "grind75.csv")
    problemset_name = csv_path.stem

    # Generate PDFs
    generate_all_pdfs(all_problems, problems_dir, problemset_name, force=force)


if __name__ == "__main__":
    main()
