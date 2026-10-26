"""Виконати ноутбуки завдання 3 у чистих Python-ядрах та зберегти виходи.

Без аргументів виконуються обидва ноутбуки; `python run_notebooks.py problem6`
виконує лише ноутбуки, назва яких містить "problem6".
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

task_dir = Path(__file__).resolve().parent
paths = sorted(task_dir.glob("task3-problem*.ipynb"))
if len(sys.argv) > 1:
    paths = [path for path in paths if any(name in path.name for name in sys.argv[1:])]
for path in paths:
    print(f"Виконується {path.name}", flush=True)
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook, timeout=900, kernel_name="python3",
        resources={"metadata": {"path": str(task_dir)}},
    )
    client.execute()
    nbformat.write(notebook, path)
    print(f"Збережено {path.name}", flush=True)
