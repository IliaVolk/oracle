import datetime
import cx_Oracle

from tests.fixtures.db_fixtures import connection, cursor
from tests.fixtures.create_db import create_db

def create_meeting_via_proc(cursor, title, address,
                            email,
                            a_date=datetime.datetime.now()+datetime.timedelta(3),
                            invited=[]):
    emails = cursor.arrayvar(cx_Oracle.STRING, invited)

    cursor.callproc('ilya_package.create_meeting',
                    [title, address, a_date, email, emails, 'desc'],
                    )


def create_user(cursor, email):
    cursor.execute('insert into "User" ("email", "name") VALUES (:email, :name)', {
        'email': email,
        'name': 'username'
    })


def test_create_meeting_proc(cursor):
    '''
    PROCEDURE create_meeting(
      title "Meeting"."title"%TYPE,
      address "Meeting"."address"%TYPE,
      a_date "Meeting"."date"%TYPE,
      email "Meeting"."email"%TYPE,
      invited STRING_LIST,
      description "Meeting"."description"%TYPE
   );
    '''
    title = 'title1'
    address = 'address1'
    email = 'qwerty@asdf.com'
    a_date = datetime.datetime.now()+datetime.timedelta(3)
    invited_emails = ['qwe@qwe.qwe', 'asd@zxc.cvb']


    create_user(cursor, email)
    create_meeting_via_proc(cursor, title, address, email, a_date, invited_emails)
    all_emails = [*invited_emails, email]
    cursor.execute('select "name", "email" from "User"')
    users = cursor.fetchall()
    assert len(users) == len(all_emails)
    assert users[0][0] == 'username'
    assert users[0][1] == email
    for user in users[1:]:
        assert user[0] == 'not confirmed'
        assert user[1] in invited_emails
    cursor.execute('select "title", "address",'
                   '"date", "email", "id" from "Meeting"')

    _title, _address, _date, _email, _id = cursor.fetchall()[0]
    assert _title == title
    assert _address == address
    assert email == _email
    cursor.execute('select "id", "email", "status" from "Invitation"')
    invitations = cursor.fetchall()
    assert len(invitations) == len(invited_emails)
    for inv in invitations:
        assert inv[0] == _id
        assert inv[1] in invited_emails
        assert inv[1] != email
        assert inv[2] == 'pending'


def test_autocomplete_emails(cursor):
    '''
    FUNCTION autocomplete_emails(
      owner_email "User"."email"%TYPE,
      pattern VARCHAR2
   ) RETURN EMAIL_LIST PIPELINED;
    '''
    email1 = 'qwe@qwe.qwe'
    email_inv = 'asd@zxc.cvb'
    create_user(cursor, email1)
    create_meeting_via_proc(
        cursor,
        'title1',
        'address1',
        email1,
        invited=[email_inv],
    )
    email_inv2 = 'asd@sds.sdfc'
    create_meeting_via_proc(
        cursor,
        'title2',
        'address2',
        email1,
        invited=[email_inv2, email_inv]
    )
    cursor.execute('select * from table("ilya_package"."AUTOCOMPLETE_EMAILS"(:email, :pattern))', {
        "email": email1,
        "pattern": ''
    })
    data = cursor.fetchall()
    emails = [x[0] for x in data]

    assert email_inv in emails
    assert email_inv2 in emails
    assert email1 not in emails

