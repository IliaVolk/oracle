from tests.fixtures.create_db import create_db
from tests.fixtures.db_fixtures import connection, cursor, db_data

def test_create(cursor):
    cursor.execute('''insert into "User" ("email") VALUES ('qwe@asd.zxc')''')