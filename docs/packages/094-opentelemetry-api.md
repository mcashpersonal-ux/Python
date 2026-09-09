# OpenTelemetry API — vendor-neutral telemetry

> OpenTelemetry standardizes traces, metrics, and logs while allowing the exporter and backend to be selected separately.

## Install and create a span

```bash
python -m pip install opentelemetry-api opentelemetry-sdk
```

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("read_sensor") as span:
    span.set_attribute("sensor.name", "line1")
    value = 23.4
```

The API alone does not export data. Configure an SDK provider and exporter in the application startup path, then propagate trace context across service boundaries.

## Data hygiene

Never put passwords, tokens, full request bodies, or unnecessary personal data in span attributes. Define retention, sampling, and access policies in the telemetry backend.

Next door: [FastAPI](086-fastapi.md) for an ASGI service integration.
