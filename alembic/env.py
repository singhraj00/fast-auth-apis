from sqlalchemy import create_engine, pool
from alembic import context
from app.db import Base
from app import models
from app.settings import settings

config = context.config

# Sync engine sirf Alembic ke liye
DATABASE_URL_SYNC = settings.DATABASE_URL.replace("+asyncpg", "")  # +asyncpg remove karo
connectable = create_engine(DATABASE_URL_SYNC, poolclass=pool.NullPool)

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=DATABASE_URL_SYNC,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
