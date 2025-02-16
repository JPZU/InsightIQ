import os
from logging.config import fileConfig
from alembic import context
from backend.database.models.base import Base
from backend.database.session import engine

# Load the Alembic configuration
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Set up logging
fileConfig(config.config_file_name)

# Bind the metadata to the engine
target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Enable type comparison
            compare_server_default=True,  # Enable server default comparison
            include_schemas=True,  # Include schema changes
            render_as_batch=True,  # Use batch mode for better compatibility
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()