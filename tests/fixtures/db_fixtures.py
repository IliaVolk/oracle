import pytest

from app.config import username, password, ip, port, proto
import cx_Oracle
from app.db.model import User


@pytest.yield_fixture()
def cursor(connection):
    connection.begin()
    yield connection.cursor()
    connection.commit()


@pytest.yield_fixture(scope='module')
def connection():
    with cx_Oracle.connect(
            username,
            password,
            '{}:{}/{}'.format(
                ip,
                port,
                proto,
            )) as conn:
        yield conn


@pytest.fixture()
def user(cursor, connection):
    email = 'qwe@asd.zxc'
    cursor.execute('''INSERT INTO "User" ("email") VALUES (:email)''', {
        "email": email,
    })
    connection.commit()
    return User('', email)
