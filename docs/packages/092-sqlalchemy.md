# SQLAlchemy — SQL toolkit and ORM

> SQLAlchemy provides explicit SQL Core APIs and an ORM for mapping Python objects to relational data.

## Install and connect

```bash
python -m pip install sqlalchemy
```

```python
import os
from sqlalchemy import create_engine, text

engine = create_engine(os.environ["DATABASE_URL"])
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar_one())
```

Use `text()` parameters rather than string interpolation for values. Keep the database URL in the environment and configure pooling, TLS, and timeouts for the target database.

## ORM model

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Reading(Base):
    __tablename__ = "readings"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float]
```

Use migrations rather than creating production schemas implicitly at application startup. Transactions should be short and explicit around units of work.

Next door: [Alembic](093-alembic.md) for schema migrations.
