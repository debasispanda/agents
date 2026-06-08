import logging
import shutil
import subprocess
import platform
from pathlib import Path
from configs.constants import GREP_TIMEOUT_SECONDS, READ_MAX_LINES

logger = logging.getLogger(__name__)

NOTE_DIR = (Path(__file__).parents[1] / "notes").resolve()

def _ripgrep_installation_guide() -> str:
    """Return the ripgrep installation guide for current OS"""
    system = platform.system()

    if system == "Darwin":
        return "Install with `brew install ripgrep`"
    
    if system == "Windows":
        return "Install with `winget install BurntSushi.ripgrep.MSVC` or `choco install ripgrep` or `scoop install ripgrep`."
    
    return "Install with your package manager. E.g - `apt-get install ripgrep`"

def list_files(pattern: str = "*.md") -> str:
    """
    List all the markdown files in the notes directory matching a glob pattern
    """
    logger.info("list_files(pattern=%r)", pattern)

    if not NOTE_DIR.exists():
        return f"Error: notes directory is not found at {NOTE_DIR}"
    
    try:
        paths = NOTE_DIR.glob(pattern)
    except (ValueError) as e:
        return f"Error: invalid glob pattern {pattern}: {e}"
    
    matches = sorted(f.name for f in paths if f.is_file())

    if not matches:
        return f"No files matched pattern: {pattern}"
    
    return "\n".join(matches)

def grep(pattern: str, max_results: int = 30, context: int = 0) -> str:
    """
    Search markdown files in notes with ripgrep matching pattern and return matches with `file:line:text` format.

    pattern - keyword(s) that need to search.
    max_results - maximum expected results.
    context - how many surrounding lines to be included in each match(rg -C).
    
    Recently edited files come first via `--sortr=modified`.
    `--no-config` ignores any user `~/.ripgreprc` so behavior is identical across machines.
    """
    logger.info("grep(pattern=%r, max_results=%d, context=%d)", pattern, max_results, context)

    if max_results < 1:
        return "Error: max_results must be equal to 1 or greater"
    if context < 0:
        return "Error: context must be equal to 0 or greater"
    if not shutil.which('rg'):
        return f"Error: ripgrep util ('rg') is not installed. {_ripgrep_installation_guide()}"
    
    cmd = [
        "rg",
        "--line-number",
        "--no-heading",
        "--ignore-case",
        "--no-config",
        "--sortr=modified",
        "--max-count",
        str(max_results),
        "--glob",
        "*.md",
        *(["--context", str(context)] if context > 0 else []),
        "--",
        pattern,
        ".",
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=NOTE_DIR,
            capture_output=True,
            text=True,
            check=False,
            timeout=GREP_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        logger.warning("greo timed out for pattern=%r", pattern)
        return f"Error: grep timed out after {GREP_TIMEOUT_SECONDS} seconds. Try a more specific pattern."

    if result.returncode == 2:
        return f"Error: invalid pattern {pattern!r}: {result.stderr.strip()}"
    if not result.stdout.strip():
        return f"No matches found for pattern: {pattern!r}"
    
    lines = result.stdout.splitlines()

    if len(lines) > max_results:
        lines = lines[:max_results] + [
            f"...truncated to {max_results} matches. Try a more specific pattern."
        ]
    return "\n".join(lines)

def _safe_path(path: str) -> Path | None:
    """
    Resolve an user provided path against the notes directory
    """
    target = (NOTE_DIR / path).resolve()

    if not target.is_relative_to(NOTE_DIR):
        return None
    return target

def read_file(path: str, offset: int = 1, limit: int = READ_MAX_LINES) -> str:
    """
    Read a bounded line range from a file relative to the notes directory.
    path - File name
    offset - 
    """
    logger.info("read_file(path=%r, offset=%d, limit=%d)", path, offset, limit)

    safe = _safe_path(path)

    if safe is None:
        return f"Error: path {path!r} is outside the notes directory."
    if not safe.exists():
        return f"Error: file {path!r} not found!"
    if not safe.is_file():
        return f"Error: path {path!r} is not a file!"
    if offset < 1:
        return "Error: offset must be equal to 1 or greater!"
    if limit < 1:
        return "Error: limit must be equal to 1 or greater!"
    if limit > READ_MAX_LINES:
        return f"Error: limit must be equal to {READ_MAX_LINES} or lesser"
    
    try:
        lines = safe.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return f"Error: {path} is not UTF-8 text"
    
    end = min(offset + limit - 1, len(lines))
    excerpt = lines[offset - 1: end]

    if not excerpt:
        return F"Error: no lines found. {path} has {len(lines)} lines"
    return "\n".join(f"{i}: {line}" for i, line in enumerate(excerpt))
