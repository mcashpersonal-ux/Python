#!/usr/bin/env python3
import pathlib
import re
def norm(t):
    out=[]
    for ch in t:
        if ch in "\uf8cf\ufe0f":
            continue
        out.append(ch)
    t="".join(out)
    t=t.replace(",,",",")
    t=t.replace(" ,",",")
    t=t.replace(", "," ,")
    t=t.replace(".",".")
    t=re.sub(r"\(\s*\.\s*\)","()",t)
    return t
def main():
    fs=sorted(pathlib.Path("docs").rglob("*.md"))
    total=0
    for f in fs:
        t=f.read_text(encoding="utf-8")
        c=norm(t)
        if c!=t:
            f.write_text(c,encoding="utf-8")
            total+=1
            print("fixed",f)
    print("files fixed:",total)
if __name__=="__main__":
    main()