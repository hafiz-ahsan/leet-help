"""Web server for browsing problems and solutions."""

import csv
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="leet-help", docs_url=None, redoc_url=None)

_problems_dir: Path = Path("problems")
_index_csv: Path = Path("problem-index.csv")
_templates_dir: Path = Path("templates")


def configure(problems_dir: Path, index_csv: Path, templates_dir: Path) -> None:
    global _problems_dir, _index_csv, _templates_dir
    _problems_dir = problems_dir
    _index_csv = index_csv
    _templates_dir = templates_dir


def _load_index() -> list[dict]:
    if not _index_csv.exists():
        return []
    rows = []
    with open(_index_csv, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


@app.get("/", response_class=HTMLResponse)
def index():
    html = (_templates_dir / "browser.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html)


@app.get("/api/problems")
def get_problems(difficulty: str = "", category: str = ""):
    problems = _load_index()
    if difficulty:
        problems = [p for p in problems if p["Difficulty"].lower() == difficulty.lower()]
    if category:
        problems = [p for p in problems if p["Category"].lower() == category.lower()]
    return problems


@app.get("/api/problems/{number}/solutions")
def get_solutions(number: int):
    rows = _load_index()
    match = next((r for r in rows if int(r["Number"]) == number), None)
    if not match:
        raise HTTPException(status_code=404, detail="Problem not found")

    slug = match["URL"].rstrip("/").split("/")[-1]
    problem_dir = _problems_dir / f"{number}-{slug}"

    result = {"problem": None, "solutions": []}

    problem_file = problem_dir / "problem.md"
    if problem_file.exists():
        result["problem"] = problem_file.read_text(encoding="utf-8")

    for md_file in sorted(problem_dir.glob("solution-*.md")):
        label = md_file.stem.replace("solution-", "").replace("-", " ").title()
        result["solutions"].append({
            "label": label,
            "filename": md_file.name,
            "content": md_file.read_text(encoding="utf-8"),
        })

    return result
