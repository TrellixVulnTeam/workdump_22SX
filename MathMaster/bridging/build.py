#!/usr/bin/env python
import re
import os
import shutil
import subprocess
import sys

tex_path = sys.argv[1]
check_call = lambda s: subprocess.check_call(s, shell=True)
build_dir = os.path.dirname(tex_path)
build_delimiter = "___"
build_path = os.path.join(build_dir, build_delimiter + os.path.basename(tex_path))
pdf_path = build_path.replace(".tex", ".pdf")

def transpile(build_path, max_nested=10):
    with open(build_path, 'r') as f:
        tex = f.read()
    for _ in range(max_nested):
        tex = re.sub(r"\(([^()\n]*?)\((.*?)\)([^()\n]*?)\)", r"\\pr{\1(\2)\3}", tex)
    with open(build_path, 'w') as f:
        f.write(tex)

def clean(build_dir, build_path):
    unwanted_extensions = [".aux", ".log", ".out"]
    unwanted_files = [file for file in os.listdir(build_dir)
                      if any((file.endswith(ext) for ext in unwanted_extensions))]
    unwanted_files += [build_path]
    map(os.remove, unwanted_files)

if __name__ == '__main__':
    shutil.copy(tex_path, build_path)
    transpile(build_path)
    check_call("pdflatex -halt-on-error '{}'".format(build_path))
    shutil.move(pdf_path, pdf_path.replace(build_delimiter, ""))
    clean(build_dir, build_path)
    print("SUCCESS")
