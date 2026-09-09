# responses — mock HTTP calls

> responses intercepts requests made by the `requests` library so unit tests do not call real services.

## Install and mock

```bash
python -m pip install requests responses pytest
```

```python
import responses
import requests

@responses.activate
def test_status() -> None:
    responses.get("https://api.example.com/status", json={"ok": True}, status=200)
    response = requests.get("https://api.example.com/status", timeout=5)
    assert response.json() == {"ok": True}
```

Register exact URLs and assert that calls occurred. Keep a small number of integration tests against a controlled service because mocks cannot prove that the remote API still behaves as expected.

Next door: [requests](requests.md).
