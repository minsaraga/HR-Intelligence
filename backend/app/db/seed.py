from sqlalchemy.orm import Session
from app.db.models import Employee, Skill, Certification, CertificationSkillMap, LearningResource, EmployeeSkill


BASE_EMPLOYEES = [
    ("Ava Sharma", "Software Engineer", "India", "Mid", [("python", 4, 0.9, "seed"), ("sql", 3, 0.8, "seed")]),
    ("John Chen", "Senior DevOps Engineer", "Singapore", "Senior", [("docker", 5, 0.95, "seed"), ("aws", 4, 0.85, "seed")]),
    ("Maria Garcia", "Cloud Architect", "US", "Lead", [("aws", 5, 0.95, "seed"), ("cloud-architecture", 5, 0.9, "seed")]),
    ("Raj Patel", "Junior Developer", "India", "Junior", [("javascript", 2, 0.7, "seed"), ("python", 2, 0.65, "seed")]),
    ("Sarah Johnson", "AI Engineer", "UK", "Mid", [("python", 4, 0.9, "seed"), ("genai", 3, 0.8, "seed"), ("langchain", 3, 0.75, "seed")]),
    ("Ahmed Hassan", "Backend Developer", "UAE", "Mid", [("java", 4, 0.85, "seed"), ("spring-boot", 4, 0.8, "seed"), ("sql", 3, 0.75, "seed")]),
    ("Emily Wong", "Full Stack Developer", "Canada", "Senior", [("javascript", 5, 0.9, "seed"), ("python", 4, 0.85, "seed"), ("rest-apis", 4, 0.8, "seed")]),
    ("Carlos Silva", "Data Engineer", "Brazil", "Mid", [("python", 4, 0.85, "seed"), ("sql", 5, 0.95, "seed"), ("aws", 3, 0.75, "seed")]),
    ("Lisa Anderson", "Security Engineer", "US", "Senior", [("iam", 5, 0.95, "seed"), ("aws", 4, 0.85, "seed"), ("cloud-architecture", 4, 0.8, "seed")]),
    ("Yuki Tanaka", "Mobile Developer", "Japan", "Mid", [("flutter", 4, 0.9, "seed"), ("firebase", 3, 0.8, "seed"), ("rest-apis", 3, 0.75, "seed")]),
]

BASE_SKILLS = [
    ("aws", "AWS", "cloud"),
    ("azure", "Azure", "cloud"),
    ("python", "Python", "language"),
    ("java", "Java", "language"),
    ("javascript", "JavaScript", "language"),
    ("sql", "SQL", "database"),
    ("docker", "Docker", "devops"),
    ("kubernetes", "Kubernetes", "devops"),
    ("terraform", "Terraform", "devops"),
    ("spring-boot", "Spring Boot", "framework"),
    ("langchain", "LangChain", "ai"),
    ("langgraph", "LangGraph", "ai"),
    ("langflow", "Langflow", "ai"),
    ("rasa", "Rasa", "ai"),
    ("firebase", "Firebase", "cloud"),
    ("php", "PHP", "language"),
    ("flutter", "Flutter", "framework"),
    ("mysql", "MySQL", "database"),
    ("oracle", "Oracle", "database"),
    ("genai", "GenAI", "ai"),
    ("ai-agents", "AI Agents", "ai"),
    ("rest-apis", "REST APIs", "backend"),
    ("cloud-architecture", "Cloud Architecture", "architecture"),
    ("iam", "IAM", "security"),
]

CERTIFICATIONS = [
    ("aws-certified-solutions-architect-associate", "AWS Certified Solutions Architect Associate", "AWS"),
    ("aws-certified-developer-associate", "AWS Certified Developer Associate", "AWS"),
    ("azure-fundamentals", "Azure Fundamentals", "Microsoft"),
    ("azure-administrator", "Azure Administrator Associate", "Microsoft"),
    ("gcp-associate-cloud-engineer", "Google Cloud Associate Cloud Engineer", "Google"),
    ("cka", "Certified Kubernetes Administrator", "CNCF"),
    ("ckad", "Certified Kubernetes Application Developer", "CNCF"),
]

