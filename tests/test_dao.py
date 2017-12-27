from app.db.model import Meeting, User, Invitation
from app.db.meeting_dao import MeetingDao
from app.db.user_dao import UserDao
from tests.fixtures.db_fixtures import connection, cursor, user
from tests.fixtures.create_db import create_db
from app.db.invitation_dao import InvitationDao
import datetime


def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microsecond)


def test_meeting_delete(user):
    meetings = [Meeting(
        user,
        'title{}'.format(i),
        'address{}'.format(i),
        chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        [],
        'desc{}'.format(i),
    ) for i in range(2)]
    with MeetingDao() as dao:
        for m in meetings:
            dao.create(m)
        created = dao.get(user)
        assert len(created) == 2
        dao.delete(created[0].id)
        after_delete = dao.get(user)
        assert len(after_delete) == 1
        assert after_delete[0].id == created[1].id


def test_accept_discard_invitation(user):
    inv1 = Invitation(user=User(email='qqq@qqq.qqq'))
    inv2 = Invitation(user=User(email='www@www.www'))
    with MeetingDao() as dao:
        dao.create(Meeting(
            user=user,
            title='title1',
            address='address1',
            invited=[inv1, inv2],
            date=chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        ))
        meeting = dao.get(user)[0]
    assert len(meeting.invited) == 2
    assert meeting.invited[0].status == 'pending'
    assert meeting.invited[1].status == 'pending'
    with InvitationDao() as dao:
        dao.accept(meeting.id, inv1.user)
    with MeetingDao() as dao:
        meeting = dao.get_single(meeting.id)
    assert len(meeting.invited) == 2
    assert [inv.status for inv in meeting.invited if inv == inv1][0] == 'accept'
    assert [inv.status for inv in meeting.invited if inv == inv2][0] == 'pending'

    with InvitationDao() as dao:
        dao.discard(meeting.id, inv1.user)
    with MeetingDao() as dao:
        meeting = dao.get_single(meeting.id)
    assert len(meeting.invited) == 2
    assert meeting.invited[0].status == 'pending'
    assert meeting.invited[1].status == 'pending'


def test_autocomplete_emails(user):
    inv1 = Invitation(user=User(email='qqq@qqq.qqq'))
    inv2 = Invitation(user=User(email='www@www.www'))
    with MeetingDao() as dao:
        dao.create(Meeting(
            user=user,
            title='title1',
            address='address1',
            invited=[inv1],
            date=chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        ))
        dao.create(Meeting(
            user=user,
            title='title1',
            address='address2',
            invited=[inv1, inv2],
            date=chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        ))
    with UserDao() as dao:
        users = dao.get_autocomplete(user)

    assert inv1.user in users
    assert inv2.user in users
    assert user not in users


def test_user_should_not_see_meeting_until_accept(user):
    user2 = User(email='qqq@qqq.qqq')
    with UserDao() as dao:
        dao.create(user2)
    meeting = Meeting(
        user,
        'title',
        'address',
        chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        [Invitation(user=user2)],
        'desc',
    )
    with MeetingDao() as dao:
        dao.create(meeting)
        m1 = dao.get(user)
        m2 = dao.get(user2)
    with InvitationDao() as dao:
        i1 = dao.get(user)
        i2 = dao.get(user2)
    assert len(m1) == 1
    assert len(m1[0].invited) == 1
    meeting = m1[0]
    assert len(m2) == 0
    assert len(i1) == 0
    assert len(i2) == 1

    with InvitationDao() as dao:
        dao.accept(meeting.id, user2)
    with MeetingDao() as dao:
        m1 = dao.get(user)
        m2 = dao.get(user2)
    with InvitationDao() as dao:
        i1 = dao.get(user)
        i2 = dao.get(user2)
    assert len(m1) == 1
    assert len(m2) == 1
    assert len(i1) == 0
    assert len(i2) == 0


def test_get_meetings(user):
    meetings = [Meeting(
        user,
        'title{}'.format(i),
        'address{}'.format(i),
        chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        [Invitation(user=User(email='qqq@qqq.qqq'))],
        'desc{}'.format(i),
    ) for i in range(10)]
    for m in meetings:
        with MeetingDao() as dao:
            dao.create(m)
    meetings.reverse()
    with MeetingDao() as dao:
        result = dao.get(user)
    assert len(result) == 10
    for i, m in enumerate(result):
        m2 = [m2 for m2 in meetings if m2.title == m.title][0]
        assert m.address == m2.address
        assert m.date == m2.date
        assert m.desc == m2.desc
        assert m.user == user
        assert len(m.invited) == 1 == len(m2.invited)


