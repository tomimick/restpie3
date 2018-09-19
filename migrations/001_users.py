"""Peewee migrations -- 001_create.py.

    Some examples:

    > Model = migrator.orm['model_name'] # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
"""

def migrate(migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    # create extension manually - you must be a superuser to do this
    # is needed by uuid_generate_v4()

#     migrator.sql("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")


    migrator.sql("""CREATE TYPE type_user_role AS ENUM (
        'disabled',
        'readonly',
        'editor',
        'admin',
        'superuser')
    """)


    migrator.sql("""CREATE TABLE users (

        id uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),

        created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        modified timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

        email text UNIQUE,
        password text,
        first_name text,
        last_name text,
        role type_user_role DEFAULT 'readonly',
        tags text[]
    )""")
    # normal integer-id: id serial PRIMARY KEY NOT NULL,


def rollback(migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

