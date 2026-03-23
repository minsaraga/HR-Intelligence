from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    geography = Column(String, nullable=False)
    career_stage = Column(String, nullable=False)

    skills = relationship("EmployeeSkill", back_populates="employee", cascade="all, delete-orphan")
    certifications = relationship("EmployeeCertification", back_populates="employee", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)


class EmployeeSkill(Base):
    __tablename__ = "employee_skills"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    proficiency = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
    source = Column(String, nullable=False)

    employee = relationship("Employee", back_populates="skills")
    skill = relationship("Skill")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    issuer = Column(String, nullable=False)


class CertificationSkillMap(Base):
    __tablename__ = "certification_skill_map"

    id = Column(Integer, primary_key=True)
    certification_id = Column(Integer, ForeignKey("certifications.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    weight = Column(Float, nullable=False)

    certification = relationship("Certification")
    skill = relationship("Skill")


class EmployeeCertification(Base):
    __tablename__ = "employee_certifications"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    certification_id = Column(Integer, ForeignKey("certifications.id"), nullable=False)

    employee = relationship("Employee", back_populates="certifications")
    certification = relationship("Certification")


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    skill_slug = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
