from sqlmodel import SQLModel, Field
from typing import Optional

# Modelo de Department
class Department(SQLModel, table=True):
    id: int = Field(primary_key=True)
    department: str = Field(index=True)

# Modelo de Job
class Job(SQLModel, table=True):
    id: int = Field(primary_key=True)
    job: str = Field(index=True)

# Modelo de Employee
class Employee(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True, nullable=True)
    datetime: str = Field(index=True, nullable=True)
    department_id: int = Field(foreign_key="department.id", nullable=True)
    job_id: int = Field(foreign_key="job.id", nullable=True)