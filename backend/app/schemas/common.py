from pydantic import BaseModel
from typing import List, Dict


class SkillUpdate(BaseModel):
    skill: str
    proficiency: int
    confidence: float
    source: str


class EmployeeOut(BaseModel):
    id: int
    name: str
    role: str
    geography: str
    career_stage: str
    skills: Dict[str, dict]
    certifications: List[str]
