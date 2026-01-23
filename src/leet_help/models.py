"""Data models for leet-help."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Problem:
    """Represents a LeetCode problem."""

    number: int
    title: str
    acceptance: str
    difficulty: str
    url: str

    @property
    def slug(self) -> str:
        """Extract slug from URL (e.g., 'two-sum' from 'https://leetcode.com/problems/two-sum/')."""
        # URL format: https://leetcode.com/problems/two-sum/
        parts = self.url.rstrip("/").split("/")
        return parts[-1]

    @property
    def directory_name(self) -> str:
        """Generate directory name (e.g., '1-two-sum')."""
        return f"{self.number}-{self.slug}"

    def get_problem_dir(self, base_dir: Path) -> Path:
        """Get the problem directory path."""
        return base_dir / self.directory_name
