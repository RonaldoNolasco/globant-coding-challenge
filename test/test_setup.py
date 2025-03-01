import pytest
from sqlalchemy.orm import Session
from app.database import init_db, get_session

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Inicializa la base de datos antes de ejecutar los tests."""
    init_db()

@pytest.fixture(scope="module")
def test_session():
    """Crea una sesión de base de datos compartida para un conjunto de pruebas."""
    session = next(get_session())  # Obtiene la sesión de la BD
    yield session
    session.close()
