from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Employee, Certification, Skill, LearningResource

router = APIRouter()


@router.get("/employees/search")
def search_employees(name: str = "", db: Session = Depends(get_db)):
    query = db.query(Employee)
    if name:
        query = query.filter(Employee.name.ilike(f"%{name}%"))
    employees = query.all()
    return [
        {
            "id": e.id,
            "name": e.name,
            "role": e.role,
            "geography": e.geography,
            "career_stage": e.career_stage,
        }
        for e in employees
    ]


@router.get("/certifications/available")
def list_certifications(db: Session = Depends(get_db)):
    certs = db.query(Certification).all()
    return [{"slug": c.slug, "name": c.name} for c in certs]


@router.get("/employees/skills/suggestions")
def skill_suggestions(db: Session = Depends(get_db)):
    skills = db.query(LearningResource.skill_slug).distinct().all()
    return [s[0] for s in skills]
