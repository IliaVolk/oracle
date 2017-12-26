from tests.fixtures.db_fixtures import connection, cursor, db_data
from tests.fixtures.create_db import create_db
from cx_Oracle import DatabaseError
import pytest


def test_can_connect(connection):
    assert isinstance(connection.version, str) == True
    assert len(connection.version) > 0


@pytest.mark.parametrize(
    'name,email', [
        ('Valid', 'qwe@qwe.qwe'),
        ('Sergei', 'qwyleqwyle@gmail.com'),
        ('I'*32, 'qwe@qwe.qwe')
    ]
)
def test_create_user_success(name, email, cursor):
    cursor.execute('''INSERT INTO "User" ("email", "name") 
                              VALUES (:email, :name)''', email=email, name=name)
    cursor.execute('select "name", "email" from "User"')
    _name, _email = cursor.fetchall()[0]
    assert name == _name
    assert email == _email


@pytest.mark.parametrize(
    'name,email', [
        ('valid', 'asd'),
        ('I', 'qwe@qwe.qwe'),
        ('I'*33, 'qwe@qwe.qwe')
    ],
)
def test_create_user_constraints_violation(name, email, cursor):
    with pytest.raises(DatabaseError):
        cursor.execute('''INSERT INTO "User" ("email", "name") 
                          VALUES (:email, :name)''', email=email, name=name)

