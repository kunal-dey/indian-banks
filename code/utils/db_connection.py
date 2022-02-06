import psycopg2
from contextlib import contextmanager

from utils.config_files import CONFIG


@contextmanager
def read_from_db():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host=CONFIG['database']['host'],
            port=CONFIG['database']['port'],
            database=CONFIG['database']['database'],
            user=CONFIG['database']['user'],
            password=CONFIG['database']['password']
        )
        cursor = connection.cursor()
        yield cursor
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@contextmanager
def operate_on_db():
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            host="localhost",
            port="6000",
            database="indianbanks",
            user="postgres",
            password="kunal@22061994"
        )
        cursor = connection.cursor()
        yield cursor
        connection.commit()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
