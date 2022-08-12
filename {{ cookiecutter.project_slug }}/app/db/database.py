from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DB_CONNECTION_URL

engine = create_engine(DB_CONNECTION_URL)  # fast_executemany=True
Session = sessionmaker(engine, autoflush=False, autocommit=False)
