# 22 — Testing & Debugging

> Tests catch regressions early and document expected behavior.
> Write them before fixing bugs- a test that fails first proves
> the bug existed and that your fix works.u

---

##pytest- first test

```python
# test_math.py
def add(a,b):
    return a + b

def test_add():
    assert add(2, 3) == 5

def test_add_strings():
    assert add("a", "b") == "ab"
```

Run with: pytest. pytest finds test_* functions automatically,
asserting with plain assert (no unittest ceremony). Failure output
shows the full diff for easy diagnosis.u

---

##parametrize- one test,many cases

```python
import pytest

def add(a,b):
    return a + b

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0.1, 0.2, 0.30000000000000004),
])
def test_add(a, b, expected):
    assert add(a,b) == expected
```

Parametrize runs the same body over a table of cases- one
failure names the failing row. Beware float rounding- pick exact
expected values or use pytest.approx.u

---

##fixtures- shared setup

```python
import pytest

@pytest.fixture
def db():
    conn = {"data": {}}
    yield conn
    conn.clear()

def test_insert(db):
    db["data"]["k"] = 1
    assert db["data"]["k"] == 1

def test_empty(db):
    assert db["data"] == {}
```

Fixture yeilds setup thene teardown- fresh state per test. Each
test gets its own db,so tests cannot leak into each other.

Order does not matter- fixtures compose via dependency.u

---

##temporary files- tmp_path

```python
import pytest

def test_write(tmp_path):
    f = tmp_path / "out.txt"
    f.write_text("hello")
    assert f.read_text() == "hello"
```

tmp_path gives each test a fresh temp dir- cleaned up
automatically. Perfect for file-based code without polluting
the repo. No need to hand-roll mkdtemp/rmtree.u

---

##mocking- unittest.mock

```python
from unittest.mock import Mock

def fetch_data(client):
    return client.get("url").json()

client = Mock()
client.get.return_value.json.return_value = {"ok": True}
resp = fetch_data(client)
assert resp["ok"] is True
```

Mock replaces slow or flaky dependencies (APIs, clock, random).
Set up return chains via .return_value. assert_called_with
verifies args afterward. Mock only for boundaries- not the logic
you own.u

---

##debugging- pdb

```python
def divide(a,b):
    result = a / b
    return result

def main():
    x = divide(10, 2)
    breakpoint()
    print(x * 2)
```

breakpoint() drops you into pdb at that line- inspect vars,
step with n, print with p, continue with c. For non-interactive
use, add temporary print() or logging.debug(u

---

##assertraises- testing errors

```python
import pytest

def validate(n):
    if n < 0:
        raise ValueError("negative")
    return n

def test_validates():
    with pytest.raises(ValueError):
        validate(-1)
```

pytest.raises asserts the block raises- failing if it does?t.**
You can repr(e.value) for the message, or match= regex. Test the
happy path too- errors are not the only contract.u

---

##Next steps

go to Type Hints at advanced/type-hints.md