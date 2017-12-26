from .dao import Dao
from .model import User


class UserDao(Dao):
    def create(self, user: User):
        self.cursor.callproc(
            'ilya_package.create_user',
            [user.email, user.name]
        )

    def get(self, email: str):
        self.cursor.execute('select * from TABLE(ilya_package.get_user(:email))', {
            "email": email
        })
        data = self.cursor.fetchall()
        if len(data):
            return User(data[0][1], data[0][0])

    def get_autocomplete(self, user):
        self.cursor.execute('select * from TABLE(ilya_package.autocomplete_emails(:email))', {
            "email": user.email,
        })
        data = self.cursor.fetchall()
        users = [User(email=rec[0]) for rec in data]
        return users
