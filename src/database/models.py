from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    func,
    Integer,
    String,
    Text,
    Numeric
)
from sqlalchemy.orm import declarative_base, relationship
from database.connection import engine
from utils.logger import get_logger

Base = declarative_base()

class Source(Base):
    __tablename__ = "sources"
    source_id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String(100), nullable=False, unique=True)

    jobs = relationship("Job", back_populates="source")

class Company(Base):
    __tablename__ = "companies"
    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False, unique=True)

    jobs = relationship("Job", back_populates="company")


class Location(Base):
    __tablename__ = "locations"
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    state = Column(String(100))
    county = Column(String(100))
    city = Column(String(100))
    display_name = Column(String(255), unique=True, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    jobs = relationship("Job", back_populates="location") 

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_tag = Column(String(100), unique=True, nullable =False)
    category_name = Column(String(255), nullable=False)

    jobs = relationship("Job", back_populates="category")

class Job(Base):
    __tablename__ = "jobs"
    extraction_timestamp = Column(
    DateTime,
    nullable=False,
    server_default=func.current_timestamp(),
)
    job_id = Column(String(20), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    salary_min = Column(Numeric(10,2))
    salary_max = Column(Numeric(10,2))
    salary_average = Column(Numeric(10,2))
    salary_predicted = Column(Boolean)
    contract_type = Column(String(50))
    contract_time = Column(String(50))
    created_date = Column(DateTime)
    redirect_url = Column(Text)
    adref = Column(Text)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.location_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.source_id"), nullable=False)

    company = relationship("Company", back_populates="jobs" )
    location = relationship("Location", back_populates="jobs")
    category = relationship("Category", back_populates="jobs")
    source = relationship("Source", back_populates="jobs")










