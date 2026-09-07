# Useful Python Packages — Hub

> Curated catalog of high-value third-party packages, grouped by job.
> Each category below will get its own tutorial page with copy-paste snippets.

> All names verified live on PyPI.

---

## SCADA, PLC & Industrial Protocols

| Package | PyPI name | What it does |
|---|---|---|
| Modbus TCP/RTU | `pymodbus` | Client/server Modbus — reads/writes coils and registers over TCP (for example, port 502), RTU, or ASCII |
| Modbus (simple) | `minimalmodbus` | Tiny serial-only Modbus RTU for instruments, sensors |
| Modbus toolkit | `modbus-tk` | Generic Modbus fieldbus toolkit — TCP, RTU, easier framing |
| Modbus TCP | `pyModbusTCP` | Minimal Modbus TCP client, zero or few deps |
| Modbus RTU | `umodbus` | Lightweight Modbus RTU/TCP (some forks maintain) |
| OPC UA | `asyncua` | Open Platform Communications UA — async client/server for modern PLCs |
| OPC UA (legacy) | `opcua` | Older synchronous OPC-UA client/server |
| SNMP | `pysnmp` | SNMP v1/v2c/v3 — read network gear stats (switches, routers) |
| SNMP (lextudio fork) | `pysnmp-lextudio` | Maintained SNMP fork, async aware |
| MQTT | `paho-mqtt` | Industrial pub/sub messaging — talk to brokers (Mosquitto, HiveMQ, cloud IoT) |
| MQTT (async) | `aiomqtt` | Asyncio-native MQTT 5 client for event loops |
| S7 (Siemens PLC) | `python-snap7` | Direct S7 protocol access to Siemens S7-1200/1500/300/400 |
| TwinCAT (Beckhoff) | `pyads` | ADS protocol for Beckhoff TwinCAT — real-time PLC data |
| CAN bus | `python-can` | CAN networking — read/write frames over USB/PCAN/SocketCAN |
| Serial ports | `pyserial` | Cross-platform serial port I/O — RS-232/485 for sensors, meters |

> Tip: For a SCADA system (any vendor), first identify the wire protocol — Modbus TCP/serial, OPC UA, SNMP, MQTT, CAN, S7, or ADS — and pick the matching row. Most SCADA gateways expose Modbus TCP or OPC UA as convenience interfaces.

---

## Databases

| Package | PyPI name | What it does |
|---|---|---|
| SQLite (builtin) | (stdlib `sqlite3`) | Embedded SQL database — zero setup, ships with Python |
| PostgreSQL | `psycopg2-binary` | Battle-tested PostgreSQL adapter (binary wheels) |
| PostgreSQL (modern) | `psycopg` | New-gen Psycopg 3, async support |
| MySQL | `pymysql` | Pure-Python MySQL client |
| MongoDB | `pymongo` | Official MongoDB driver — docs, aggregations, gridfs |
| Redis | `redis` | In-memory key-value store client — caching, queues, pub/sub |
| InfluxDB | `influxdb-client` | Time-series DB client — well suited for industrial telemetry logging |
| SQLite async | `aiosqlite` | Async wrapper around sqlite3 for asyncio apps |

---

## HTTP, APIs & Web Scraping

| Package | PyPI name | What it does |
|---|---|---|
| HTTP client (simple) | `requests` | The de-facto HTTP client — REST APIs, tokens, files |
| HTTP client (async) | `httpx` | Async + sync HTTP, HTTP/2, drop-in requests-like |
| HTTP client (low-level) | `urllib3` | Low-level HTTP connection pooling; Requests uses it, while HTTPX uses httpcore |
| Async HTTP | `aiohttp` | Asyncio HTTP client/server — web scraping at scale |
| HTML parsing | `beautifulsoup4` | Parse messy HTML — find tags, tables, links |
| Fast HTML/XML | `lxml` | C-speed HTML/XML processing — pairs with bs4 |
| WebSocket | `websockets` | RFC6455 client/server for asyncio — live dashboards, push |
| GraphQL | `gql` | GraphQL client for Python — query modern APIs |

---

## Data Science, Numerics & Charts

