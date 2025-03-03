import os
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import logging
logger = logging.getLogger('uvicorn.error')

# Se cargan las variables de entorno
load_dotenv()

# Se obtiene la url de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL")

# DESA: "sqlite:///db/database.db"
# CERT: "sqlite:///db/test_database.db"
# PROD: Cadena de conexion generada en railway.com

# Se crea el motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Se define la funcion de inicializacion de la BD
def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

# Se define la funcion de obtencion de la sesion
def get_session():
    with Session(engine) as session:
        yield session
