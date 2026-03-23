from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Employee, LearningResource
from app.db.session import get_db
from app.schemas.requests import RecommendationRequest
from app.services.recommendations import build_learning_path

router = APIRouter()


@router.get("/skills/suggestions")
def skill_suggestions(db: Session = Depends(get_db)):
    rows = db.query(LearningResource.skill_slug).distinct().all()
    return sorted([r[0] for r in rows])


@router.post("/{employee_id}/recommendations")
def get_recommendations(employee_id: int, payload: RecommendationRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    current_skills = {
        es.skill.slug: {
            "proficiency": es.proficiency,
            "confidence": es.confidence,
            "source": es.source,
        }
        for es in employee.skills
    }

    resources = db.query(LearningResource).filter(LearningResource.skill_slug == payload.target_skill.lower()).all()
    recommendation = build_learning_path(
        current_skills,
        payload.target_skill,
        payload.timeline_weeks,
        resources=[
            {
                "title": r.title,
                "url": r.url,
                "type": r.type,
                "difficulty": r.difficulty,
            }
            for r in resources
        ],
    )
    return {
        "employee_id": employee_id,
        "personalized": True,
        "analysis": recommendation,
    }
