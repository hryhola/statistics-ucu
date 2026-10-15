"""Export each executed notebook as LaTeX with its embedded figures."""
from pathlib import Path
import nbformat
from nbconvert import LatexExporter
from nbconvert.writers import FilesWriter

pdf_dir = Path(__file__).resolve().parent
notebooks_dir = pdf_dir.parent / "notebooks"
for path in sorted(notebooks_dir.glob("task2-part*.ipynb")):
    notebook = nbformat.read(path, as_version=4)
    destination = pdf_dir / "exports" / path.stem
    destination.mkdir(parents=True, exist_ok=True)
    exporter = LatexExporter()
    body, resources = exporter.from_notebook_node(
        notebook,
        resources={"metadata": {"path": str(notebooks_dir)},
                   "output_files_dir": f"{path.stem}_files"},
    )
    # XeLaTeX fonts with Ukrainian glyphs, including code comments and answers.
    body = body.replace(r"\usepackage{fontspec}", r"""\usepackage{fontspec}
        \setmainfont{STIX Two Text}
        \setsansfont{PT Sans}
        \setmonofont{Menlo}[Scale=0.85]""")
    body = body.replace("∈", r"\ensuremath{\in}")
    body = body.replace(r"\href{../input/", r"\href{../../../input/")
    FilesWriter(build_directory=str(destination)).write(body, resources, notebook_name=path.stem)
    print(f"Exported {path.name} -> {destination.name}/{path.stem}.tex", flush=True)
