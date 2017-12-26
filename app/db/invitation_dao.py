from .dao import Dao
from .model import Meeting, User


class InvitationDao(Dao):

    def get(self, user):
        self.cursor.execute('''SELECT * FROM TABLE(ilya_package.get_invitations(:email))''', {
            "email": user.email,
        })
        data = self.cursor.fetchall()
        meetings = [Meeting(
                    id=record[0],
                    title=record[1],
                    address=record[2],
                    date=record[3],
                    desc=None,
                    user=User(record[5], record[4]),
                    invited=None,
                ) for record in data]

        return meetings
        '''
        id "Meeting"."id"%TYPE,
          title "Meeting"."title"%TYPE,
          address "Meeting"."address"%TYPE,
          a_date "Meeting"."date"%TYPE,
          email "Invitation"."email"%TYPE,
          name "User"."name"%TYPE
        '''

    def accept(self, id, user: User):
        self.cursor.callproc(
            'ilya_package.accept_invitation',
            [id, user.email]
        )

    def discard(self, id, user: User):
        self.cursor.callproc(
            'ilya_package.discard_invitation',
            [id, user.email]
        )