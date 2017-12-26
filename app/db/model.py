from dateutil.parser import parse


class User:
    def __init__(self, name=None, email=None):
        self.email = email
        self.name = name

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.email == other.email


class Meeting:
    def __init__(self, user=None, title=None, address=None,
                 date=None, invited=None, desc=None, id=None):
        if isinstance(user, str):
            user = User('', user)
        self.user = user
        self.title = title
        self.address = address
        if date and isinstance(date, str):
            self.date = parse(date)
        else:
            self.date = date
        self.invited = invited
        self.desc = desc if desc else ''
        self.id = id

    def __repr__(self):
        return str(self.__dict__)


class Invitation:
    def __init__(self, user=None, status=None, id=None):
        self.user = user
        self.status = status
        self.id = id

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.user == other.user and self.id == other.id
