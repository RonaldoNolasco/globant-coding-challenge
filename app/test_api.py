from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_departments_csv():
    csv_content = b"1,Finance\n2,Engineering\n3,HR"
    files = {"file": ("departments.csv", csv_content, "text/csv")}
    
    response = client.post("/upload_csv/", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "Data uploaded successfully"}

def test_get_employees_per_quarter():
    response = client.get("/employees_per_quarter/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
