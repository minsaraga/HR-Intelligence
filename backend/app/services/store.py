from typing import Dict, List

employees: Dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Ava Sharma",
        "role": "Software Engineer",
        "geography": "India",
        "career_stage": "Mid",
        "skills": {
            "python": {"proficiency": 4, "confidence": 0.9, "source": "seed"},
            "sql": {"proficiency": 3, "confidence": 0.8, "source": "seed"},
        },
        "certifications": []
    }
}

certification_skill_map: Dict[str, List[dict]] = {
    "aws-certified-solutions-architect-associate": [
        {"skill": "aws", "weight": 0.9},
        {"skill": "cloud-architecture", "weight": 0.8},
        {"skill": "iam", "weight": 0.6},
    ],
    "azure-fundamentals": [
        {"skill": "azure", "weight": 0.9},
        {"skill": "cloud-fundamentals", "weight": 0.7},
    ],
}

learning_resources: Dict[str, List[dict]] = {
    "aws": [
        {
            "title": "AWS Cloud Practitioner Essentials (free)",
            "url": "https://explore.skillbuilder.aws/learn",
            "type": "course",
            "difficulty": "beginner",
        },
        {
            "title": "AWS in 100 Seconds",
            "url": "https://www.youtube.com/watch?v=ulprqHHWlng",
            "type": "video",
            "difficulty": "beginner",
        },
        {
            "title": "AWS Well-Architected Framework",
            "url": "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html",
            "type": "docs",
            "difficulty": "intermediate",
        },
    ],
    "python": [
        {
            "title": "FastAPI docs",
            "url": "https://fastapi.tiangolo.com/",
            "type": "docs",
            "difficulty": "intermediate",
        }
    ]
}
