# 45 — MongoDB with PyMongo

> `PyMongo` is the official MongoDB driver — document CRUD, aggregation
> pipelines, GridFS for large binary files, all against MongoDB's
> flexible schema-less collections.

---

## install

```bash
pip install pymongo
```

---

## connect and insert a document

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["app"]
readings = db["readings"]

result = readings.insert_one({"value": 23.4, "sensor": "line1"})
print(result.inserted_id)
```

Documents are plain dicts — no schema migration step, though you should
still agree on a shape as a team.

---

## query documents

```python
for doc in readings.find({"value": {"$gt": 20}}):
    print(doc)

one = readings.find_one({"sensor": "line1"})
```

`find` returns a lazy cursor — iterate it or call `list(..)` to
materialize; don't call it repeatedly expecting cached results.

---

## update and delete

```python
readings.update_one({"sensor": "line1"}, {"$set": {"value": 25.0}})
readings.update_many({"sensor": "line1"}, {"$inc": {"value": 1}})
readings.delete_one({"sensor": "line1"})
```

---

## aggregation pipeline

```python
pipeline = [
    {"$match": {"sensor": "line1"}},
    {"$group": {"_id": "$sensor", "avg_value": {"$avg": "$value"}}},
]
for doc in readings.aggregate(pipeline):
    print(doc)
```

---

## error handling basics

```python
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

try:
    readings.insert_one({"_id": "line1", "value": 23.4})
    readings.insert_one({"_id": "line1", "value": 25.0}) # duplicate _id
except DuplicateKeyError as e:
    print("duplicate key:", e)
except ServerSelectionTimeoutError as e:
    print("could not reach MongoDB:", e)
```

---

## snippets box

```python
# create an index for faster queries/uniqueness
readings.create_index("sensor")
readings.create_index("sensor", unique=True)
```

```python
# bulk insert
readings.insert_many([{"value": 1.1}, {"value": 2.2}, {"value": 3.3}])
```

---

## when to use what

| Need | Package |
|---|---|
| Document store, flexible schema | `pymongo` |
| Relational data with strong schema | `psycopg` / `pymysql` |
| Time-series specifically | `influxdb-client` |

Next door: model documents with `pydantic` for validation before
inserting.
