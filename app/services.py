import pandas as pd
import io
from fastapi import HTTPException
from sqlmodel import select, func, case
from app.models import Department, Job, Employee
from app.utils import process_data
import logging
logger = logging.getLogger('uvicorn.error')
#logger.info('A')

def process_csv(file, session, file_type):
    try:
        contents = file.file.read()

        if not contents:
            if file_type == "departments":
                df = pd.DataFrame(columns=["id", "department"])
            elif file_type == "jobs":
                df = pd.DataFrame(columns=["id", "job"])
            elif file_type == "employees":
                df = pd.DataFrame(columns=["id", "name", "datetime", "department_id", "job_id"])
            else:
                raise HTTPException(status_code=400, detail="Unrecognized file type")
        else:
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")), header=None, dtype=str)

        if file_type == "departments":
            df.columns = ["id", "department"]
            df["id"] = df["id"].astype(int)
            return process_data(session, Department, df, "id", "department")

        elif file_type == "jobs":
            df.columns = ["id", "job"]
            df["id"] = df["id"].astype(int)
            return process_data(session, Job, df, "id", "job")

        elif file_type == "employees":
            df.columns = ["id", "name", "datetime", "department_id", "job_id"]
            df["id"] = df["id"].astype(int)
            df["department_id"] = pd.to_numeric(df["department_id"], errors="coerce")
            df["job_id"] = pd.to_numeric(df["job_id"], errors="coerce")
            return process_data(session, Employee, df, "id", "name", "datetime", "department_id", "job_id")
        
        else:
            raise HTTPException(status_code=400, detail="Unrecognized file type")
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def employees_per_quarter(session):
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
    
    return [
        {
            "department": dept,
            "job": job,
            "Q1": q1,
            "Q2": q2,
            "Q3": q3,
            "Q4": q4
        } for dept, job, q1, q2, q3, q4 in results
    ]

from sqlalchemy.sql import select, func

def departments_above_mean(session):
    # Subconsulta para obtener el número de empleados por departamento
    subquery_counts = (
        select(Employee.department_id, func.count(Employee.id).label("dept_count"))
        .where(Employee.datetime.like("2021-%"))
        .group_by(Employee.department_id)
        .subquery()
    )

    # Subconsulta para obtener el promedio de empleados por departamento
    subquery_avg = (
        select(func.avg(subquery_counts.c.dept_count))
        .scalar_subquery()
    )

    # Consulta principal para seleccionar departamentos con empleados por encima del promedio
    query = (
        select(Department.id, Department.department, func.count(Employee.id).label("hired_count"))
        .join(Employee, Employee.department_id == Department.id, isouter=True)
        .where(Employee.datetime.like("2021-%"))
        .group_by(Department.id, Department.department)
        .having(func.count(Employee.id) > subquery_avg)
        .order_by(func.count(Employee.id).desc())
    )

    results = session.exec(query).all()

    return [
        {
            "id": id,
            "department": department,
            "hired_count": hired_count
        } for id, department, hired_count in results
    ]

