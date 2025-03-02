import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import logging
logger = logging.getLogger('uvicorn.error')

load_dotenv()

# Si la variable TESTING está en "true", usar BD en memoria
DATABASE_URL = os.environ.get("DATABASE_URL")

# DESA: "sqlite:///db/database.db"
# CERT: "sqlite:///db/test_database.db"
# PROD: "postgresql://postgres:TQIZrLVrMCuTjEDVSbYmGsxvmdELdhEI@postgres.railway.internal:5432/railway"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    logger.info(DATABASE_URL)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
