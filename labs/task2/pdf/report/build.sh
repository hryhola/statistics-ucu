#!/bin/sh
# Compile the editable report; does not regenerate or overwrite its LaTeX source.
set -eu
cd "$(dirname "$0")"
mkdir -p build ../output/pdf
task2_python="${TASK2_PYTHON:-../../../../.venv/bin/python}"
if [ ! -x "$task2_python" ]; then
    task2_python=python3
fi
"$task2_python" prepare_code.py
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build Task_2_Report.tex
cp build/Task_2_Report.pdf ../output/pdf/Task_2_Final_Report.pdf
