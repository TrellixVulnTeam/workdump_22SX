#!/usr/bin/env python
import re
import sys

tex_path = sys.argv[1]
with open(tex_path, 'r') as f: tex = f.read()

for i in range(10):
    tex = re.sub(r"\(([^()\n]*?)\((.*?)\)([^()\n]*?)\)", r"\\pr{\1(\2)\3}", tex)

with open(tex_path, 'w') as f: f.write(tex)