CERT_SKILL_MAPS = {
    "aws-certified-solutions-architect-associate": [("aws", 0.9), ("cloud-architecture", 0.8), ("iam", 0.6)],
    "aws-certified-developer-associate": [("aws", 0.9), ("rest-apis", 0.7), ("python", 0.5)],
    "azure-fundamentals": [("azure", 0.9), ("cloud-architecture", 0.6)],
    "azure-administrator": [("azure", 0.9), ("iam", 0.7), ("cloud-architecture", 0.7)],
    "gcp-associate-cloud-engineer": [("cloud-architecture", 0.8), ("iam", 0.6)],
    "cka": [("kubernetes", 0.95), ("docker", 0.7)],
    "ckad": [("kubernetes", 0.9), ("docker", 0.8)],
}

LEARNING_RESOURCES = [
    ("aws", "AWS Cloud Practitioner Essentials", "https://explore.skillbuilder.aws/learn", "course", "beginner"),
    ("aws", "AWS in 100 Seconds", "https://www.youtube.com/watch?v=ulprqHHWlng", "video", "beginner"),
    ("aws", "AWS Well-Architected Framework", "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html", "docs", "intermediate"),
    ("python", "Python Official Tutorial", "https://docs.python.org/3/tutorial/", "docs", "beginner"),
    ("python", "FastAPI Docs", "https://fastapi.tiangolo.com/", "docs", "intermediate"),
    ("docker", "Docker Getting Started", "https://docs.docker.com/get-started/", "docs", "beginner"),
    ("docker", "Docker in 100 Seconds", "https://www.youtube.com/watch?v=Gjnup-PuquQ", "video", "beginner"),
    ("kubernetes", "Kubernetes Basics", "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "docs", "beginner"),
    ("kubernetes", "Kubernetes in 100 Seconds", "https://www.youtube.com/watch?v=PziYflu8cB8", "video", "beginner"),
    ("javascript", "MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "docs", "beginner"),
    ("java", "Java Tutorial for Beginners", "https://docs.oracle.com/javase/tutorial/", "docs", "beginner"),
    ("genai", "Introduction to Generative AI", "https://www.cloudskillsboost.google/course_templates/536", "course", "beginner"),
    ("langchain", "LangChain Documentation", "https://python.langchain.com/docs/get_started/introduction", "docs", "intermediate"),
    ("azure", "Microsoft Learn Azure Fundamentals", "https://learn.microsoft.com/en-us/training/azure/", "course", "beginner"),
    ("sql", "SQL Tutorial", "https://www.w3schools.com/sql/", "docs", "beginner"),
]


def seed_db(db: Session):
    # Seed skills
    existing_skills = {s.slug for s in db.query(Skill).all()}
    for slug, name, category in BASE_SKILLS:
        if slug not in existing_skills:
            db.add(Skill(slug=slug, name=name, category=category))
    db.flush()

    # Seed certifications
    existing_certs = {c.slug for c in db.query(Certification).all()}
    for slug, name, issuer in CERTIFICATIONS:
        if slug not in existing_certs:
            db.add(Certification(slug=slug, name=name, issuer=issuer))
    db.flush()

    # Seed employees
    existing_employees = db.query(Employee).count()
    if existing_employees == 0:
        skill_by_slug = {s.slug: s for s in db.query(Skill).all()}
        for name, role, geography, career_stage, skills in BASE_EMPLOYEES:
            emp = Employee(name=name, role=role, geography=geography, career_stage=career_stage)
            db.add(emp)
            db.flush()
            for skill_slug, proficiency, confidence, source in skills:
                skill = skill_by_slug.get(skill_slug)
                if skill:
                    db.add(EmployeeSkill(
                        employee_id=emp.id,
                        skill_id=skill.id,
                        proficiency=proficiency,
                        confidence=confidence,
                        source=source
                    ))

    skill_by_slug = {s.slug: s for s in db.query(Skill).all()}
    cert_by_slug = {c.slug: c for c in db.query(Certification).all()}

    # Seed certification skill maps
    for cert_slug, mappings in CERT_SKILL_MAPS.items():
        cert = cert_by_slug.get(cert_slug)
        if not cert:
            continue
        existing = db.query(CertificationSkillMap).filter(CertificationSkillMap.certification_id == cert.id).count()
        if existing:
            continue
        for skill_slug, weight in mappings:
            skill = skill_by_slug.get(skill_slug)
            if skill:
                db.add(CertificationSkillMap(certification_id=cert.id, skill_id=skill.id, weight=weight))

    # Seed learning resources
    existing_resources = db.query(LearningResource).count()
    if existing_resources == 0:
        for skill_slug, title, url, rtype, difficulty in LEARNING_RESOURCES:
            db.add(LearningResource(skill_slug=skill_slug, title=title, url=url, type=rtype, difficulty=difficulty))

    db.commit()
