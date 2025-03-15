from sqlalchemy import create_engine      #type: ignore
from sqlalchemy.orm import sessionmaker     #type: ignore
from dotenv import load_dotenv          #type: ignore
import os   
load_dotenv()

DATABASE_URL = os.getenv("postgreSql_url")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()