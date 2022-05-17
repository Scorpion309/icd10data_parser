import logging

from mysql.connector import connect, Error

from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD


def create_db(connection):
    create_db_query = "CREATE DATABASE IF NOT EXISTS medical_codes"
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)


def create_table(connection):
    create_db_query = """CREATE TABLE IF NOT EXISTS codes(
                     pk INT AUTO_INCREMENT PRIMARY KEY,
                     group_code VARCHAR(7),
                     group_desc VARCHAR(256),
                     code VARCHAR(3),
                     code_desc VARCHAR(256)
                     );"""
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)


def insert_data(connection, *args):
    create_db_query = """INSERT INTO codes (group_code, group_desc, code, code_desc)
                         VALUES ( %s, %s, %s, %s);
                      """
    with connection.cursor() as cursor:
        cursor.execute(create_db_query, args)


def get_data(connection):
    create_db_query = "SELECT * FROM codes;"
    with connection.cursor() as cursor:
        return cursor.execute(create_db_query)


def save_data_to_db(data):
    try:
        with connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
        ) as connection:
            logging.info('Connected to DB! Creating data table...')
            create_db(connection)
            connection.connect(database="medical_codes")
            create_table(connection)
            logging.info('Data table created! Saving data...')
            for group_code, detailed_elements in data.items():
                group_desc = detailed_elements['group_desc']
                for detailed_code, group_detailed_elements in detailed_elements['detailed_code'].items():
                    for code, group_elements in group_detailed_elements['detailed_code'].items():
                        code_desc = group_elements['group_desc']
                        insert_data(connection, group_code, group_desc, code, code_desc)
            connection.commit()
            logging.info('Data saved.')
    except Error as error:
        logging.warning(error, error.args)
        raise
    finally:
        connection.close()
        logging.info('Connection closed.')
