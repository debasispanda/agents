from pathlib import Path
import re

NOTES_DIR = (Path(__file__).parents[1] / "notes").resolve()

def list_files() -> list[str]:
    """
    List all the markdown files in the notes directory matching
    a glob pattern.
    """
    return [f.name for f in sorted(NOTES_DIR.glob("*.md"))]

def grep(pattern: str, max_results: int = 30) -> list[str]:
    """
    Search files that matches with a pattern
    """
    rx = re.compile(pattern, re.IGNORECASE)
    hits = []
    for f in sorted(NOTES_DIR.glob("*.md")):
        lines = f.read_text().splitlines()
        for i, l in enumerate(lines, start=1):
            if rx.search(l):
                hits.append(f"{f.name}:{i} {l.strip()}")
            if (len(hits) >= max_results):
                return hits

    return hits

def read_file(file_name: str) -> str:
    """
    Read a markdown file by file name in notes directory. Raise error if path is outside notes directory.
    """
    file_path = (NOTES_DIR / file_name).resolve()
    if not file_path.is_relative_to(NOTES_DIR):
        raise ValueError(f"File {file_name} is not found in notes directory")

    return file_path.read_text()
