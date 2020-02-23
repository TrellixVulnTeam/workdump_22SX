#!/usr/bin/env bash
# Use as: { "keys": [ "ctrl+alt+b" ], "command": "exec", "args": { "shell_cmd": "\"C:\\Program Files\\Git\\usr\\bin\\bash.exe\" build.sh" } }
work_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
original_path="analysis.tex"
transpile_path="__analysis.tex"

cd ${work_dir}
cp ${original_path} ${transpile_path}
python transpile.py ${transpile_path}
pdflatex -halt-on-error ${transpile_path} | grep '^!.*' -A200 --color=always
bash clean.sh ${work_dir}
