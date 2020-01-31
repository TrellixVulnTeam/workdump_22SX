import re

def find_start(pre, opening, tex, regex_shit="", offset=-1):
    begin = regex_shit + pre + opening
    try:
        return re.search(begin, tex).start() + len(begin) - len(regex_shit) + offset
    except Exception as e:
        raise Exception("WAH NO START", e)

def find_end(start, tex, opening, closing):
    bal = 1
    for i in range(start + 1, len(tex)):
        if tex[i] == opening: bal += 1
        if tex[i] == closing: bal -= 1
        if bal == 0: return i
    raise Exception("WAH NO END")

tex_path = "analysis.tex"
pre = r""
(opening, closing, regex_shit) = ("(", ")", "\\")

with open(tex_path, 'r') as f: tex = f.read()

while(True):
    try:
        start = find_start(pre, opening, tex, regex_shit)
        end = find_end(start, tex, opening, closing)
        print(start, tex[start])
        print(end, tex[end])
        tex = tex[ :start] + "\\pr{" + tex[start - 1:end] + "}" + tex[end + 1: ]
    except Exception as e:
        print(e)
        break

with open("format_" + tex_path, 'w') as f: f.write(tex)
print("File written: ", "format_" + tex_path)

"""
def find_start(pre, opening, tex):
    begin = pre + opening
    try:
        return re.search(begin, tex).start() + len(begin) - 2
    except Exception as e:
        raise Exception("WA", e)

def find_end(start, tex, opening, closing):
    bal = 1
    for i in range(start + 1, len(tex)):
        if tex[i] == opening: bal += 1
        if tex[i] == closing: bal -= 1
        if bal == 0: return i
    raise Exception("WA")

tex_path = "analysis.tex"
pre = r"\\PR!!"
(opening, closing) = (r"{", r"}")

with open(tex_path, 'r') as f: tex = f.read()

while(True):
    try:
        start = find_start(pre, opening, tex)
        end = find_end(start, tex, opening, closing)
        print(start, tex[start])
        print(end, tex[end])
        tex_list = list(tex)
        tex_list[start] = '('
        tex_list[end] = ')'
        tex = "".join(tex_list)
    except Exception as e:
        print(e)
        break

with open(tex_path, 'w') as f: f.write(tex)
print("File written: ", tex_path)
"""