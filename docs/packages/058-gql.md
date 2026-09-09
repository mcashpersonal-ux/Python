# 56 — GraphQL client with gql

> `gql` queries GraphQL APIs from Python — building queries, sending them
> over HTTP or WebSocket transports, and optionally validating against a
> schema fetched via introspection.

---

## install

```bash
pip install gql[aiohttp]
```

The transport is a separate extra — `[aiohttp]` here, or `[requests]`,
`[websockets]` depending on how you want to connect.

---

## run a query (sync, requests transport)

```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

transport = RequestsHTTPTransport(url="https://api.example.com/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

query = gql("""
    query GetReadings($sensor: String!) {
        readings(sensor: $sensor) {
            id
            value
        }
    }
""")

result = client.execute(query, variable_values={"sensor": "line1"})
print(result)
```

`fetch_schema_from_transport=True` downloads the schema via introspection
so `gql` can validate your query client-side before sending it.

---

## async query

```python
import asyncio
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

async def main():
    transport = AIOHTTPTransport(url="https://api.example.com/graphql")
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        result = await session.execute(gql("{ readings { id value } }"))
        print(result)

asyncio.run(main())
```

---

## mutations

```python
mutation = gql("""
    mutation AddReading($sensor: String!, $value: Float!) {
        addReading(sensor: $sensor, value: $value) {
            id
        }
    }
""")
result = client.execute(mutation, variable_values={"sensor": "line1", "value": 23.4})
```

---

## subscriptions (WebSocket transport)

```python
async def subscribe():
    from gql.transport.websockets import WebsocketsTransport

    transport = WebsocketsTransport(url="wss://api.example.com/graphql")
    async with Client(transport=transport) as session:
        subscription = gql("subscription { readingAdded { id value } }")
        async for result in session.subscribe(subscription):
            print(result)
```

---

## error handling basics

```python
from gql.transport.exceptions import TransportQueryError, TransportServerError

try:
    result = client.execute(query, variable_values={"sensor": "line1"})
except TransportQueryError as e:
    print("GraphQL error:", e.errors)
except TransportServerError as e:
    print("server/transport error:", e)
```

---

## snippets box

```python
# add auth headers
transport = RequestsHTTPTransport(
    url="https://api.example.com/graphql", headers={"Authorization": "Bearer TOKEN"}
)
```

---

## when to use what

| Need | Package |
|---|---|
| GraphQL APIs specifically | `gql` |
| REST APIs | `requests` / `httpx` |
| Building your own GraphQL server | (not covered here — see FastAPI + Strawberry) |

Next door: validate responses with `pydantic` models matching the schema
types.
