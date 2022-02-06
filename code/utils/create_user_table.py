from utils.db_connection import operate_on_db


def create_user_table():
    with operate_on_db() as c:
    # query must change for psycopg2
        query = """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(20) NOT NULL UNIQUE,
                        password TEXT NOT NULL)
                """
        c.execute(query)