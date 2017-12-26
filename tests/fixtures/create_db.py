import pytest
import os


def execute_no_errors(q, cursor):
    queries = q.split(';')
    for query in queries:
        if query.strip():
            try:
                cursor.execute(query)
            except Exception as e:
                pass


def execute(q, cursor):
    queries = q.split(';')
    for query in queries:
        if query.strip():
            cursor.execute(query)


@pytest.yield_fixture(autouse=True)
def create_db(cursor):
    with open('db/create_db.sql') as create_db:
        create_db_query = create_db.read()
    with open('db/drop_db.sql') as drop_db:
        drop_db_query = drop_db.read()
    execute_no_errors(drop_db_query, cursor)
    execute(create_db_query, cursor)
    triggers_path = os.path.join('db', 'triggers')
    with open('db/package.sql') as package:
        cursor.execute(package.read())
    with open('db/package_body.sql') as package:
        cursor.execute(package.read())
    for file in os.listdir(triggers_path):
        with open(os.path.join(triggers_path, file)) as trigger:
            cursor.execute(trigger.read())

    yield
    # execute(drop_db_query, cursor)

