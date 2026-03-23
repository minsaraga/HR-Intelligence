from pydantic import BaseModel


class EmployeeCreateRequest(BaseModel):
    name: str
    role: str
    geography: str
    career_stage: str


class CertificationUpdateRequest(BaseModel):
    certification_slug: str


class RecommendationRequest(BaseModel):
    target_skill: str
    timeline_weeks: int = 6
