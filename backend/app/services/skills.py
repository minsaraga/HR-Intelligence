import io
import re
from typing import Dict, List

from docx import Document
from pypdf import PdfReader

SKILL_PATTERNS: Dict[str, List[str]] = {
    "aws": ["aws", "amazon web services", "amazon q", "bedrock", "ec2", "s3", "lambda", "cloudformation"],
    "azure": ["azure", "resource groups", "azure vms", "container apps", "azure storage"],
    "python": ["python", "fastapi", "pandas", "numpy"],
    "java": ["java", "core java", "junit", "jdbc"],
    "javascript": ["javascript", "reactjs", "node.js"],
    "sql": ["sql", "database systems", "relational dbs"],
    "docker": ["docker", "docker compose", "containers", "kubernetes", "k8s"],
    "spring-boot": ["spring boot", "maven"],
    "langchain": ["langchain"],
    "langgraph": ["langgraph"],
    "langflow": ["langflow"],
    "rasa": ["rasa", "rasa chatbot"],
    "firebase": ["firebase"],
    "php": ["php"],
    "flutter": ["flutter"],
    "mysql": ["mysql"],
    "oracle": ["oracle"],
    "genai": ["genai", "generative ai", "ai prototyping"],
    "ai-agents": ["ai agents", "agentic workflows", "agentic frameworks"],
    "rest-apis": ["rest api", "restful applications", "api development"],
    "cloud-architecture": ["cloud architecture", "scalable solutions", "system resilience", "distributed systems"],
    "iam": ["iam", "identity and access management", "roles and policies"],
}

SECTION_WEIGHTS = {
    "profile": 0.7,
    "experience": 1.6,
    "projects": 1.3,
    "skills": 1.1,
    "certifications": 0.9,
    "education": 0.5,
    "other": 0.6,
}

SECTION_HEADERS = {
    "profile": ["profile"],
    "experience": ["professional experience", "experience"],
    "projects": ["personal projects", "projects"],
    "skills": ["skills"],
    "certifications": ["certifications", "certification"],
    "education": ["education"],
}


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    parts = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        parts.append(txt)
    return "\n".join(parts)


def _extract_docx_text(content: bytes) -> str:
    doc = Document(io.BytesIO(content))
    return "\n".join(p.text for p in doc.paragraphs if p.text)


def extract_text_from_file(filename: str, content: bytes) -> str:
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        return _extract_pdf_text(content)
    if name.endswith(".docx"):
        return _extract_docx_text(content)
    return content.decode("utf-8", errors="ignore")


def _detect_section(line: str, current: str) -> str:
    ll = line.lower().strip().rstrip(':')
    for section, headers in SECTION_HEADERS.items():
        if ll in headers:
            return section
    return current


def _split_into_sections(text: str) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {k: [] for k in SECTION_WEIGHTS.keys()}
    current = "other"
    for raw_line in re.split(r"\n+", text):
        line = raw_line.strip()
        if not line:
            continue
        current = _detect_section(line, current)
        sections.setdefault(current, []).append(line)
    return {k: "\n".join(v) for k, v in sections.items() if v}


def _count_pattern(text_lower: str, pattern: str) -> int:
    return len(re.findall(rf"\b{re.escape(pattern.lower())}\b", text_lower))


def _years_near_skill(text_lower: str, pattern: str) -> int:
    out = 0
    regexes = [
        rf"(\d{{1,2}})\+?\s*(?:years|yrs).*?{re.escape(pattern.lower())}",
        rf"{re.escape(pattern.lower())}.*?(\d{{1,2}})\+?\s*(?:years|yrs)",
    ]
    for rgx in regexes:
        for m in re.findall(rgx, text_lower):
            try:
                out = max(out, int(m))
            except ValueError:
                pass
    return out


def _proficiency_from_score(score: float) -> int:
    if score < 1.0:
        return 1
    if score < 2.2:
        return 2
    if score < 4.0:
        return 3
    if score < 6.0:
        return 4
    return 5


def _confidence(weighted_hits: float, evidence_count: int, years: int) -> float:
    conf = 0.35 + (weighted_hits * 0.05) + (evidence_count * 0.04) + (min(years, 8) * 0.02)
    return round(max(0.4, min(0.95, conf)), 2)


def extract_skills_from_text(text: str):
    raw_text = text or ""
    sections = _split_into_sections(raw_text)
    snippets = re.split(r"(?<=[.!?•\-])\s+", raw_text)

    found = []
    for skill, patterns in SKILL_PATTERNS.items():
        weighted_hits = 0.0
        evidence = []
        years = 0
        section_presence = set()
        explicit_skill_list_bonus = 0.0
        experience_bonus = 0.0
        project_bonus = 0.0

        for section_name, section_text in sections.items():
            lower = section_text.lower()
            hits_in_section = 0

            for pattern in patterns:
                count = _count_pattern(lower, pattern)
                hits_in_section += count
                years = max(years, _years_near_skill(lower, pattern))
                if count > 0:
                    for s in snippets:
                        if pattern.lower() in s.lower() and s[:180] not in evidence and len(evidence) < 4:
                            evidence.append(s[:180])

            if hits_in_section > 0:
                weight = SECTION_WEIGHTS.get(section_name, 0.6)
                weighted_hits += min(hits_in_section, 3) * weight
                section_presence.add(section_name)

                if section_name == "skills":
                    explicit_skill_list_bonus += 0.8
                if section_name == "experience":
                    experience_bonus += 0.9
                if section_name == "projects":
                    project_bonus += 0.6

        if weighted_hits == 0:
            continue

        breadth_bonus = 0.35 * len(section_presence)
        years_bonus = min(1.5, years * 0.35)
        score = weighted_hits + explicit_skill_list_bonus + experience_bonus + project_bonus + breadth_bonus + years_bonus

        found.append({
            "skill": skill,
            "proficiency": _proficiency_from_score(score),
            "confidence": _confidence(weighted_hits, len(evidence), years),
            "source": "cv_extraction"
        })

    found.sort(key=lambda x: (-x["proficiency"], -x["confidence"], x["skill"]))
    return found


def extract_skills_from_file(filename: str, content: bytes):
    text = extract_text_from_file(filename, content)
    return extract_skills_from_text(text)
