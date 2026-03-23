def build_learning_path(current_skills: dict, target_skill: str, timeline_weeks: int, resources=None):
    target_skill = target_skill.lower().strip()
    current = current_skills.get(target_skill)
    current_level = current.get("proficiency", 0) if current else 0

    gap = max(0, 4 - current_level)
    resources = resources or []

    stages = [
        "Foundation",
        "Practice",
        "Applied Project"
    ]

    plan = []
    for idx, r in enumerate(resources, start=1):
        stage = stages[min(idx - 1, len(stages) - 1)]
        plan.append({
            "week": min(idx, timeline_weeks),
            "stage": stage,
            "resource": r,
            "goal": f"Build competence in {target_skill} ({stage.lower()})"
        })

    return {
        "target_skill": target_skill,
        "current_level": current_level,
        "target_level": 4,
        "gap": gap,
        "timeline_weeks": timeline_weeks,
        "learning_path": plan,
    }
