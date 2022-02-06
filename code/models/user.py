from exceptions.db_connection_exceptions import DbConnectionException
from utils.db_connection import operate_on_db, read_from_db
from schemas.user import User


class UserModel:
    
    def __init__(self, user: User):
        self.user = user

    @classmethod
    def find_by_username(cls, username: str):
        try:
            with read_from_db() as c:
                query = "SELECT * FROM users WHERE username=%s"
                c.execute(query, (username,))
                result = c.fetchone()
        except:
            raise DbConnectionException()
        return cls(
            user=User.from_db(*result)
         ) if result else None

    @classmethod
    def find_by_userid(cls, _id):
        try:
            with read_from_db() as c:
                query = "SELECT * FROM users WHERE id=%(int)s"
                c.execute(query, (_id,))
                result = c.fetchone()
        except:
            raise DbConnectionException()
        return cls(
            user=User.from_db(*result)
         ) if result else None

    def save_to_db(self):
        try:
            with operate_on_db() as c:
                query = "INSERT INTO users (username, password) VALUES (%s,%s)"
                c.execute(query, (self.user.username,self.user.password))
        except:
            raise DbConnectionException()

    def delete_from_db(self):
        try:
            with operate_on_db() as c:
                query ="DELETE FROM users WHERE username=%s"
                c.execute(query, (self.user.username,))
        except:
            raise DbConnectionException()