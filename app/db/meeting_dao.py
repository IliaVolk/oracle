from .dao import Dao
from .model import Meeting, User, Invitation
import cx_Oracle


class MeetingDao(Dao):

    def collect_data(self, data):
        meetings = []
        for record in data:
            id = record[0]
            current_meeting = None
            for meeting in meetings:
                if meeting.id == id:
                    current_meeting = meeting
                    break
            if current_meeting is None:
                current_meeting = Meeting(
                    id=record[0],
                    title=record[2],
                    address=record[3],
                    date=record[4],
                    desc=record[5],
                    user=User(email=record[1]),
                    invited=[],
                )
                meetings.append(current_meeting)
            if record[7] is not None:
                current_meeting.invited.append(Invitation(
                    user=User(record[6], record[7]),
                    status=record[8],
                ))
        return meetings

    def get(self, user: User):
        self.cursor.execute(
            'select * from TABLE(ilya_package.get_meetings_list(:email, NULL))', {
                'email': user.email,
            })
        data = self.cursor.fetchall()

        return self.collect_data(data)

    def create(self, meeting: Meeting):
        emails = self.cursor.arrayvar(
            cx_Oracle.STRING,
            [inv.user.email for inv in meeting.invited])
        self.cursor.callproc('ilya_package.create_meeting', [
            meeting.title,
            meeting.address,
            meeting.date,
            meeting.user.email,
            emails,
            meeting.desc
        ])

    def get_single(self, id: int) -> Meeting:
        self.cursor.execute(
            'select * from TABLE(ilya_package.get_meetings_list(NULL, :id))',
            [id])
        data = self.cursor.fetchall()
        if len(data) > 0:
            return self.collect_data(data)[0]

    def update(self, meeting: Meeting):
        '''
        id "Meeting"."id"%TYPE,
        title "Meeting"."title"%TYPE,
        address "Meeting"."address"%TYPE,
        a_date "Meeting"."date"%TYPE,
        invited STRING_LIST,
        description "Meeting"."description"%TYPE
        '''
        self.cursor.callproc('ilya_package.update_meeting', [
            meeting.id,
            meeting.title,
            meeting.address,
            meeting.date,
            [inv.user.email for inv in meeting.invited],
            meeting.desc,
        ])

    def delete(self, id):
        self.cursor.callproc('ilya_package.delete_meeting', [id])



