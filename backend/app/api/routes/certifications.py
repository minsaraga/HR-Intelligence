from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Certification, CertificationSkillMap, Employee, EmployeeCertification, EmployeeSkill, Skill
from app.db.session import get_db
from app.schemas.requests import CertificationUpdateRequest

router = APIRouter()


@router.get("/certifications/available")
def available_certifications(db: Session = Depends(get_db)):
    return [
        {"slug": c.slug, "name": c.name}
        for c in db.query(Certification).all()
    ]


@router.post("/employees/{employee_id}/certifications")
def add_certification(employee_id: int, payload: CertificationUpdateRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    certification = db.query(Certification).filter(Certification.slug == payload.certification_slug).first()
    if not certification:
        raise HTTPException(status_code=404, detail="Certification mapping not found")

    already = db.query(EmployeeCertification).filter(
        EmployeeCertification.employee_id == employee_id,
        EmployeeCertification.certification_id == certification.id,
    ).first()
    if not already:
        db.add(EmployeeCertification(employee_id=employee_id, certification_id=certification.id))

    mapped = db.query(CertificationSkillMap).filter(CertificationSkillMap.certification_id == certification.id).all()
    mapped_skills = []
    for entry in mapped:
        skill = db.query(Skill).filter(Skill.id == entry.skill_id).first()
        existing = db.query(EmployeeSkill).filter(
            EmployeeSkill.employee_id == employee_id,
            EmployeeSkill.skill_id == skill.id,
        ).first()
        if existing:
            existing.proficiency = max(existing.proficiency, 3)
            existing.confidence = max(existing.confidence, entry.weight)
            existing.source = f"certification:{payload.certification_slug}"
        else:
            db.add(EmployeeSkill(
                employee_id=employee_id,
                skill_id=skill.id,
                proficiency=3,
                confidence=entry.weight,
                source=f"certification:{payload.certification_slug}",
            ))
        mapped_skills.append({"skill": skill.slug, "weight": entry.weight})

    db.commit()
    return {
        "employee_id": employee_id,
        "certification": payload.certification_slug,
        "mapped_skills": mapped_skills,
        "profile_updated": True,
    }
