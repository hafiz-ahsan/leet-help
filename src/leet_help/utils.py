"""Shared utilities for leet-help."""

import csv
from pathlib import Path

from .models import Problem


def load_problems_from_csv(csv_path: Path) -> list[Problem]:
    """Load problems from a CSV file."""
    problems = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip empty rows
            if not row.get("Number") or not row.get("URL"):
                continue
            problems.append(
                Problem(
                    number=int(row["Number"]),
                    title=row["Title"],
                    acceptance=row["Acceptance"],
                    difficulty=row["Difficulty"],
                    url=row["URL"],
                )
            )
    return problems


def filter_problems_by_numbers(
    problems: list[Problem], numbers: list[int]
) -> list[Problem]:
    """Filter problems to only include those with specified numbers."""
    number_set = set(numbers)
    return [p for p in problems if p.number in number_set]
