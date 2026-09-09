# 68 — Classic machine learning with scikit-learn

> `scikit-learn` covers the classic ML toolbox — regression,
> classification, clustering, preprocessing — behind one consistent
> `fit`/`predict` API. The default choice before reaching for deep
> learning.

---

## install

```bash
pip install scikit-learn
```

---

## train/test split and a regression model

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[0], [1], [2], [3], [4]]) # feature: hour
y = np.array([18.2, 23.4, 31.1, 19.8, 25.0]) # target: temperature

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
print(model.predict(X_test))
```

Every scikit-learn estimator follows the same shape: `fit(X, y)` to
train, `predict(X)` to use it — swapping models means changing one line.

---

## classification

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train_labels)

predictions = model.predict(X_test)
print(accuracy_score(y_test_labels, predictions))
```

---

## preprocessing with a pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression()),
])
pipe.fit(X_train, y_train_labels)
print(pipe.score(X_test, y_test_labels))
```

A `Pipeline` bundles preprocessing and the model together — fitting
scales the training data and fits the model in one call, and prevents
accidentally leaking test-set statistics into training.

---

## clustering (unsupervised)

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)
print(labels)
```

---

## error handling basics

```python
from sklearn.linear_model import LinearRegression
import numpy as np

model = LinearRegression()
try:
    model.fit(np.array([[1, 2], [3, 4]]), np.array([1, 2, 3])) # mismatched lengths
except ValueError as e:
    print("shape mismatch:", e)
```

Also watch for calling `.predict()` before `.fit()` — raises
`NotFittedError`, a clear signal the model was never trained.

---

## snippets box

```python
# cross-validation instead of a single split
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5)
print(scores.mean())
```

```python
# save/load a trained model
import joblib
joblib.dump(model, "model.joblib")
model = joblib.load("model.joblib")
```

!!! warning "Load only trusted artifacts"
    `joblib.load()` can execute code while deserializing. Load model files only
    from a trusted source, and verify their package versions and provenance.

---

## when to use what

| Need | Package |
|---|---|
| Classic ML: regression, trees, clustering | `scikit-learn` |
| Deep learning, custom neural nets | `torch` |
| Just numeric arrays, no ML | `numpy` |

Next door: swap `LinearRegression` for `torch` once the problem needs a
neural network instead of a classic model.
