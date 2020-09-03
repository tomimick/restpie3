# 002_movies.py

def migrate(migrator, database, fake=False, **kwargs):

    migrator.sql("""CREATE TABLE movies(
        id INTEGER PRIMARY KEY,

        created timestamp not null default CURRENT_TIMESTAMP,
        modified timestamp not null default CURRENT_TIMESTAMP,

        creator integer REFERENCES users(id),

        title text,
        director text
    )""")

def rollback(migrator, database, fake=False, **kwargs):

    migrator.sql("""DROP TABLE movies""")

