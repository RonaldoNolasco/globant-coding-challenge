import pandas as pd
import io
from fastapi import HTTPException
from sqlmodel import select, func, case
from app.models import Department, Job, Employee
from app.utils import get_model_metadata, process_data
from app.constants import MODEL_MAP
import numpy as np
import logging
logger = logging.getLogger('uvicorn.error')
#logger.info('A')

# Funcion generica para leer un archivo CSV y procesar su contenido
def process_csv(file, session, file_type):
    try:
        # Se lee el contenido del archivo
        contents = file.file.read()

        # Si no se encuentra dentro de los modelos mapeados, se lanza un error
        if file_type not in MODEL_MAP:
            raise HTTPException(status_code=400, detail="Unrecognized file type")

        # Se obtiene la clase del modelo
        model = MODEL_MAP[file_type]

        # Se obtiene la metadata de la clase
        metadata = get_model_metadata(model)

        # Se obtiene la lista de campos de la clase
        columns = list(metadata.keys())
        
        # Si no tiene contenido, se crea un dataframe vacio
        if not contents:
            df = pd.DataFrame(columns=columns)
        
        # Sino, se lee el csv con el formato esperado
        else:
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")), header=None, names=columns)
        
        # Se itera por todos las columnas
        for col, col_type in metadata.items(): 

            # Aquellos que en el modelo sean int
            if col_type is int:
                # Se le castea a int, manejando aquellos que son nulos
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        # Reemplazar NaN por None (manejar nulidad de claves foraneas)
        df = df.replace({np.nan: None})

        return process_data(session, model, df, *columns)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def employees_per_quarter(session):

    # Se obtienen los empleados del 2021 por trimestre, agrupando por departamento y area, y se ordena por departamento y trabajo
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

    # Se ejecuta la consulta
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
        select(Department.id, Department.department, func.count(Employee.id).label("hired"))
        .join(Employee, Employee.department_id == Department.id, isouter=True)
        .where(Employee.datetime.like("2021-%"))
        .group_by(Department.id, Department.department)
        .having(func.count(Employee.id) > subquery_avg)
        .order_by(func.count(Employee.id).desc())
    )

    # Se ejecuta la consulta
    results = session.exec(query).all()

    return [
        {
            "id": id,
            "department": department,
            "hired": hired
        } for id, department, hired in results
    ]

