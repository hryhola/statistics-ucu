"""Highlight editable Python snippets; --from-notebooks refreshes their sources."""
import argparse
import json
from pathlib import Path

from pygments import highlight
from pygments.formatters import LatexFormatter
from pygments.lexers import PythonLexer
from pygments.style import Style
from pygments.token import Comment, Keyword, Name, Number, Operator, String


class ReportStyle(Style):
    default_style = ""
    styles = {
        Comment: "italic #527A65",
        Keyword: "bold #315A9E",
        Name.Builtin: "#754399",
        Name.Function: "#754399",
        Number: "#9C4B17",
        Operator: "#43556B",
        String: "#A13E40",
    }


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--from-notebooks", action="store_true")
args = parser.parse_args()
report_dir = Path(__file__).resolve().parent
code_dir = report_dir / "code"
code_dir.mkdir(exist_ok=True)

if args.from_notebooks:
    notebooks_dir = report_dir.parent.parent / "notebooks"
    for path in sorted(notebooks_dir.glob("task2-part*.ipynb")):
        notebook = json.loads(path.read_text())
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                source = "".join(cell["source"]).rstrip() + "\n"
                (code_dir / f"{cell['id']}.py").write_text(source)

output_dir = report_dir / "build" / "code"
output_dir.mkdir(parents=True, exist_ok=True)
formatter = LatexFormatter(style=ReportStyle, commandprefix="PY")
(output_dir / "style.tex").write_text(formatter.get_style_defs())
for source in sorted(code_dir.glob("*.py")):
    (output_dir / f"{source.stem}.tex").write_text(
        highlight(source.read_text(), PythonLexer(), formatter)
    )
print(f"Highlighted {len(list(code_dir.glob('*.py')))} Python snippets.")
