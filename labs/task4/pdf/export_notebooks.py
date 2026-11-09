"""Build a LaTeX report from saved Task 4 notebooks without rerunning calculations."""
import base64
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

from report_selection import *
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
    body = "\n".join(" & ".join(label(x) for x in r) + r" \\" for r in rows)
    assert bool(notes) == ("note" in cut), (name, notes)
    note = (r"\par\nopagebreak\vspace{1pt}{\itshape\color{black!60}" + latex(cut["note"]) + "}" + "\n") if notes else ""
    if len(rows) <= 20:
        return (r"\Needspace{" + str(30+len(rows)*13) + "pt}\n"
                + r"\begingroup\fontsize{7.5}{9.5}\selectfont\setlength{\tabcolsep}{" + sep + r"}\renewcommand{\arraystretch}{1.12}"
                + r"\par\noindent\begin{tabular}{" + spec + "}\n\\hline\n" + header + "\n\\hline\n" + body
                + "\n\\hline\n\\end{tabular}\n" + note + "\\par\\endgroup\n")
    head = header + "\n\\hline\n"
    return (r"\begingroup\fontsize{7.5}{9.5}\selectfont\setlength{\tabcolsep}{" + sep + r"}\renewcommand{\arraystretch}{1.12}" + "\n"
            + r"\begin{longtable}{" + spec + "}\n\\hline\n" + head
            + r"\endfirsthead" + "\n\\hline\n" + head + r"\endhead" + "\n"
            + r"\hline\endfoot" + "\n" + body + "\n\\end{longtable}\n" + note
            + r"\endgroup" + "\n")

