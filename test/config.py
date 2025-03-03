import pytest
from sqlalchemy.orm import Session
from app.database import init_db, get_session

# Inicializa la base de datos antes de ejecutar los tests, a nivel de la sesion
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """"""
    init_db()

# Crea una sesión de base de datos compartida para un conjunto de pruebas, a nivel del modulo
@pytest.fixture(scope="module")
def test_session():
    session = next(get_session())
    yield session
    session.close()
