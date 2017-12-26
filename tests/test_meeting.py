import cx_Oracle

from tests.fixtures.db_fixtures import connection, cursor, db_data
from tests.fixtures.create_db import create_db
from cx_Oracle import DatabaseError
import pytest

@pytest.fixture(params=('title', 'address', 'email'))
def create_meeting(cursor, title, address, email):
    cursor.execute('''insert into "User" ("email", "name") values (:email, 'Name')''', email=email)
    cursor.execute('''INSERT INTO "Meeting" ("title", "address", "email", "date")
                                  VALUES (:title, :address, :email, TO_DATE('2018-11-11 18:45:38', 'YYYY-MM-DD HH24:MI:SS'))''',
                   title=title, address=address, email=email)


@pytest.fixture(params=['new_meeting'])
def update_meeting(cursor, new_meeting):
    query = '''update "Meeting" set '''
    query += ', '.join(['"{}"=\'{}\''.format(k, v) for k, v in new_meeting.items()])
    cursor.execute(query)


def test_create_meeting_no_user(cursor):
    with pytest.raises(DatabaseError):
        cursor.execute('''INSERT INTO "Meeting" ("title", "address", "email")
                          VALUES ('wer', 'ewr', 'qwe.qwe@qwe')''')


@pytest.mark.parametrize(
    'title, address, email', [
        ('Title', 'Address', 'qwe@qwe.qwe'),
        ('Another title', 'Another address', 'qwyleqwyle@gmail.com')
    ],
)
def test_create_meeting(cursor, create_meeting):
    pass


@pytest.mark.parametrize(
    'title, address, email', [
        ('I'*257, 'Address', 'qwe@qwe.qwe'),
        ('Title', 'I'*257, 'qwyleqwyle@gmail.com')
    ],
)
def test_create_meeting_raises(cursor, title, address, email):
    with pytest.raises(DatabaseError):
        create_meeting(cursor, title, address, email)


@pytest.mark.parametrize(
    'title, address, email', [
        ('Title', 'Address', 'qwe@qwe.qwe'),
    ]
)
@pytest.mark.parametrize(
    'new_meeting', [{
            'title': 'New Title',
        }, {
            'address': 'New Address',
        },
    ]
)
def test_update_meeting(cursor, create_meeting, update_meeting):
    pass


@pytest.mark.parametrize(
    'title, address, email', [
        ('Title', 'Address', 'qwe@qwe.qwe'),
    ]
)
@pytest.mark.parametrize(
    'new_meeting', [{
            'id': 1,
        }, {
            'email': 'asd@asd.asd',
        }
    ]
)
def test_update_meeting_fail(cursor, title, address, email, new_meeting):
    with pytest.raises(DatabaseError):
        create_meeting(cursor, title, address, email)
        update_meeting(cursor, new_meeting)

