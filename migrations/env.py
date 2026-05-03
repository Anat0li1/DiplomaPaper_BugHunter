from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import os

# Alembic Config object with access to values from alembic.ini.
config = context.config

# Configure Python logging from alembic.ini when the file is present.
if config.config_file_name and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)

# Model metadata used by Alembic autogenerate.
from models import db
from app import app
target_metadata = db.metadata

def get_url():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/quality_portal')


def run_migrations_offline() -> None:
    """Run migrations without opening a database connection."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live database connection."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

