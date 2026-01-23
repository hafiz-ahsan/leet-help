"""Generate solutions for LeetCode problems using LLM."""

import shutil
import subprocess
import re
from datetime import datetime
from pathlib import Path

import yaml

from .models import Problem


def check_llm_available() -> None:
    """Check if llm CLI is available in PATH. Raises RuntimeError if not found."""
    if shutil.which("llm") is None:
        raise RuntimeError(
            "llm command not found in PATH.\n"
            "Please install Simon Willison's llm CLI tool:\n"
            "  pipx install llm\n"
            "  # or\n"
            "  brew install llm\n"
            "\n"
            "Then configure your API keys:\n"
            "  llm keys set openai\n"
            "  llm keys set anthropic"
        )


def load_config(config_path: Path) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_reference_solutions(problem_number: int, reference_dirs: list[str]) -> list[dict]:
    """
    Find existing solutions for a problem in reference directories.

    Searches for directories matching the pattern {number}-* (e.g., 1-TwoSum).

    Returns a list of dicts with 'path' and 'content' keys.
    """
    references = []
    pattern = re.compile(rf"^{problem_number}-")

    for ref_dir in reference_dirs:
        ref_path = Path(ref_dir)
        if not ref_path.exists():
            continue

        # Search recursively for directories matching the pattern
        for subdir in ref_path.rglob("*"):
            if subdir.is_dir() and pattern.match(subdir.name):
                # Found a matching directory, read all code files
                for code_file in subdir.iterdir():
                    if code_file.is_file() and code_file.suffix in (".py", ".java", ".cpp", ".js", ".md"):
                        try:
                            content = code_file.read_text(encoding="utf-8")
                            references.append({
                                "path": str(code_file),
                                "filename": code_file.name,
                                "content": content,
                            })
                        except Exception:
                            continue

    return references


def build_reference_section(references: list[dict]) -> str:
    """Build the reference section of the prompt from found solutions."""
    if not references:
        return ""

    sections = ["## Existing Reference Solutions\n"]
    sections.append("The following are existing solutions for this problem that you can learn from:\n")

    for ref in references:
        sections.append(f"### {ref['filename']} (from {Path(ref['path']).parent.name})")
        sections.append(f"```\n{ref['content']}\n```\n")

    return "\n".join(sections)


def build_prompt(problem: Problem, problem_description: str, references: list[dict], config: dict) -> str:
    """Build the full prompt for the LLM."""
    reference_section = build_reference_section(references)

    template = config["prompt"]["template"]
    prompt = template.format(
        problem_description=problem_description,
        reference_section=reference_section,
    )

    return prompt


def get_model_alias(model_name: str, config: dict) -> str:
    """Get the alias for a model name, or return the name if no alias found."""
    for model in config["llm"]["models"]:
        if model["name"] == model_name:
            return model["alias"]
        if model.get("alias") == model_name:
            return model_name
    return model_name


def resolve_model_name(model_input: str, config: dict) -> str:
    """Resolve an alias or model name to the full model name."""
    for model in config["llm"]["models"]:
        if model.get("alias") == model_input or model["name"] == model_input:
            return model["name"]
    # If not found in config, assume it's a valid model name
    return model_input


def call_llm(prompt: str, model: str, system_prompt: str | None = None) -> str:
    """
    Call Simon Willison's llm CLI tool and return the response.

    Args:
        prompt: The prompt to send
        model: The model name (e.g., 'gpt-4', 'claude-3-sonnet')
        system_prompt: Optional system prompt

    Returns:
        The LLM response text
    """
    cmd = ["llm", "-m", model]

    if system_prompt:
        cmd.extend(["-s", system_prompt])

    cmd.append(prompt)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"llm command failed: {result.stderr}")

    return result.stdout


def solve_problem(
    problem: Problem,
    problems_dir: Path,
    config: dict,
    model: str | None = None,
    include_timestamp: bool = False,
) -> Path:
    """
    Generate a solution for a problem using LLM.

    Args:
        problem: The problem to solve
        problems_dir: Base directory where problems are stored
        config: Configuration dict
        model: Model to use (overrides config default)
        include_timestamp: If True, include timestamp in output filename

    Returns:
        Path to the saved solution file
    """
    problem_dir = problem.get_problem_dir(problems_dir)
    problem_file = problem_dir / "problem.md"

    if not problem_file.exists():
        raise FileNotFoundError(f"Problem file not found: {problem_file}. Run download first.")

    # Read problem description
    problem_description = problem_file.read_text(encoding="utf-8")

    # Find reference solutions
    reference_dirs = config.get("reference_directories", [])
    references = find_reference_solutions(problem.number, reference_dirs)

    if references:
        print(f"  Found {len(references)} reference file(s)")

    # Resolve model name
    model_name = model or config["llm"]["default_model"]
    full_model_name = resolve_model_name(model_name, config)
    model_alias = get_model_alias(full_model_name, config)

    print(f"  Using model: {full_model_name} (alias: {model_alias})")

    # Build prompt
    prompt = build_prompt(problem, problem_description, references, config)
    system_prompt = config["prompt"].get("system")

    # Call LLM
    print(f"  Calling LLM...")
    response = call_llm(prompt, full_model_name, system_prompt)

    # Build output filename
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"solution-{model_alias}-{timestamp}.md"
    else:
        output_filename = f"solution-{model_alias}.md"

    output_path = problem_dir / output_filename

    # Build full output content with metadata
    output_content = f"""# Solution for {problem.number}. {problem.title}

**Generated by:** {full_model_name}
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source:** <{problem.url}>

---

{response}
"""

    output_path.write_text(output_content, encoding="utf-8")
    print(f"  Saved to {output_path}")

    return output_path


def solve_problems(
    problems: list[Problem],
    problems_dir: Path,
    config: dict,
    models: list[str] | None = None,
    include_timestamp: bool = False,
) -> list[Path]:
    """
    Generate solutions for multiple problems.

    Args:
        problems: List of problems to solve
        problems_dir: Base directory where problems are stored
        config: Configuration dict
        models: List of models to use (will generate a solution for each model)
        include_timestamp: If True, include timestamp in output filenames

    Returns:
        List of paths to saved solution files
    """
    # Check that llm CLI is available
    check_llm_available()

    saved_files = []
    total = len(problems)

    # Use default model if none specified
    if not models:
        models = [config["llm"]["default_model"]]

    print(f"Solving {total} problems with {len(models)} model(s)")

    for i, problem in enumerate(problems, 1):
        for model in models:
            print(f"[{i}/{total}] Solving {problem.number}. {problem.title} with {model}...")
            try:
                path = solve_problem(
                    problem,
                    problems_dir,
                    config,
                    model=model,
                    include_timestamp=include_timestamp,
                )
                saved_files.append(path)
            except FileNotFoundError as e:
                print(f"  ERROR: {e}")
            except Exception as e:
                print(f"  ERROR: Failed to solve: {e}")

    print(f"\nGenerated {len(saved_files)} solution(s)")
    return saved_files
