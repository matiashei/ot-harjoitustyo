import os
from dotenv import load_dotenv

dirname = os.path.dirname(__file__)

try:
    load_dotenv(os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

DATABASE_FILENAME = os.getenv("DATABASE_FILENAME", "tilix.db")
DATABASE_FILE_PATH = os.path.join(dirname, "..", "data", DATABASE_FILENAME)