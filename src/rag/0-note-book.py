# Build tools

# 1. Get the data path
from pathlib import Path
import re

DATA_DIR = (Path(__file__).parent / "data").resolve()

# 2. List all the files in the data directory
data_paths = sorted(DATA_DIR.glob("*.md"))

relative_paths = [str(path.relative_to(DATA_DIR)) for path in data_paths]

# 3. Read file content and split lines
file = DATA_DIR / "02-billing-runbook.md"

text = file.read_text()
lines = text.splitlines()

# Regex match with string
pattern = "connection pool"
rx = re.compile(pattern, re.IGNORECASE)

dummy_lines = [
    "This line contains our pattern connection pool",
    "This line doesn't container our pattern"
]

for line in dummy_lines:
    if(rx.search(line)):
        print("Found!")
    else:
        print("Not found!")

one_file_hits = []

for i, l in enumerate(lines, 1):
    if rx.search(l):
        print('===>')
        rel = file.relative_to(DATA_DIR)
        one_file_hits.append(f"{rel}:{i}: {l.strip()}")