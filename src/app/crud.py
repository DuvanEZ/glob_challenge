from sqlalchemy.orm import Session
from . import models, schemas

def create_department(db: Session, department: schemas.DepartmentCreate):
    new_dept = models.Department(**department.dict())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

def create_job(db: Session, job: schemas.JobCreate):
    new_job = models.Job(**job.dict())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    new_emp = models.Employee(**employee.dict())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

def get_departments(db: Session):
    return db.query(models.Department).all()

def get_jobs(db: Session):
    return db.query(models.Job).all()

def get_employees(db: Session):
    return db.query(models.Employee).all()
