"""Build a LaTeX report from saved Task 3 notebooks without rerunning calculations."""
import base64
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

from report_selection import CODE, COMMON, OUTPUTS, TABLE_CUTS, NOTES, FRAME, INTRO, PAGE_BREAK_BEFORE_ANSWER, PAGE_BREAK_BEFORE_QUESTION, select_code, answer_text, frame_code
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import LatexFormatter
from pygments.lexers import PythonLexer

ROOT = Path(__file__).resolve().parent
TASK = ROOT.parent
REPORT = ROOT / "report"
GENERATED = REPORT / "generated"
GENERATED.mkdir(parents=True, exist_ok=True)


def latex(text):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
                    "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
                    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(replacements.get(c, c) for c in str(text))


def markdown(text):
    text = re.sub(r"(?m)(?<=\S)\n(?=(?:[-*] |[0-9]+\. ))", "\n\n", text)
    # Notebook-relative file links cannot be resolved from a standalone report.
    text = re.sub(r"\[([^\]]+)\]\((?!https?://)[^)]+\)", r"\1", text)
    rendered = subprocess.run(["pandoc", "-f", "markdown+tex_math_dollars+autolink_bare_uris", "-t", "latex"],
                              input=text, text=True, check=True, capture_output=True).stdout
    rendered = rendered.replace(r"\def\LTcaptype{none}", "").replace("Скоригований", "Скори\\-гований")
    rendered = rendered.replace("DataDocumentation.txt", r"\newline{}DataDocumentation.txt")
    rendered = rendered.replace("→", r"\ensuremath{\rightarrow}")
    def wrap_table(match):
        count = len(match.group(1))
        usable = 166 - 3 * count
        spec = "".join(r">{\raggedright\arraybackslash}p{" + f"{usable/count:.2f}mm" + "}" for _ in range(count))
        return r"\small\setlength{\tabcolsep}{1.5mm}\begin{longtable}{" + spec + "}"
    return re.sub(r"\\begin\{longtable\}\[\]\{@\{\}([lrc]+)@\{\}\}", wrap_table, rendered)


def table(html, name, cut=None):
    soup = BeautifulSoup(html, "html.parser")
    header_rows = [[x.get_text(" ", strip=True) for x in tr.find_all(["th", "td"])]
                   for tr in soup.find("thead").find_all("tr")]
    headers = list(header_rows[0])
    # pandas prints a named index as an extra header row: keep both the column names and the index name.
    for extra in header_rows[1:]:
        for j, value in enumerate(extra):
            if value and j < len(headers) and not headers[j]:
                headers[j] = value
    rows = [[x.get_text(" ", strip=True) for x in tr.find_all(["th", "td"])]
            for tr in soup.find("tbody").find_all("tr")]
    cut = cut or {}
    notes = []
    if "rows" in cut:
        rows = [rows[i] for i in cut["rows"]]
        notes.append("вибрані рядки")
    if "columns" in cut:
        headers = [headers[i] for i in cut["columns"]]
        rows = [[r[i] for i in cut["columns"]] for r in rows]
        notes.append("вибрані колонки")
    # An unnamed integer row index carries no information next to Order or a scheme name.
    if headers[0] == "" and rows and all(re.fullmatch(r"-?\d+", r[0]) for r in rows):
        headers, rows = headers[1:], [r[1:] for r in rows]
    if "ellipsis_after" in cut:
        rows.insert(cut["ellipsis_after"], ["…"] * len(rows[0]))
    if len(headers) > 9 and len(rows) <= 3:
        headers, rows = [headers[0]] + [r[0] for r in rows], [list(r) for r in zip(headers[1:], *[r[1:] for r in rows])]
    width = max(len(headers), *(len(r) for r in rows))
    headers += [""] * (width - len(headers))
    rows = [r + [""] * (width - len(r)) for r in rows]
    longest = [max([len(headers[j])] + [len(r[j]) for r in rows]) for j in range(width)]
    if sum(longest) * 1.4 + 5 * width <= 150:
        # Narrow tables keep natural column widths instead of being stretched across the page.
        spec = "|" + "l" * width + "|"
        sep = "2.5mm"
    else:
        # Use fixed-width paragraph columns so captions and long labels wrap naturally.
        weights = [longest[j] ** 0.55 for j in range(width)]
        total = sum(weights)
        usable = 165 - 3 * width
        spec = "|" + "".join(r">{\raggedright\arraybackslash}p{" + f"{usable*w/total:.2f}mm" + "}" for w in weights) + "|"
        sep = "1.5mm"
    def label(value):
        escaped = latex(value).replace("Neighborhood", r"Neighbor\-hood")
        return re.sub(r"(?<=[a-z])(?=[A-Z])", lambda _: r"\allowbreak{}", escaped)
    header = " & ".join(label(x) for x in headers) + r" \\"
    body = "\n".join(" & ".join(latex(x) for x in r) + r" \\" for r in rows)
    assert bool(notes) == ("note" in cut), (name, notes)
    note = (r"\par\nopagebreak\vspace{-1pt}{\itshape\color{black!60}" + latex(cut["note"]) + "}" + "\n") if notes else ""
    return (r"\begingroup\fontsize{7.5}{9.5}\selectfont\setlength{\tabcolsep}{" + sep + r"}\renewcommand{\arraystretch}{1.15}" + "\n"
            + r"\par\vspace{2pt}\noindent\begin{tabular}{" + spec + "}\n\\hline\n"
            + header + "\n\\hline\n" + body + "\n\\hline\n\\end{tabular}" + note + "\\par\\vspace{2pt}\n"
            + r"\endgroup" + "\n")



