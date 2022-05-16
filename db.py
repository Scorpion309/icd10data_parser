import logging

from mysql.connector import connect, Error

from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD


def create_db(connection):
    create_db_query = "CREATE DATABASE IF NOT EXISTS medical_codes"
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)

def connect_to_db():
    try:
        with connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
        ) as connection:
            create_db(connection)
            connection.connect(database="medical_codes")
    except Error as e:
        logging.warning(e)
