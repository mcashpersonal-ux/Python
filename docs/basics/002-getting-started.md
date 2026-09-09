# 01 - Getting Started

> What you need to run Python,how to write your first script,
> and how the REPL works.

---

## Install Python

- **Windows** - download the installer from python.org and check
  "Add Python to PATH" during setup.
- **macOS** - brew install python (or the python.org installer).
- **Linux** - sudo apt install python3 (Debian/Ubuntu,.

Verify it works:

```bash
python --version
python3 --version
```

Tip: keep a scratch folder where you throw tiny test scripts.
Every snippet on this site is fair game to paste into a blank file and run.

---

## Your first program

Create hello.py:

```python
print("Hello,world!")
```

Run it:

```bash
python hello.py
```

print() writes its argument to the terminal - that's the whole hello world.

.

---

## The Python REPL

Types python (or python3) in a terminal and you get an interactive prompt:

```pycon
>>> (7*7)
49
>>> name = "Ada"
>>> name.upper()
'ADA'
>>> exit()
```

The REPL evaluates each line immediately - perfect for testing small ideas
without creating files.

The underscore holds the last result. help() and dir() give in-line docs.
!

---

## Running Python files

| Command | Does what |
|----------|----------|
| python script.py | Runs the script once |
| python -i script.py | Runs then drops into REPL to inspect variables |
| python -m pdb script.py | Runs under the debugger |

---

## Comments - your notes in code

```python
# This line is ignored by Python.
# Use comments to explain the why,not the what.

total = price * qty
```

Docstrings are explained in Functions - they document code that survives
in help().

---

## Next steps

go to Variables and Types at variables-types.md