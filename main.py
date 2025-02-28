# Importando clases
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
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
    department_id: int = Field(foreign_key="department.id")
    job_id: int = Field(foreign_key="job.id")

# Configuracion de BD
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# Eliminar la base de datos si existe
if os.path.exists(sqlite_file_name):
    os.remove(sqlite_file_name)

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