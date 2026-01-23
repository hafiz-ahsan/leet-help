"""Generate markdown index of problems and solutions."""

from pathlib import Path

from .models import Problem


def find_solution_files(problem_dir: Path) -> list[tuple[str, Path]]:
    """
    Find all solution files in a problem directory.

    Returns list of (model_name, file_path) tuples.
    """
    solutions = []
    if not problem_dir.exists():
        return solutions

    for f in problem_dir.glob("solution-*.md"):
        # Extract model name from filename: solution-{model}.md
        model_name = f.stem.replace("solution-", "")
        solutions.append((model_name, f))

    # Sort by model name for consistent ordering
    solutions.sort(key=lambda x: x[0])
    return solutions


def generate_index(
    problems: list[Problem],
    problems_dir: Path,
    output_path: Path,
) -> Path:
    """
    Generate a markdown index file with links to all problems and solutions.

    Args:
        problems: List of problems from CSV
        problems_dir: Directory containing problem folders
        output_path: Path for the output markdown file

    Returns:
        Path to the generated index file
    """
    # First pass: collect all unique model names across all problems
    all_models = set()
    problem_solutions = {}

    for problem in problems:
        problem_dir = problem.get_problem_dir(problems_dir)
        solutions = find_solution_files(problem_dir)
        problem_solutions[problem.number] = solutions
        for model_name, _ in solutions:
            all_models.add(model_name)

    # Sort model names for consistent column ordering
    model_names = sorted(all_models)

    # Build the markdown content
    lines = []
    lines.append("# LeetCode Study Index\n")
    lines.append("")
    lines.append(f"Generated from problems in `{problems_dir}/`\n")
    lines.append("")

    # Build header row
    header = "| # | Title | Difficulty | LC | Problem |"
    separator = "|---|-------|------------|----|---------"
    for model in model_names:
        # Capitalize model name for header
        display_name = model.replace("-", " ").title()
        header += f" {display_name} |"
        separator += "|--------"
    separator += "|"

    lines.append(header)
    lines.append(separator)

    # Build data rows
    for problem in problems:
        problem_dir = problem.get_problem_dir(problems_dir)
        problem_file = problem_dir / "problem.md"
        solutions = problem_solutions[problem.number]

        # Create a dict for quick lookup
        solution_dict = {name: path for name, path in solutions}

        # LC link
        lc_link = f"[LC]({problem.url})"

        # Problem link (if exists)
        if problem_file.exists():
            problem_link = f"[Problem]({problem_file})"
        else:
            problem_link = "-"

        row = f"| {problem.number} | {problem.title} | {problem.difficulty} | {lc_link} | {problem_link} |"

        # Add solution columns
        for model in model_names:
            if model in solution_dict:
                solution_path = solution_dict[model]
                row += f" [Solution]({solution_path}) |"
            else:
                row += " - |"

        lines.append(row)

    # Add summary
    lines.append("")
    lines.append("---")
    lines.append("")
    total_problems = len(problems)
    problems_with_content = sum(
        1 for p in problems
        if (p.get_problem_dir(problems_dir) / "problem.md").exists()
    )
    total_solutions = sum(len(sols) for sols in problem_solutions.values())

    lines.append(f"**Total:** {total_problems} problems, {problems_with_content} downloaded, {total_solutions} solutions")
    lines.append("")

    # Write the file
    content = "\n".join(lines)
    output_path.write_text(content, encoding="utf-8")

    return output_path
