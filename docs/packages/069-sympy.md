# 67 — Symbolic math with SymPy

> `sympy` does exact, symbolic math — algebra, calculus, equation
> solving — as opposed to NumPy/SciPy's numeric approximations. Useful
> for deriving formulas, not for crunching large datasets.

---

## install

```bash
pip install sympy
```

---

## symbols and expressions

```python
import sympy as sp

x, y = sp.symbols("x y")
expr = x**2 + 2*x*y + y**2
print(sp.expand(expr))
print(sp.factor(expr)) # (x + y)**2
```

---

## solve equations

```python
x = sp.symbols("x")
solutions = sp.solve(sp.Eq(x**2 - 4, 0), x)
print(solutions) # [-2, 2]

# system of equations
x, y = sp.symbols("x y")
solutions = sp.solve([sp.Eq(x + y, 10), sp.Eq(x - y, 2)], [x, y])
print(solutions) # {x: 6, y: 4}
```

---

## calculus

```python
x = sp.symbols("x")
f = x**3 + 2*x**2

print(sp.diff(f, x)) # derivative: 3*x**2 + 4*x
print(sp.integrate(f, x)) # antiderivative
print(sp.integrate(f, (x, 0, 2))) # definite integral, 0 to 2
print(sp.limit(sp.sin(x) / x, x, 0)) # 1
```

---

## substitute values and convert to numeric functions

```python
x = sp.symbols("x")
f = x**2 + 1

print(f.subs(x, 3)) # 10, still a sympy object

numeric_f = sp.lambdify(x, f, "numpy") # fast numpy-callable function
print(numeric_f(3)) # 10 as a plain number
```

`lambdify` is the bridge from symbolic derivation to fast numeric
evaluation with NumPy — derive the formula in sympy, then evaluate it at
scale with the lambdified version.

---

## error handling basics

```python
import sympy as sp

x = sp.symbols("x")
try:
    result = sp.solve(sp.Eq(sp.log(x), -1), x)
except NotImplementedError as e:
    print("sympy could not solve this symbolically:", e)
```

Not every equation has a closed-form symbolic solution — `sympy` will
raise or return an empty list rather than fall back to a numeric
approximation.

---

## snippets box

```python
# pretty-print in a notebook
sp.init_printing()
```

```python
# simplify a messy expression
sp.simplify((x**2 - 1) / (x - 1)) # x + 1
```

---

## when to use what

| Need | Package |
|---|---|
| Exact/symbolic math, derivations | `sympy` |
| Numeric approximation at scale | `numpy` / `scipy` |

Next door: `lambdify` a derived formula, then vectorize it over a NumPy
array of real sensor data.
