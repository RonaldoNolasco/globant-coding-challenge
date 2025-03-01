from app.models import Department, Job, Employee
from app.test_setup import test_session, setup_test_db  # Importa el fixture manualmente

def test_create_department(test_session):
    department = Department(id=1, department="Finance")
    test_session.add(department)
    test_session.commit()
    
    retrieved = test_session.get(Department, 1)
    assert retrieved is not None
    assert retrieved.department == "Finance"

def test_update_department(test_session):
    department = test_session.get(Department, 1)
    department.department = "HR"
    test_session.commit()

    updated = test_session.get(Department, 1)
    assert updated.department == "HR"

def test_delete_department(test_session):
    department = test_session.get(Department, 1)
    test_session.delete(department)
    test_session.commit()

    deleted = test_session.get(Department, 1)
    assert deleted is None
