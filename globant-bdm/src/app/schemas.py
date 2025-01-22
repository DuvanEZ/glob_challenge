from pydantic import BaseModel
from datetime import datetime

class DepartmentBase(BaseModel):
    id: int
    department: str

class JobBase(BaseModel):
    id: int
    job: str

class EmployeeBase(BaseModel):
    id: int
    name: str
    datetime: datetime
    department_id: int
    job_id: int

class DepartmentCreate(DepartmentBase):
    pass

class JobCreate(JobBase):
    pass

class EmployeeCreate(EmployeeBase):
    pass