def test_update_meeting(user):
    invited_before = [
        Invitation(user=User('', 'qqq@qqq.qqq')),
        Invitation(user=User('', 'www@www.www')),
    ]
    meeting = Meeting(
        user,
        'title',
        'address',
        chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        invited_before,
        'desc',
    )
    with MeetingDao() as dao:
        dao.create(meeting)
        id = dao.get(user)[0].id
        for inv in meeting.invited:
            with InvitationDao() as dao:
                dao.accept(id, inv.user)
    with MeetingDao() as dao:
        meeting = dao.get(user)[0]
    meeting.title = 'edited title'
    meeting.address = 'edited address'
    meeting.desc = 'edited desc'
    meeting.invited = [
        invited_before[0],
        Invitation(user=User('', 'zzz@zzz.zzz')),
    ]
    with MeetingDao() as dao:
        dao.update(meeting)
        with InvitationDao() as dao:
            dao.accept(meeting.id, meeting.invited[1].user)

    with MeetingDao() as dao:
        updated = dao.get_single(meeting.id)

    assert updated.id == meeting.id
    assert updated.desc == meeting.desc
    assert updated.date == meeting.date
    assert updated.title == meeting.title
    assert updated.address == meeting.address
    for inv in meeting.invited:
        assert inv in updated.invited

    for inv in updated.invited:
        assert inv in meeting.invited


def test_create_meeting(user):
    meeting = Meeting(
        user,
        'title',
        'address',
        chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        [Invitation(user=User('', email)) for email in ['qqq@qqq.qqq', 'www@www.www']],
        'desc',
    )
    with MeetingDao() as dao:
        dao.create(meeting)

    with MeetingDao() as dao:
        created = dao.get(user)[0]
    for inv in meeting.invited:
        with InvitationDao() as dao:
            dao.accept(created.id, inv.user)
    with MeetingDao() as dao:
        created = dao.get(user)[0]
    assert created.title == meeting.title
    assert created.address == meeting.address
    assert created.date == meeting.date
    for u in meeting.invited:
        assert u in created.invited
    for u in created.invited:
        assert u in meeting.invited
    assert created.desc == meeting.desc


def test_get_invitations(user):
    email = 'qqq@qqq.qqq'
    meetings = [Meeting(
        user,
        'title{}'.format(i),
        'address',
        chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
        [Invitation(user=User('', email)),
         Invitation(user=User('', 'www@www.www'))],
        'desc',
    ) for i in range(3)]
    meetings[0].invited = []
    for m in meetings:
        with MeetingDao() as dao:
            dao.create(m)
    meetings = meetings[1:]
    with InvitationDao() as dao:
        found = dao.get(User(email=email))
    for meeting in meetings:
        inv = [m for m in found if m.title == meeting.title][0]
        assert inv.date == meeting.date
        assert inv.user == user
        assert inv.invited is None


def test_create_user():
    users = [User('name{}'.format(i), 'qqq{}@qqq.qqq'.format(i)) for i in range(5)]
    for user in users:
        with UserDao() as dao:
            dao.create(user)

    for user in users:
        with UserDao() as dao:
            found = dao.get(user.email)
            assert found.name == user.name


def test_single_meeting(user, cursor):
    meeting = Meeting(
            user,
            'title',
            'address',
            chop_microseconds(datetime.datetime.now() + datetime.timedelta(3)),
            [Invitation(user=User('', 'qqq@qqq.qqq')),
             Invitation(user=User('', 'www@www.www'))],
            'desc',
        )
    with MeetingDao() as dao:
        dao.create(meeting)
        id = dao.get(user)[0].id
        for inv in meeting.invited:
            with InvitationDao() as dao:
                dao.accept(id, inv.user)

    with MeetingDao() as dao:
        found = dao.get_single(id)

    assert meeting.title == found.title
    assert meeting.address == found.address
    assert meeting.date == found.date
    assert meeting.desc == found.desc
    assert len(meeting.invited) == len(found.invited) == 2
    for user in meeting.invited:
        assert user in found.invited

    for user in found.invited:
        assert user in meeting.invited


def test_single_meeting_not_found():
    with MeetingDao() as dao:
        found = dao.get_single(232)

    assert found is None



