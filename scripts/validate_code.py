#!/usr/bin/env python3
import re
import pathlib
import sys
def blocks(t):
    py=re.findall(r"```python\s*\n(.*?)```",t,re.S)
    return py
def ok(p):
    t=p.read_text(encoding="utf-8")
    good=True
    for i,b in enumerate(blocks(t)):
        try:
            compile(b,f"{p.name}:{i}","exec")
        except SyntaxError as e:
            good=False
            print(f"{p.name}:{i} {e.msg} {e.text!r}")
    return good
def main():
    fs=sorted(pathlib.Path("docs").rglob("*.md"))
    bad=[]
    for f in fs:
        if not ok(f):
            bad.append(f)
    print("bad_files=",len(bad))
    if "--fix" in sys.argv:
        for f in fs:
            t=f.read_text(encoding="utf-8")
            c=t.replace("\uf8cf","")
            if c!=t:
                f.write_text(c,encoding="utf-8")
                print("swept",f.name)
    return bad
if __name__=="__main__":
    sys.exit(main())