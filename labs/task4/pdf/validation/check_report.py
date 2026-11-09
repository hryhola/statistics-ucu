"""Verify provenance, complete outputs, task coverage and the built PDF (adapted from task3)."""
import ast
import base64
import hashlib
import json
import re
from datetime import date
from pathlib import Path
import pymupdf
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
TASK=ROOT.parent
PDF=ROOT/'output/pdf/Task_4_Final_Report.pdf'
manifest=json.loads((ROOT/'validation/export_manifest.json').read_text())
notebooks={}
for name,digest in manifest['notebooks'].items():
    path=TASK/'notebooks'/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest,name
    part=int(re.search(r'part(\d)',name)[1])
    notebooks[part]=json.loads(path.read_text())
    for c in notebooks[part]['cells']:
        if c['cell_type']=='code':
            if 'skip-execution' in c.get('metadata',{}).get('tags',[]):
                assert c['execution_count'] is None and not c.get('outputs')
            else:
                assert c['execution_count'] is not None
                assert not any(o['output_type']=='error' for o in c.get('outputs',[]))
for name,snippet in manifest['snippets'].items():
    selected=[]
    for part in snippet['parts']:
        source=''.join(notebooks[snippet['problem']]['cells'][part['cell']]['source'])
        nodes=[ast.get_source_segment(source,n) for n in ast.parse(source).body]
        assert part['statement'] in nodes
        assert part['source'] in source
        selected.append(part['source'])
    framed=snippet['frame'][0]+'\n'+'\n'.join(selected)+'\n'+snippet['frame'][1]+'\n'
    assert (ROOT/'report/generated'/f'{name}.py').read_text()==framed
assert len(manifest['questions'])==19
for q in manifest['questions']:
    assert q['source']==''.join(notebooks[q['part']]['cells'][q['cell']]['source'])
    assert not(q['part']==2 and q['label'] in ['(б)','(з)','(и)'])
images=0
numeric_values=[]
for saved in manifest['outputs']:
    output=notebooks[saved['part']]['cells'][saved['cell']]['outputs'][saved['output']]
    assert hashlib.sha256(json.dumps(output,sort_keys=True).encode()).hexdigest()==saved['sha256']
    data=output.get('data',{})
    if 'image/png' in data:
        binary=base64.b64decode(''.join(data['image/png']))
        assert any(binary==(TASK/'figures'/f).read_bytes() for f in manifest['figures'])
        images+=1
    if 'text/html' in data:
        soup=BeautifulSoup(''.join(data['text/html']),'html.parser')
        rows=[[c.get_text(strip=True) for c in row.select('th,td')] for row in soup.select('tbody tr')]
        for values in rows:
            assert '...' not in values and '…' not in values, 'Truncated saved table'
        cut=saved.get('cut') or {}
        headers=[c.get_text(strip=True) for c in soup.select('thead tr')[0].select('th,td')]
        if 'rows' in cut: rows=[rows[i] for i in cut['rows']]
        if 'columns' in cut:
            headers=[headers[i] for i in cut['columns']]; rows=[[r[i] for i in cut['columns']] for r in rows]
        # The exporter drops an unnamed integer index column; it is not shown in the PDF.
        if headers and headers[0]=='' and rows and all(re.fullmatch(r'-?\d+',r[0]) for r in rows):
            rows=[r[1:] for r in rows]
        for values in rows:
            numeric_values.extend(v for v in values if re.fullmatch(r'-?\d+(?:\.\d+)?(?:e[+-]?\d+)?',v))
pdf=pymupdf.open(PDF)
text='\n'.join(p.get_text() for p in pdf)
compact=re.sub(r'\s+','',text).replace('−','-')
for value in numeric_values:
    assert value in compact,('missing table value',value)
for value in ['76.2699','963.12802','0.97280328','0.67279019','63.877265241644466','7.763698292506341']:
    assert value in compact,value
assert text.count('Опціональні пункти')==1
assert 'Опціональний пункт' not in text
assert 'Не виконано' not in text
assert 'Збережений результат' not in text
assert 'labs/task4' not in text
assert '\ufffd' not in text
assert images==9 and sum(len(p.get_images()) for p in pdf)==9
assert len(pdf.get_toc())==22
assert all(p.rect.width<p.rect.height for p in pdf)
log=(ROOT/'report/build/Task_4_Report.log').read_text()
for error in ['Overfull','Missing character:','! LaTeX Error','undefined references']:
    assert error not in log,error
assert not re.search(r'^!',log,re.M)
assert PDF.stat().st_mtime >= max(p.stat().st_mtime for p in (ROOT/'report/generated').glob('*.tex'))
checks={'date':str(date.today()),'pages':len(pdf),'code_listings':manifest['code_cells'],
        'output_tables':manifest['tables'],'shortened_tables':manifest.get('shortened_tables',0),'figures':images,'required_subtasks':19,
        'notebook_hashes_match':True,'statements_match_notebooks':True,
        'shown_table_numbers_present':True,'figure_bytes_match_notebooks':True,
        'optional_note_occurs_once':True,'tex_errors_overfull_missing_glyphs':False,
        'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest()}
(ROOT/'validation/final_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
