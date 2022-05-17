import os

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
FULL_URL = os.getenv("FULL_URL")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")

MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
