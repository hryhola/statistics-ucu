"""Check report provenance and basic PDF structure after building (requires PyMuPDF)."""
import ast
import hashlib
import json
import re
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT.parent
pdf_path = ROOT / "output/pdf/Task_3_Final_Report.pdf"
manifest = json.loads((ROOT / "validation/export_manifest.json").read_text())
for name, digest in manifest["notebooks"].items():
    path = TASK / "notebooks" / name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, name
    notebook = json.loads(path.read_text())
    problem = 5 if "problem5" in name else 6
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is not None
            assert not any(o["output_type"] == "error" for o in cell.get("outputs", []))
for name, snippet in manifest["snippets"].items():
    path = next((TASK / "notebooks").glob(f"task3-problem{snippet['problem']}-*.ipynb"))
    notebook = json.loads(path.read_text())
    selected = []
    for part in snippet["parts"]:
        source = "".join(notebook["cells"][part["cell"]]["source"])
        nodes = [ast.get_source_segment(source, n) for n in ast.parse(source).body]
        assert part["statement"] in nodes and part["statement"] in part["source"]
        selected.append(part["source"])
    before, after = snippet["frame"]
    framed = (before + "\n" if before else "") + "\n".join(selected) + "\n" + (after + "\n" if after else "")
    assert (ROOT / "report/generated" / f"{name}.py").read_text() == framed

pdf = pymupdf.open(pdf_path)
text = "\n".join(page.get_text() for page in pdf)
for required in ["1.40493", "0.148857", "55897.5", "9.15862", "1.60109", "2.44653", "0.392684", "4.84965"]:
    assert required in text, required
assert "\ufffd" not in text
assert len(pdf) >= 15
assert sum(len(page.get_images()) for page in pdf) == 9
assert len(pdf.get_toc()) == 17
assert pdf.metadata["title"] == "Завдання 3. Лінійна та нелінійна регресія"
for removed in ["Збережений результат", "Джерела та відтворення", "У цьому завданні ми працюватимемо", "labs/task3/", "requirements-executed"]:
    assert removed not in text, removed
log = (ROOT / "report/build/Task_3_Report.log").read_text()
assert not re.search(r"^!", log, re.MULTILINE)
assert pdf_path.stat().st_mtime >= max(p.stat().st_mtime for p in (ROOT / "report/generated").glob("*.tex"))
for error in ["Overfull", "Missing character:", "! LaTeX Error", "undefined references"]:
    assert error not in log, error
checks = {
    "date": "2026-11-02",
    "pages": len(pdf),
    "code_cells": manifest["code_cells"],
    "saved_output_tables": manifest["tables"],
    "figures": len(manifest["figures"]),
    "notebook_hashes_match": True,
    "selected_statements_match_notebooks": True,
    "key_results_present": True,
    "missing_glyphs_or_overfull_boxes": False,
    "pdf_sha256": hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
}
(ROOT / "validation/final_checks.json").write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(checks, ensure_ascii=False, indent=2))
