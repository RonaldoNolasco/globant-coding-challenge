from fastapi.testclient import TestClient
from test.config import test_session, setup_test_db
from app.main import app
import io

client = TestClient(app)

def test_upload_departments_csv():
    csv_content = b"1,Finance\n2,Engineering\n3,HR"
    files = {"file": ("departments.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload/departments/", files=files)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["message"] == "Data processed successfully"
    assert json_response["inserted"] == 3
    assert json_response["updated"] == 0
    assert json_response["deleted"] == 0

def test_upload_jobs_csv():
    csv_content = b"1,Analyst\n2,Developer\n3,Manager"
    files = {"file": ("jobs.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload/jobs/", files=files)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["message"] == "Data processed successfully"
    assert json_response["inserted"] == 3
    assert json_response["updated"] == 0
    assert json_response["deleted"] == 0

def test_upload_employees_csv():
    csv_content = b"1,John Doe,2021-03-15,1,2\n2,Jane Doe,2021-06-20,2,3"
    files = {"file": ("employees.csv", io.BytesIO(csv_content), "text/csv")}
    response = client.post("/upload/employees/", files=files)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["message"] == "Data processed successfully"
    assert json_response["inserted"] == 2
    assert json_response["updated"] == 0
    assert json_response["deleted"] == 0


def test_get_employees_per_quarter():
    response = client.get("/employees_per_quarter/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Debe devolver una lista

def test_get_departments_above_mean():
    response = client.get("/departments_above_mean/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Debe devolver una lista
