# save this as clean_notebook_whitespace.py
import sys
from pathlib import Path

import nbformat

def clean_source_lines(lines, max_blank_lines=1):
    cleaned = []
    blank_count = 0
    for line in lines:
        # Remove trailing spaces
        stripped = line.rstrip()
        if stripped == "":
            blank_count += 1
            if blank_count <= max_blank_lines:
                cleaned.append("")
        else:
            blank_count = 0
            cleaned.append(stripped)
    # Keep newline endings in notebook format
    return [l + "\n" for l in cleaned]

def clean_notebook(path):
    nb = nbformat.read(path, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == "code" and isinstance(cell.get("source"), str):
            # Split into lines, clean, and join back
            lines = cell["source"].splitlines()
            cell["source"] = "".join(clean_source_lines(lines))

    backup = Path(path).with_suffix(".bak.ipynb")
    Path(path).rename(backup)
    nbformat.write(nb, path)
    print(f"Cleaned notebook saved as {path}")
    print(f"Backup of original saved as {backup}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_notebook_whitespace.py <notebook.ipynb>")
        sys.exit(1)
    clean_notebook(sys.argv[1])