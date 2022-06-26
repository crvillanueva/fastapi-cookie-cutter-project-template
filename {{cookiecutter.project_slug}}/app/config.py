import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

DB_CONNECTION_URL = os.environ["DB_CONNECTION_URL"]
TIMEZONE_LOCAL = "America/Santiago"
