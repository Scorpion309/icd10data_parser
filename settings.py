import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
FULL_URL = os.getenv("FULL_URL")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL")
