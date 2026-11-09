"""Виконати завершені частини (1), (2) і (3) у чистих ядрах.

Аргумент part1, part2 або part3 обмежує запуск відповідним ноутбуком.
Опціональні комірки з тегом skip-execution не виконуються.
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

notebooks_dir = Path(__file__).resolve().parent
paths = sorted(notebooks_dir.glob("task4-problem7-part[123]-*.ipynb"))
if len(sys.argv) > 1:
    paths = [path for path in paths if any(part in path.name for part in sys.argv[1:])]
if not paths:
    raise SystemExit("Оберіть part1, part2 або part3.")
for path in paths:
    notebook = nbformat.read(path, as_version=4)
    print(f"Виконується {path.name}", flush=True)
    client = NotebookClient(
        notebook, timeout=1800, kernel_name="python3", skip_cells_with_tag="skip-execution",
        resources={"metadata": {"path": str(notebooks_dir)}},
    )
    client.execute()
    nbformat.write(notebook, path)
    print(f"Збережено {path.name}", flush=True)
