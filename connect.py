from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings


engine = create_engine(settings.database_url, echo=settings.sqlalchemy_echo)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

session = SessionLocal()
