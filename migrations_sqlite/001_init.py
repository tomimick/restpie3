# 001_init.py

def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    migrator.sql("""CREATE TABLE users (

        id INTEGER PRIMARY KEY,

        created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

        email text UNIQUE,
        password text,
        first_name text,
        last_name text,
        role text DEFAULT 'readonly',
        tags text
    )""")

def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

