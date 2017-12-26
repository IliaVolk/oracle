import cx_Oracle
from app.config import username, password, ip, port


class Dao:

    def __enter__(self):
        self.conn = cx_Oracle.connect(
            username,
            password,
            '{}:{}/orcl'.format(
                ip,
                port,
            ))
        self.conn.begin()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, *args):
        self.cursor.close()
        self.conn.close()
