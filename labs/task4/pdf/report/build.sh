#!/bin/sh
# Compile the current LaTeX source and exported notebook content.
set -eu
cd "$(dirname "$0")"
mkdir -p build ../output/pdf
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build Task_4_Report.tex
cp build/Task_4_Report.pdf ../output/pdf/Task_4_Final_Report.pdf
