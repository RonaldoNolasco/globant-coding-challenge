from sqlmodel import SQLModel, Field

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
