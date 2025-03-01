from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener el nombre del archivo de la BD desde .env
DATABASE_FILE = os.getenv("DATABASE_FILE", "data/database.db")
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"  # Puedes cambiar a otro motor de BD si es necesario

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Función para inicializar la base de datos
def init_db():
    SQLModel.metadata.create_all(engine)

# Obtener sesión
def get_session():
    with Session(engine) as session:
        yield session
