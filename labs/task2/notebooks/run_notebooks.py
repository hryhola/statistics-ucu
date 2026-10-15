"""Execute every Task 2 notebook in a separate fresh kernel and save outputs."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

task_dir = Path(__file__).resolve().parent
for path in sorted(task_dir.glob("task2-part*.ipynb")):
    print(f"Running {path.name}", flush=True)
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(
        notebook, timeout=600, kernel_name="statistics-ucu",
        resources={"metadata": {"path": str(task_dir)}},
    )
    client.execute()
    nbformat.write(notebook, path)
    print(f"Saved {path.name}", flush=True)
