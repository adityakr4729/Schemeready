from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Text, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), default="General")
    state = Column(String(100), nullable=False)
    district = Column(String(100), default="")
    occupation = Column(String(100), default="Student")
    is_student = Column(Boolean, default=True)
    education_level = Column(String(100), default="B.Tech")
    annual_family_income = Column(Float, nullable=False)
    area_type = Column(String(20), default="Urban") # Rural / Urban
    category_type = Column(String(50), default="General") # General / OBC / SC / ST / EWS
    is_demo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_documents = relationship("UserDocument", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")

class Scheme(Base):
    __tablename__ = "schemes"

    scheme_id = Column(String(50), primary_key=True, index=True)
    scheme_name = Column(String(255), nullable=False)
    ministry = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    state = Column(String(100), nullable=False, default="All India")
    category = Column(String(100), nullable=False, default="Scholarship")
    description = Column(Text, nullable=False)
    benefits = Column(Text, nullable=False)
    deadline = Column(String(50), nullable=True) # ISO format YYYY-MM-DD
    renewal_required = Column(Boolean, default=False)
    renewal_information = Column(Text, default="")
    application_url = Column(String(500), nullable=False)
    official_source_url = Column(String(500), nullable=False)
    last_updated = Column(String(50), default="2026-08-01")

    eligibility_rules = relationship("EligibilityRule", back_populates="scheme", cascade="all, delete-orphan")
    required_documents = relationship("RequiredDocument", back_populates="scheme", cascade="all, delete-orphan")

class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False)
    field = Column(String(100), nullable=False) # e.g. age, annual_family_income, is_student, state
    operator = Column(String(20), nullable=False) # gte, lte, eq, in
    value = Column(JSON, nullable=False) # target threshold value or list
    label = Column(String(255), nullable=False)
    failure_reason = Column(Text, nullable=False)

    scheme = relationship("Scheme", back_populates="eligibility_rules")

class RequiredDocument(Base):
    __tablename__ = "required_documents"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False)
    doc_id = Column(String(50), nullable=False) # e.g. DOC_AADHAAR, DOC_INCOME
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    mandatory = Column(Boolean, default=True)

    scheme = relationship("Scheme", back_populates="required_documents")

class UserDocument(Base):
    __tablename__ = "user_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doc_id = Column(String(50), nullable=False) # e.g. DOC_INCOME
    doc_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)
    status = Column(String(50), default="Available") # Available, Missing, Verified
    extracted_data = Column(JSON, nullable=True)
    verification_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user_documents")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False)
    status = Column(String(50), default="In Progress") # Draft, Ready to Apply, Applied
    readiness_score = Column(Float, default=0.0)
    applied_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="applications")

class Renewal(Base):
    __tablename__ = "renewals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheme_id = Column(String(50), ForeignKey("schemes.scheme_id"), nullable=False)
    renewal_due_date = Column(String(50), nullable=False)
    status = Column(String(50), default="Upcoming") # Upcoming, Complete, Overdue
    notes = Column(Text, nullable=True)
