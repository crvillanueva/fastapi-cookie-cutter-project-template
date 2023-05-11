from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_CONNECTION_URL, DB_ECHO

engine = create_engine(DB_CONNECTION_URL, echo=DB_ECHO)  # fast_executemany=True
Session = sessionmaker(engine, autoflush=False, autocommit=False)
