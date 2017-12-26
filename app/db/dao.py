import cx_Oracle
from app.config import username, password, ip, port, proto


class Dao:

    def __enter__(self):
        self.conn = cx_Oracle.connect(
            username,
            password,
            '{}:{}/{}'.format(
                ip,
                port,
                proto,
            ))
        self.conn.begin()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, *args):
        self.cursor.close()
        self.conn.close()
