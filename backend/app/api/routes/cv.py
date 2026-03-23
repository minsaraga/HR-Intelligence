from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Employee, EmployeeSkill, Skill
from app.db.session import get_db
from app.services.skills import extract_skills_from_file

router = APIRouter()


@router.post("/{employee_id}/cv/upload")
async def upload_cv(employee_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    content = await file.read()
    extracted = extract_skills_from_file(file.filename or "", content)

    for item in extracted:
        skill = db.query(Skill).filter(Skill.slug == item["skill"]).first()
        if not skill:
            skill = Skill(slug=item["skill"], name=item["skill"].replace("-", " ").title(), category="inferred")
            db.add(skill)
            db.flush()

        existing = db.query(EmployeeSkill).filter(
            EmployeeSkill.employee_id == employee_id,
            EmployeeSkill.skill_id == skill.id,
        ).first()

        if existing:
            existing.proficiency = max(existing.proficiency, item["proficiency"])
            existing.confidence = max(existing.confidence, item["confidence"])
            existing.source = item["source"]
        else:
            db.add(EmployeeSkill(
                employee_id=employee_id,
                skill_id=skill.id,
                proficiency=item["proficiency"],
                confidence=item["confidence"],
                source=item["source"],
            ))

    db.commit()
    return {
        "employee_id": employee_id,
        "filename": file.filename,
        "extracted_skills": extracted,
        "profile_updated": True,
    }
