from dotenv import load_dotenv


load_dotenv()


import mysql.connector
import os
import logging


logger = logging.getLogger('db')
#logger.setLevel(getattr(logging, os.environ['LOG_LEVEL'].upper(), None))

db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']
db_database = os.environ['DB_DATABASE']


def create_db_connection():
    db_connection = mysql.connector.connect(
        host=db_host,
        port=db_port,
        user=db_username,
        password=db_password,
        database=db_database,
        pool_size=10,
    )
    return db_connection
