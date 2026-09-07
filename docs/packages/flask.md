# Flask — small web applications

> Flask is a lightweight WSGI web framework with routing, request handling, templates, and extensions.

## Install and create an app

```bash
python -m pip install flask
```

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(debug=True)
```

`debug=True` is for local development only; never expose the debugger to an untrusted network. Use a production WSGI server and a reverse proxy when deploying.

## Request data

```python
from flask import request

@app.post("/echo")
def echo():
    payload = request.get_json(silent=False)
    return jsonify(payload)
```

Validate payloads, enforce authentication and authorization, and configure limits for body size and request time before accepting untrusted traffic.

Next door: [Jinja2](jinja2.md) for templates.
