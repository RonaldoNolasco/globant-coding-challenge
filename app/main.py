from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlmodel import Session, select, func, case
import pandas as pd
import io
from database import create_db_and_tables, get_session, engine
from models import Department, Job, Employee

# Inicializar la base de datos
create_db_and_tables()

# Crear la aplicación FastAPI
app = FastAPI()

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), session: Session = Depends(get_session)):
    try:
        contents = await file.read()
        filename = file.filename.lower()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), header=None, dtype=str)
        
        # Determinar el tipo de archivo y aplicar esquema con casteo de datos
        if "departments" in filename:
            df.columns = ["id", "department"]
            df["id"] = df["id"].astype(int)
            departments = [Department(id=int(row["id"]), department=str(row["department"])) for _, row in df.iterrows()]
            session.add_all(departments)
        
        elif "jobs" in filename:
            df.columns = ["id", "job"]
            df["id"] = df["id"].astype(int)
            jobs = [Job(id=int(row["id"]), job=str(row["job"])) for _, row in df.iterrows()]
            session.add_all(jobs)
        
        elif "hired_employees" in filename:
            df.columns = ["id", "name", "datetime", "department_id", "job_id"]
            df["id"] = df["id"].astype(int)
            df["department_id"] = pd.to_numeric(df["department_id"], errors="coerce")
            df["job_id"] = pd.to_numeric(df["job_id"], errors="coerce")
            employees = [Employee(id=int(row["id"]), name=str(row["name"]), datetime=str(row["datetime"]),
                                  department_id=int(row["department_id"]) if not pd.isna(row["department_id"]) else None,
                                  job_id=int(row["job_id"]) if not pd.isna(row["job_id"]) else None)
                         for _, row in df.iterrows()]
            session.add_all(employees)
        
        else:
            raise HTTPException(status_code=400, detail="Unrecognized file format")
        
        session.commit()
        return {"message": "Data uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/employees_per_quarter/")
def employees_per_quarter(session: Session = Depends(get_session)):
    query = (
        select(
            Department.department, Job.job,
            func.sum(case((func.substr(Employee.datetime, 6, 2).in_(["01", "02", "03"]), 1), else_=0)).label("Q1"),
            func.sum(case((func.substr(Employee.datetime, 6, 2).in_(["04", "05", "06"]), 1), else_=0)).label("Q2"),
            func.sum(case((func.substr(Employee.datetime, 6, 2).in_(["07", "08", "09"]), 1), else_=0)).label("Q3"),
            func.sum(case((func.substr(Employee.datetime, 6, 2).in_(["10", "11", "12"]), 1), else_=0)).label("Q4")
        )
        .join(Employee, Employee.department_id == Department.id, isouter=True)
        .join(Job, Employee.job_id == Job.id, isouter=True)
        .where(Employee.datetime.like("2021-%"))
        .group_by(Department.department, Job.job)
        .order_by(Department.department, Job.job)
    )
    
    results = session.exec(query).all()
    
    response = [{
        "department": department,
        "job": job,
        "Q1": q1,
        "Q2": q2,
        "Q3": q3,
        "Q4": q4
    } for department, job, q1, q2, q3, q4 in results]
    
    return response

@app.get("/departments_above_mean/")
def departments_above_mean(session: Session = Depends(get_session)):
    subquery = select(func.avg(func.count(Employee.id))).where(Employee.datetime.like("2021-%")).group_by(Employee.department_id).scalar_subquery()
    
    query = (
        select(Department.id, Department.department, func.count(Employee.id).label("hired_count"))
        .join(Employee, Employee.department_id == Department.id, isouter=True)
        .where(Employee.datetime.like("2021-%"))
        .group_by(Department.id, Department.department)
        .having(func.count(Employee.id) > subquery)
        .order_by(func.count(Employee.id).desc())
    )
    
    results = session.exec(query).all()
    
    response = [{
        "id": id,
        "department": department,
        "hired_count": hired_count
    } for id, department, hired_count in results]
    
    return response