formatter = LatexFormatter(style='friendly', commandprefix='PY')
(GENERATED/'style.tex').write_text(formatter.get_style_defs())
manifest={'notebooks':{},'code_cells':0,'tables':0,'figures':[], 'snippets':{},'outputs':[],'questions':[]}
notebooks={}
for part in [1,2,3]:
    path=next((TASK/'notebooks').glob(f'*part{part}-*.ipynb'))
    notebooks[part]=json.loads(path.read_text())
    manifest['notebooks'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
    for cell in notebooks[part]['cells']:
        if cell['cell_type']=='code' and 'skip-execution' not in cell.get('metadata',{}).get('tags',[]):
            assert cell['execution_count'] is not None
            assert not any(o['output_type']=='error' for o in cell.get('outputs',[]))

def listing(part, ci, prefixes, name=None):
    name=name or f'p{part}-c{ci}'
    code, provenance=chosen_code(notebooks[part],ci,prefixes)
    framed=FRAME[0]+'\n'+code+FRAME[1]+'\n'
    (GENERATED/f'{name}.py').write_text(framed)
    (GENERATED/f'{name}.tex').write_text(highlight(framed,PythonLexer(),formatter))
    manifest['snippets'][name]={'problem':part,'parts':provenance,'frame':FRAME}
    manifest['code_cells']+=1
    return (r'\pythoncodelong{' if framed.count('\n')>42 else r'\pythoncode{')+name+'}'

def outputs(part,ci):
    chunks=[]
    for j,output in enumerate(notebooks[part]['cells'][ci].get('outputs',[])):
        name=f'p{part}-c{ci}-out{j}'
        data=output.get('data',{})
        manifest['outputs'].append({'part':part,'cell':ci,'output':j,'sha256':hashlib.sha256(json.dumps(output,sort_keys=True).encode()).hexdigest()})
        if 'image/png' in data:
            figure,caption=FIGURES[part,ci]
            embedded=base64.b64decode(''.join(data['image/png']))
            assert embedded==(TASK/'figures'/figure).read_bytes(),figure
            chunks.append(r'\begin{figure}[H]\centering'+'\n'+r'\includegraphics[width='+str(FIGURE_WIDTHS.get((part,ci),1))+r'\linewidth,height=0.85\textheight,keepaspectratio]{../../figures/'+figure+'}\n'+r'\caption{'+latex(caption)+'}\n'+r'\end{figure}')
            manifest['figures'].append(figure)
        elif 'text/html' in data:
            cut=TABLE_CUTS.get((part,ci,j))
            manifest['outputs'][-1]['cut']=cut
            chunks.append(table(''.join(data['text/html']),name,cut))
            manifest['tables']+=1
            if cut: manifest['shortened_tables']=manifest.get('shortened_tables',0)+1
        elif 'text/markdown' in data:
            if (part,ci) in MARKDOWN_OUTPUT_NEEDSPACE:
                chunks.append(r'\Needspace{'+str(MARKDOWN_OUTPUT_NEEDSPACE[part,ci])+'pt}')
            chunks.append(markdown(answer_text(''.join(data['text/markdown']))))
        else:
            text=''.join(output.get('text',data.get('text/plain',[]))).strip()
            if not text or text.startswith('<Figure size'):continue
            (GENERATED/f'{name}.txt').write_text(text+'\n')
            # Long summaries can flow; short outputs remain together.
            height=min(600,10+sum(max(1,math.ceil(len(line)/110)) for line in text.splitlines())*9.2)
            if height<210: chunks.append(r'\Needspace{'+str(height)+'pt}')
            chunks.append(r'\resulttext{'+name+'.txt}')
    if (part,ci) in SIDE_BY_SIDE_OUTPUTS:
        assert len(chunks)==2
        chunks=[re.sub(r'\\Needspace\{[^}]+\}', '', c) for c in chunks]
        return (r'\Needspace{120pt}\par\noindent\begin{minipage}[t]{0.49\linewidth}' + chunks[0]
                + r'\end{minipage}\hfill\begin{minipage}[t]{0.49\linewidth}' + chunks[1]
                + r'\end{minipage}\par')
    return '\n\n'.join(chunks)

common=[r'\section*{Спільні припущення та підготовка}',r'\markright{Підготовка}',markdown(INTRO),listing(1,3,COMMON,'common-data'),outputs(1,3)]
(GENERATED/'common.tex').write_text('\n\n'.join(common))
for part in [1,2,3]:
    n=notebooks[part]
    chunks=[r'\section{'+latex(PART_TITLES[part])+'}',r'\markright{Частина '+str(part)+'}']
    # Preserve the assignment's part-level statement.
    statement=''.join(n['cells'][4]['source']).split('\n',1)[1].strip()
    chunks.append(markdown(statement))
    if part==3:
        chunks.extend([listing(3,3,LOGIT_PREP,'logit-data'),outputs(3,3)])
    for qi,ci,ai,title in SECTIONS[part]:
        source=''.join(n['cells'][qi]['source']);heading,body=source.split('\n',1)
        label=heading.removeprefix('### ').strip()
        shown_label=f"{part}.{label.strip('()')}"
        if (part,ci) in PAGE_BREAK_BEFORE_QUESTION:chunks.append(r'\clearpage')
        code_lines = 0
        if (part,ci) in CODE:
            code_lines=len(chosen_code(n,ci,CODE[part,ci])[0].splitlines())+2
        reserve=min(650,90+math.ceil(len(body)/85)*13+(code_lines*11+25 if code_lines<=30 else 80))
        chunks.extend([r'\Needspace{'+str(reserve)+'pt}',r'\subsection{'+latex(shown_label+' '+title)+'}',r'\begin{taskstatement}'+markdown(body)+r'\end{taskstatement}'])
        manifest['questions'].append({'part':part,'cell':qi,'label':label,'source':source})
        if (part,ci) in CODE:
            chunks.extend([listing(part,ci,CODE[part,ci]),outputs(part,ci)])
        if (part,ci) in PAGE_BREAK_BEFORE_ANSWER:chunks.append(r'\clearpage')
        # A sub-task without code has no outputs to interpret: the answer follows the statement directly.
        answer=markdown(refs(answer_text(''.join(n['cells'][ai]['source'])),part))
        chunks.append((r'\answerheading'+'\n' if (part,ci) in CODE else r'\par\medskip'+'\n')+answer)
    (GENERATED/f'part{part}.tex').write_text('\n\n'.join(chunks)+'\n')
(ROOT/'validation/export_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f"Exported {manifest['code_cells']} listings, {manifest['tables']} full tables, {len(manifest['figures'])} figures, {len(manifest['questions'])} questions.")
