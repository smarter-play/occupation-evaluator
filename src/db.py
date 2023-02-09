from dotenv import load_dotenv
import mysql.connector
import os


load_dotenv()


db_connection = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    port=os.environ['DB_PORT'],
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_DATABASE'],
)
