# Alembic — database migrations

> Alembic versions schema changes for SQLAlchemy applications and lets deployments move databases forward or backward deliberately.

## Install and initialize

```bash
python -m pip install alembic sqlalchemy
alembic init migrations
```

Configure the database URL through environment variables rather than committing credentials. Create a revision with `alembic revision -m "add readings"`, edit its `upgrade()` and `downgrade()` functions, then apply it with `alembic upgrade head`.

## Migration shape

```python
def upgrade() -> None:
    op.add_column("readings", sa.Column("quality", sa.Integer(), nullable=True))

def downgrade() -> None:
    op.drop_column("readings", "quality")
```

Test migrations against a disposable database and review destructive operations separately. A downgrade is not always lossless after data has been written.

Next door: [SQLAlchemy](sqlalchemy.md).
