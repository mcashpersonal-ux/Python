# 69 — Deep learning with PyTorch

> `torch` (PyTorch) provides tensors, automatic differentiation, and
> neural network building blocks. The dominant framework for deep
> learning research and increasingly for production.

---

## install

```bash
pip install torch
```

For GPU support, follow the platform-specific install command from
pytorch.org — the plain `pip install torch` gives you a CPU-only build.

---

## tensors (like NumPy arrays, but with autograd)

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = (x ** 2).sum()
y.backward() # compute gradients
print(x.grad) # d(y)/d(x) = 2x -> [2., 4., 6.]
```

`requires_grad=True` tells PyTorch to track operations on this tensor so
`.backward()` can compute gradients — the core mechanism behind training.

---

## a minimal neural network

```python
import torch
import torch.nn as nn

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 16)
        self.fc2 = nn.Linear(16, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = Net()
sample = torch.randn(1, 4)
print(model(sample))
```

---

## a training loop

```python
import torch
import torch.nn as nn
import torch.optim as optim

model = Net()
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()

X = torch.randn(100, 4)
y = torch.randn(100, 1)

for epoch in range(10):
    optimizer.zero_grad()
    predictions = model(X)
    loss = loss_fn(predictions, y)
    loss.backward()
    optimizer.step()
    print(f"epoch {epoch}: loss={loss.item():.4f}")
```

The pattern is always the same: zero gradients, forward pass, compute
loss, backward pass, optimizer step.

---

## using a GPU when available

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
X = X.to(device)
```

---

## error handling basics

```python
import torch

try:
    a = torch.randn(3, 4)
    b = torch.randn(5, 6)
    a @ b
except RuntimeError as e:
    print("shape/device mismatch:", e)
```

Shape mismatches and device mismatches (one tensor on CPU, one on GPU)
are the two most common `RuntimeError`s — check `.shape` and `.device` on
both operands.

---

## snippets box

```python
# save/load model weights
torch.save(model.state_dict(), "model.pt")
model.load_state_dict(torch.load("model.pt"))
```

```python
# switch to eval mode for inference (disables dropout/batchnorm training behavior)
model.eval()
with torch.no_grad():
    predictions = model(X)
```

---

## when to use what

| Need | Package |
|---|---|
| Neural networks, deep learning | `torch` |
| Classic ML (trees, regression, clustering) | `scikit-learn` |

Next door: preprocess and split data with `scikit-learn`'s utilities
before feeding tensors into a `torch` model.
