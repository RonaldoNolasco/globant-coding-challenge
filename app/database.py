from sqlmodel import SQLModel, Session, create_engine
import os

# Obtener el nombre del archivo de la base de datos desde la variable de entorno
DB_FILENAME = os.getenv("DATABASE_NAME", "database.db")
DATABASE_URL = f"sqlite:///./{DB_FILENAME}"  # Construir la URL de conexión

# Si se usa SQLite, eliminar la BD existente para recrearla
""" if os.path.exists(DB_FILENAME):
    os.remove(DB_FILENAME) """

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Función para inicializar la base de datos
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependencia para obtener la sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session