formatter = LatexFormatter(style="friendly", commandprefix="PY")
(GENERATED / "style.tex").write_text(formatter.get_style_defs())
figures = {
    (5, 5): ("problem5_mssubclass.png", "MSSubClass як числовий код і як категоріальна змінна."),
    (5, 8): ("problem5_scatter.png", "Ціна продажу та п'ять числових регресорів."),
    (5, 20): ("problem5_normality.png", "Розподіл і Q-Q графік залишків повної моделі."),
    (5, 26): ("problem5_influence.png", "Залишки, важіль, відстань Кука та нетипові площі."),
    (5, 32): ("problem5_jtest.png", "Схема тесту зі штучними регресорами: прогноз кожної моделі переводимо в шкалу іншої."),
    (5, 35): ("problem5_cv.png", "Фактичні ціни та прогнози LeaveOneOut для двох моделей."),
    (6, 6): ("problem6_linear.png", "Лінійна модель для перших 500 продажів."),
    (6, 9): ("problem6_nonlinear.png", "Порівняння лінійної та експоненційної моделей."),
    (6, 12): ("problem6_residuals.png", "Залишки експоненційної моделі за роком будівництва."),
}
titles = {
    5: ["Тип житла та кодування категорій", "Графічний аналіз", "Проста лінійна регресія",
        "Спільний F-тест для MSSubClass", "Інтерпретація коефіцієнтів", "Довірчий інтервал і нормальність",
        "Покроковий відбір за BIC", "Викиди, важіль і вплив", "Імпутація пропусків",
        "Ціна чи логарифм ціни", "Крос-валідація"],
    6: ["Лінійна модель", "Експоненційна модель", "Статистичні висновки для NLS", "Збіжність і перенавчання"],
}
manifest = {"notebooks": {}, "code_cells": 0, "tables": 0, "figures": [], "snippets": {}}
for problem in [5, 6]:
    path = next((TASK / "notebooks").glob(f"task3-problem{problem}-*.ipynb"))
    notebook = json.loads(path.read_text())
    manifest["notebooks"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    chunks = []
    if problem == 5:
        common, provenance = select_code(notebook, COMMON)
        common = frame_code("common", common)
        (GENERATED / "common.py").write_text(common)
        (GENERATED / "common.tex").write_text(highlight(common, PythonLexer(), formatter))
        manifest["snippets"]["common"] = {"problem": 5, "parts": provenance, "frame": FRAME["common"]}
        chunks.extend([r"\section*{Спільна підготовка}", r"\markboth{Підготовка}{}",
                       markdown(INTRO[5]), r"\pythoncode{common}"])
    question = 0
    last_code = None
    for i, cell in enumerate(notebook["cells"]):
        source = "".join(cell["source"]).strip()
        if cell["cell_type"] == "markdown":
            if source.startswith("# Задача"):
                heading = source.split("\n", 1)[0]
                if problem == 6:
                    chunks.append(r"\clearpage")
                chunks.append(r"\section{" + latex(heading.removeprefix("# ")) + "}")
                chunks.append(r"\markboth{Задача " + str(problem) + "}{}")
                if problem == 6:
                    chunks.append(markdown(INTRO[6]))
            elif source.startswith("## ("):
                heading, body = source.split("\n", 1)
                label = heading.removeprefix("## ")
                title = f"{label} {titles[problem][question]}"
                code_cell = next(c for (p, c) in CODE if p == problem and c > i)
                excerpt, _ = select_code(notebook, CODE[(problem, code_cell)])
                # Keep the heading, the statement and the first lines of code together; code boxes may break.
                reserve = min(420, 105 + math.ceil(len(body) / 85) * 13 + min(len(excerpt.splitlines()), 4) * 10.5)
                if (problem, label) in PAGE_BREAK_BEFORE_QUESTION:
                    chunks.append(r"\clearpage")
                chunks.append(r"\Needspace{" + str(reserve) + "pt}")
                chunks.append(r"\subsection{" + latex(title) + "}")
                chunks.append("\\begin{taskstatement}\n" + markdown(body) + "\\end{taskstatement}\n")
                question += 1
            elif question:
                if (problem, last_code) in PAGE_BREAK_BEFORE_ANSWER:
                    chunks.append(r"\clearpage")
                chunks.append("\\answerheading\n" + markdown(answer_text(source)))
        elif (problem, i) in CODE:
            last_code = i
            assert cell["execution_count"] is not None, (path, i)
            assert not any(o["output_type"] == "error" for o in cell.get("outputs", [])), (path, i)
            name = f"p{problem}-c{i}"
            code, provenance = select_code(notebook, CODE[(problem, i)])
            code = frame_code((problem, i), code)
            (GENERATED / f"{name}.py").write_text(code)
            (GENERATED / f"{name}.tex").write_text(highlight(code, PythonLexer(), formatter))
            manifest["snippets"][name] = {"problem": problem, "parts": provenance, "frame": FRAME[(problem, i)]}
            chunks.append((r"\pythoncodelong{" if code.count("\n") > 32 else r"\pythoncode{") + name + "}")
            manifest["code_cells"] += 1
            for j in OUTPUTS[(problem, i)]:
                output = cell["outputs"][j]
                data = output.get("data", {})
                if "image/png" in data:
                    figure, caption = figures[(problem, i)]
                    saved = (TASK / "figures" / figure).read_bytes()
                    embedded = base64.b64decode("".join(data["image/png"]))
                    assert saved == embedded, (path, i, "saved figure differs from notebook")
                    # All figures stay in portrait orientation at text width (digital reading, no printing).
                    chunks.append("\\begin{figure}[H]\n\\centering\n"
                                  + r"\includegraphics[width=\linewidth,height=0.82\textheight,keepaspectratio]{../../figures/"
                                  + figure + "}\n\\caption{" + latex(caption) + "}\n\\end{figure}\n")
                    manifest["figures"].append(figure)
                elif "text/html" in data:
                    cut = dict(TABLE_CUTS.get((problem, i, j), {}))
                    if (problem, i, j) in NOTES:
                        cut["note"] = NOTES[(problem, i, j)]
                    chunks.append(table("".join(data["text/html"]), name, cut))
                    manifest["tables"] += 1
                else:
                    text = "".join(output.get("text", data.get("text/plain", []))).strip()
                    if not text or text.startswith("<Figure size"):
                        continue
                    out_name = f"{name}-out{j}.txt"
                    (GENERATED / out_name).write_text(text + "\n")
                    text_height = 10 + sum(max(1, math.ceil(len(line) / 110)) for line in text.splitlines()) * 9.2
                    chunks.append(r"\Needspace{" + str(text_height) + "pt}")
                    chunks.append(r"\resulttext{" + out_name + "}")
                    if (problem, i, j) in NOTES:
                        chunks.append(r"\resultnote{" + latex(NOTES[(problem, i, j)]) + "}")
    assert question == len(titles[problem])
    (GENERATED / f"problem{problem}.tex").write_text("\n\n".join(chunks) + "\n")
used = {"style.tex", "problem5.tex", "problem6.tex"}
for name in manifest["snippets"]:
    used.update({name + ".py", name + ".tex"})
for problem in [5, 6]:
    used.update(re.findall(r"\\resulttext\{([^}]+)\}", (GENERATED / f"problem{problem}.tex").read_text()))
for path in GENERATED.iterdir():
    if re.fullmatch(r"p[56]-c[0-9]+(?:-out[0-9]+)?\.(?:py|tex|txt)", path.name) and path.name not in used:
        path.unlink()
(ROOT / "validation" / "export_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(f"Exported {manifest['code_cells']} core listings, {manifest['tables']} selected tables, {len(manifest['figures'])} figures.")
