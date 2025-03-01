import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

from app.database import init_db

@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()  # Reinicia la BD en memoria antes de cada test

client = TestClient(app)

# Test: Subir un archivo CSV de departamentos
def test_upload_departments_csv():
    csv_content = b"1,Finance\n2,Engineering\n3,HR"
    files = {"file": ("departments.csv", io.BytesIO(csv_content), "text/csv")}
    
    response = client.post("/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

# Test: Subir un archivo CSV de trabajos
def test_upload_jobs_csv():
    csv_content = b"1,Analyst\n2,Developer\n3,Manager"
    files = {"file": ("jobs.csv", io.BytesIO(csv_content), "text/csv")}
    
    response = client.post("/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

# Test: Subir un archivo CSV de empleados
def test_upload_employees_csv():
    csv_content = b"1,John Doe,2021-03-15,1,2\n2,Jane Doe,2021-06-20,2,3"
    files = {"file": ("hired_employees.csv", io.BytesIO(csv_content), "text/csv")}
    
    response = client.post("/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

# Test: Obtener empleados por trimestre
def test_get_employees_per_quarter():
    response = client.get("/employees_per_quarter/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Debe devolver una lista
    # No verificamos datos exactos porque pueden variar según el estado de la BD

# Test: Obtener departamentos con contrataciones por encima del promedio
def test_get_departments_above_mean():
    response = client.get("/departments_above_mean/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Debe devolver una lista
