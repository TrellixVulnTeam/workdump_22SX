#!/usr/bin/env bash
cd /c/Users/jguzman2/dont_upload/workdump/MathMaster/real_analysis
cp analysis.tex format_analysis.tex
python transpile.py format_analysis.tex
pdflatex format_analysis.tex
bash clean.sh
