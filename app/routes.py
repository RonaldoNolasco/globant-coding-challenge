from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session
from app.database import get_session
from app.services import process_csv, employees_per_quarter, departments_above_mean

router = APIRouter()

@router.post("/upload/departments/")
async def upload_departments(file: UploadFile = File(...), session: Session = Depends(get_session)):
    return process_csv(file, session, file_type="departments")

@router.post("/upload/jobs/")
async def upload_jobs(file: UploadFile = File(...), session: Session = Depends(get_session)):
    return process_csv(file, session, file_type="jobs")

@router.post("/upload/employees/")
async def upload_employees(file: UploadFile = File(...), session: Session = Depends(get_session)):
    return process_csv(file, session, file_type="employees")

@router.get("/employees_per_quarter/")
def get_employees_per_quarter(session: Session = Depends(get_session)):
    return employees_per_quarter(session)

@router.get("/departments_above_mean/")
def get_departments_above_mean(session: Session = Depends(get_session)):
    return departments_above_mean(session)
