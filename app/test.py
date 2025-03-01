import pytest
import io
from sqlmodel import Session, select
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, get_session
from app.models import Department, Job, Employee

# Setup de la BD de prueba
@pytest.fixture(autouse=True)
def setup_test_db():
    """ Reinicia la base de datos en memoria antes de cada test """
    init_db()

@pytest.fixture
def test_session():
    """ Obtiene una sesión de prueba y la cierra al final """
    session = next(get_session())
    yield session
    session.close()

client = TestClient(app)

# TESTS CRUD PARA Department
def test_create_department(test_session):
    department = Department(id=1, department="Finance")
    test_session.add(department)
    test_session.commit()

    result = test_session.exec(select(Department).where(Department.id == 1)).first()
    assert result is not None
    assert result.department == "Finance"

def test_update_department(test_session):
    department = test_session.exec(select(Department).where(Department.id == 1)).first()
    department.department = "Updated Finance"
    test_session.commit()

    result = test_session.exec(select(Department).where(Department.id == 1)).first()
    assert result.department == "Updated Finance"

def test_delete_department(test_session):
    department = test_session.exec(select(Department).where(Department.id == 1)).first()
    test_session.delete(department)
    test_session.commit()

    result = test_session.exec(select(Department).where(Department.id == 1)).first()
    assert result is None

# TESTS CRUD PARA Job
def test_create_job(test_session):
    job = Job(id=1, job="Analyst")
    test_session.add(job)
    test_session.commit()

    result = test_session.exec(select(Job).where(Job.id == 1)).first()
    assert result is not None
    assert result.job == "Analyst"

def test_update_job(test_session):
    job = test_session.exec(select(Job).where(Job.id == 1)).first()
    job.job = "Senior Analyst"
    test_session.commit()

    result = test_session.exec(select(Job).where(Job.id == 1)).first()
    assert result.job == "Senior Analyst"

def test_delete_job(test_session):
    job = test_session.exec(select(Job).where(Job.id == 1)).first()
    test_session.delete(job)
    test_session.commit()

    result = test_session.exec(select(Job).where(Job.id == 1)).first()
    assert result is None

# TESTS CRUD PARA Employee
def test_create_employee(test_session):
    test_session.add(Department(id=1, department="Finance"))
    test_session.add(Job(id=1, job="Analyst"))
    test_session.commit()

    employee = Employee(id=1, name="John Doe", datetime="2024-02-01", department_id=1, job_id=1)
    test_session.add(employee)
    test_session.commit()

    result = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    assert result is not None
    assert result.name == "John Doe"
    assert result.department_id == 1
    assert result.job_id == 1

def test_update_employee(test_session):
    employee = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    employee.name = "John Smith"
    test_session.commit()

    result = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    assert result.name == "John Smith"

def test_delete_employee(test_session):
    employee = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    test_session.delete(employee)
    test_session.commit()

    result = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    assert result is None

# TESTS DE API
def test_upload_departments_csv():
    csv_content = b"1,Finance\n2,Engineering\n3,HR"
    files = {"file": ("departments.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

def test_upload_jobs_csv():
    csv_content = b"1,Analyst\n2,Developer\n3,Manager"
    files = {"file": ("jobs.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

def test_upload_employees_csv():
    csv_content = b"1,John Doe,2021-03-15,1,2\n2,Jane Doe,2021-06-20,2,3"
    files = {"file": ("hired_employees.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

def test_get_employees_per_quarter():
    response = client.get("/employees_per_quarter/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Debe devolver una lista

def test_get_departments_above_mean():
    response = client.get("/departments_above_mean/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Debe devolver una lista

