from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Employee
from app.db.session import get_db
from app.schemas.requests import EmployeeCreateRequest

router = APIRouter()


@router.post("")
def create_employee(payload: EmployeeCreateRequest, db: Session = Depends(get_db)):
    employee = Employee(
        name=payload.name,
        role=payload.role,
        geography=payload.geography,
        career_stage=payload.career_stage,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return {
        "id": employee.id,
        "name": employee.name,
        "role": employee.role,
        "geography": employee.geography,
        "career_stage": employee.career_stage,
        "skills": {},
        "certifications": [],
    }


@router.get("/search")
def search_employees(name: str, db: Session = Depends(get_db)):
    rows = db.query(Employee).filter(Employee.name.ilike(f"%{name}%")).all()
    return [
        {
            "id": emp.id,
            "name": emp.name,
            "role": emp.role,
            "geography": emp.geography,
            "career_stage": emp.career_stage,
        }
        for emp in rows
    ]


@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {
        "id": employee.id,
        "name": employee.name,
        "role": employee.role,
        "geography": employee.geography,
        "career_stage": employee.career_stage,
        "skills": {
            es.skill.slug: {
                "proficiency": es.proficiency,
                "confidence": es.confidence,
                "source": es.source,
            }
            for es in employee.skills
        },
        "certifications": [ec.certification.slug for ec in employee.certifications],
    }
