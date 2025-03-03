from app.models import Department, Job, Employee
from test.config import test_session, setup_test_db
from sqlmodel import Session, select

# Test para crear un departamento
def test_create_department(test_session):
    department = Department(id=1, department="Finance")
    test_session.add(department)
    test_session.commit()

    result = test_session.exec(select(Department).where(Department.id == 1)).first()
    assert result is not None
    assert result.department == "Finance"

# Test para actualizar un departamento
def test_update_department(test_session):
    department = test_session.exec(select(Department).where(Department.id == 1)).first()
    department.department = "Updated Finance"
    test_session.commit()

    result = test_session.exec(select(Department).where(Department.id == 1)).first()
    assert result.department == "Updated Finance"

# Test para eliminar un departamento
def test_delete_department(test_session):
    department = test_session.exec(select(Department).where(Department.id == 1)).first()
    test_session.delete(department)
    test_session.commit()

    result = test_session.exec(select(Department).where(Department.id == 1)).first()
    assert result is None

# Test para crear un trabajo
def test_create_job(test_session):
    job = Job(id=1, job="Analyst")
    test_session.add(job)
    test_session.commit()

    result = test_session.exec(select(Job).where(Job.id == 1)).first()
    assert result is not None
    assert result.job == "Analyst"

# Test para actualizar un trabajo
def test_update_job(test_session):
    job = test_session.exec(select(Job).where(Job.id == 1)).first()
    job.job = "Senior Analyst"
    test_session.commit()

    result = test_session.exec(select(Job).where(Job.id == 1)).first()
    assert result.job == "Senior Analyst"

# Test para eliminar un trabajo
def test_delete_job(test_session):
    job = test_session.exec(select(Job).where(Job.id == 1)).first()
    test_session.delete(job)
    test_session.commit()

    result = test_session.exec(select(Job).where(Job.id == 1)).first()
    assert result is None

# Test para crear un empleado
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

# Test para actualizar un empleado
def test_update_employee(test_session):
    employee = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    employee.name = "John Smith"
    test_session.commit()

    result = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    assert result.name == "John Smith"

# Test para eliminar un empleado
def test_delete_employee(test_session):
    employee = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    test_session.delete(employee)
    test_session.commit()

    result = test_session.exec(select(Employee).where(Employee.id == 1)).first()
    assert result is None