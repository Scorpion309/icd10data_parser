import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
FULL_URL = os.getenv("FULL_URL")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")

MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
