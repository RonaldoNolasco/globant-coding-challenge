import os
import sys

# Agregar el directorio raíz del proyecto al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.database import get_session
from app.models import Employee

DATABASE_URL = "sqlite:///data/test_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def get_test_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Crea y limpia la BD antes y después de los tests."""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
    

# 1️⃣ Test para crear un empleado
def test_create_employee(setup_database):
    employee_data = {
        "name": "Juan Pérez",
        "department_id": 1,
        "job_id": 1,
        "datetime": "2024-01-15"
    }
    response = client.post("/api/employees/", json=employee_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Juan Pérez"

# 2️⃣ Test para obtener empleados
def test_get_employees(setup_database):
    response = client.get("/api/employees/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# 3️⃣ Test para actualizar un empleado
def test_update_employee(setup_database):
    employee_id = 1  # Asegúrate de que existe un empleado con ID=1
    updated_data = {"name": "Juan Pérez Modificado"}
    response = client.put(f"/api/employees/{employee_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Juan Pérez Modificado"

# 4️⃣ Test para eliminar un empleado
def test_delete_employee(setup_database):
    employee_id = 1
    response = client.delete(f"/api/employees/{employee_id}")
    assert response.status_code == 204

# 5️⃣ Test para obtener empleados por trimestre
def test_get_employees_per_quarter(setup_database):
    response = client.get("/api/employees_per_quarter/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
