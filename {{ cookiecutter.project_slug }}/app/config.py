import logging
import os
import sys

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

APP_LOG_LEVEL = os.getenv("APP_LOG_LEVEL", "INFO").upper()
APP_PORT = int(os.getenv("APP_PORT", 8000))
APP_TIMEZONE_LOCAL = "America/Santiago"

DB_CONNECTION_URL = os.environ["DB_CONNECTION_URL"]
DB_ECHO = os.getenv("DB_ECHO", False)


logging.basicConfig(
    level=APP_LOG_LEVEL,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
