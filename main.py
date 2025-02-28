# Importando clases
from typing import Annotated
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select, func
import pandas as pd
import io
import os


# Tablas de base de datos
class Department(SQLModel, table=True):
    id: int = Field(primary_key=True)
    department: str = Field(index=True)

class Job(SQLModel, table=True):
    id: int = Field(primary_key=True)
    job: str = Field(index=True)

class Employee(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    datetime: str = Field(index=True)
    department_id: int = Field(foreign_key="department.id", nullable=True)
    job_id: int = Field(foreign_key="job.id", nullable=True)

# Configuracion de BD
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Eliminar la base de datos si existe
""" if os.path.exists(sqlite_file_name):
    os.remove(sqlite_file_name)
 """
# Se crean las tablas de la BD
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Se genera la sesión de la aplicación
def get_session():
    with Session(engine) as session:
        yield session

# Se inicializa la aplicación
SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()

# Se define una accion al iniciar la aplicacion
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/upload_csv/")
async def upload_csv(file: UploadFile = File(...), session: Session = Depends(get_session)):
    try:
        contents = await file.read()
        filename = file.filename.lower()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")), header=None, dtype=str)
        
        # Determinar el tipo de archivo subido y aplicar el esquema correcto con casteo de datos
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
        select(Department.department, Job.job,
               func.substr(Employee.datetime, 6, 2).label("month"),
               func.count().label("num_employees"))
        .join(Employee, Employee.department_id == Department.id, isouter=True)
        .join(Job, Employee.job_id == Job.id, isouter=True)
        .where(Employee.datetime.like("2021-%"))
        .group_by(Department.department, Job.job, "month")
        .order_by(Department.department, Job.job)
    )
    
    results = session.exec(query).all()
    
    output = {}
    for department, job, month, num_employees in results:
        quarter = (int(month) - 1) // 3 + 1
        key = (department, job)
        if key not in output:
            output[key] = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
        output[key][f"Q{quarter}"] += num_employees
    
    response = []
    for (department, job), quarters in output.items():
        response.append({"department": department, "job": job, **quarters})
    
    return response


""" @app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]} """
""" 
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True} """