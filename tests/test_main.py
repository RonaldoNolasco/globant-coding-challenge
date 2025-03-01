import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
import os
import sys

# Agregar el directorio raíz del proyecto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.models import Department, Job, Employee
from app.database import get_session

# Crear una base de datos en memoria para pruebas
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)

# Fixture para crear la base de datos de prueba antes de cada test
@pytest.fixture(name="session")
def setup_db():
    SQLModel.metadata.create_all(engine)  # Crear tablas
    with Session(engine) as session:
        yield session  # Pasar sesión a la prueba
    SQLModel.metadata.drop_all(engine)  # Limpiar después de la prueba

# Sobrescribir la dependencia de la sesión de la BD en la API
def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

# ------------------ TESTS ------------------

def test_insert_employee(session):
    """Prueba la inserción de un empleado"""
    employee = Employee(id=1, name="John Doe", datetime="2021-06-15", department_id=1, job_id=1)
    session.add(employee)
    session.commit()
    
    stored_employee = session.get(Employee, 1)
    assert stored_employee is not None
    assert stored_employee.name == "John Doe"

def test_update_employee(session):
    """Prueba la actualización de un empleado"""
    employee = Employee(id=2, name="Jane Doe", datetime="2021-06-15", department_id=1, job_id=1)
    session.add(employee)
    session.commit()

    employee.name = "Jane Smith"
    session.commit()

    updated_employee = session.get(Employee, 2)
    assert updated_employee.name == "Jane Smith"

def test_delete_employee(session):
    """Prueba la eliminación de un empleado"""
    employee = Employee(id=3, name="Alice", datetime="2021-06-15", department_id=1, job_id=1)
    session.add(employee)
    session.commit()

    session.delete(employee)
    session.commit()

    deleted_employee = session.get(Employee, 3)
    assert deleted_employee is None

def test_upload_csv():
    """Prueba la carga de un archivo CSV a través del endpoint"""
    csv_data = "id,department\n1,Engineering\n2,HR"
    files = {"file": ("departments.csv", csv_data, "text/csv")}
    
    response = client.post("/api/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

def test_employees_per_quarter():
    """Prueba el endpoint /employees_per_quarter/"""
    response = client.get("/api/employees_per_quarter/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_departments_above_mean():
    """Prueba el endpoint /departments_above_mean/"""
    response = client.get("/api/departments_above_mean/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
