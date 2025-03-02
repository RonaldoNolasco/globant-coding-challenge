import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv

load_dotenv()

# Si la variable TESTING está en "true", usar BD en memoria
TESTING = os.getenv("TESTING", "false").lower() == "true"

if TESTING:
    DATABASE_URL = "sqlite:///db/test_database.db"
else:
    DATABASE_URL = "sqlite:///db/database.db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    if TESTING:
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    else:
        #SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