| Package | PyPI name | What it does |
|---|---|---|
| Arrays | `numpy` | N-dimensional arrays + linear algebra — foundation of everything |
| Tables | `pandas` | DataFrames — munge time series, compute stats, resample |
| Plotting | `matplotlib` | Publication-quality static plots, thisicals, charts |
| Interactive charts | `plotly` | Interactive web charts — zoom, hover, export |
| Dashboards | `dash` | Web dashboards purely in Python (Plotly-backed) |
| Quick dashboards | `streamlit` | Bare-bones data apps with scripts — fastest ROI |
| Notebooks | `jupyterlab` | Interactive notebooks for exploration and teaching |
| Excel read/write | `openpyxl` | Read/write .xlsx without Excel installed |
| Excel writer | `xlsxwriter` | High-performance .xlsx writer with formatting |
| Scientific | `scipy` | Optimization, stats, signal processing on numpy |
| Symbolic | `sympy` | Symbolic math — algebra, calculus, solvers |
| Machine learning | `scikit-learn` | Classic ML — regressions, trees, clustering |
| Deep learning | `torch` | PyTorch — tensors, autograd, neural nets |
| Serialization | `pyarrow` | Apache Arrow/Parquet — fast columnar exchange |

---

## CLI, Config & Automation

| Package | PyPI name | What it does |
|---|---|---|
| CLI framework | `click` | Compose command-line tools from functions |
| CLI framework (modern) | `typer` | Type-hint driven CLI — builds on click |
| Progress bars | `tqdm` | Instant progress bars over loops — must-have |
| Pretty output | `rich` | Colorized tables, logs, syntax-highlighted terminal |
| Logging | `structlog` | Structured JSON logs for services — greppable at scale |
| Config YAML | `pyyaml` | Load/save YAML config files |
| Config env vars | `python-dotenv` | Load .env files into environment — keep secrets out of code |
| Validation | `pydantic` | Typed, validated settings and data models — pairs with FastAPI |
| Scheduling | `schedule` | Human-readable periodic jobs (every 10 minutes) |
| Cron expressions | `croniter` | Parse/expand cron strings for custom schedulers |
| Date handling | `python-dateutil` | Robust date parsing, timezones, relativedelta |
| Date handling (modern) | `pendulum` | Drop-in datetime replacement with easy timezone math |
| Date handling (arrows) | `arrow` | Fluent human-friendly datetimes |

---

## Web Frameworks & APIs

| Package | PyPI name | What it does |
|---|---|---|
| Fast API | `fastapi` | Modern async REST APIs with OpenAPI docs auto-generated |
| ASGI server | `uvicorn` | Fast ASGI server — serves FastAPI/Starlette |
| Micro web | `flask` | Lightweight classic web app framework |
| Full stack | `django` | Batteries-included framework — ORM, admin, auth |
| ASGI framework | `starlette` | Lightweight ASGI toolkit under FastAPI |
| Templating | `jinja2` | Server-side HTML templating for Flask/Django/static sites |
| ORM | `sqlalchemy` | SQL toolkit + ORM — talk to many DBs same API |
| Migrations | `alembic` | SQLAlchemy migration manager — version your schema |
| Telemetry | `opentelemetry-api` | Vendor-neutral tracing/metrics/logging for services |

---

## Testing & Dev Tools

| Package | PyPI name | What it does |
|---|---|---|
| Test runner | `pytest` | The standard test framework — fixtures, parametrize |
| Coverage | `pytest-cov` | Coverage reports — see untested lines |
| Fake data | `faker` | Generate realistic fake names, addresses, serials for tests |
| Mock server | `responses` | Stub HTTP calls when unit-testing requests/httpx |
| Linter | `ruff` | Ultra-fast Python linter + formatter (replaces flake8/black) |
| Type checker | `mypy` | Static type checking against your hints |
| Formatting | `black` | Opinionated code formatter — zero-config style |
| Sorting imports | `isort` | Sorts imports automatically |
| Pre-commit | `pre-commit` | Git hooks running lint/format/tests before every commit |
| Package build | `build` | Standard PEP 517 sdist/wheel builder |
| Dist tool | `hatchling` | Modern backend for pyproject-style packaging |

---

## Next steps

Each table row will bloom into a dedicated tutorial page under this section.
Pick a row you use at work (the SCADA/Modbus/OPC UA rows are prime candidates),
and we will go deep: install, connect, read/write data, handle errors, real snippet.