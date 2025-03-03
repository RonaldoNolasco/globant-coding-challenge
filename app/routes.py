from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session
from app.database import get_session
from app.services import process_csv, employees_per_quarter, departments_above_mean

router = APIRouter()

# Ruta para la carga del csv de department
@router.post("/upload/departments/")
async def upload_departments(file: UploadFile = File(...), session: Session = Depends(get_session)):
    return process_csv(file, session, file_type="departments")

# Ruta para la carga del csv de job
@router.post("/upload/jobs/")
async def upload_jobs(file: UploadFile = File(...), session: Session = Depends(get_session)):
    return process_csv(file, session, file_type="jobs")

# Ruta para la carga del csv de hired_employees
@router.post("/upload/employees/")
async def upload_employees(file: UploadFile = File(...), session: Session = Depends(get_session)):
    return process_csv(file, session, file_type="employees")

# Ruta para obtener el reporte de empleados por trimestre
@router.get("/employees_per_quarter/")
def get_employees_per_quarter(session: Session = Depends(get_session)):
    return employees_per_quarter(session)

# Ruta para obtener los departamentos por encima de la media
@router.get("/departments_above_mean/")
def get_departments_above_mean(session: Session = Depends(get_session)):
    return departments_above_mean(session)
