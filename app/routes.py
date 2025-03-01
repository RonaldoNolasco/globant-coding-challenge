from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session
from app.database import get_session
from app.services import process_csv, employees_per_quarter, departments_above_mean

router = APIRouter()

@router.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), session: Session = Depends(get_session)):
    return process_csv(file, session)

@router.get("/employees_per_quarter/")
def get_employees_per_quarter(session: Session = Depends(get_session)):
    return employees_per_quarter(session)

@router.get("/departments_above_mean/")
def get_departments_above_mean(session: Session = Depends(get_session)):
    return departments_above_mean(session)
