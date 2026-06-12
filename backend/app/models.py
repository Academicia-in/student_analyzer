from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class StudentMarks(Base):
    __tablename__ = "student_marks"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_no = Column(String)
    subject_code = Column(String)

    co1 = Column(Float)
    co2 = Column(Float)
    co3 = Column(Float)
    co4 = Column(Float)
    co5 = Column(Float)

    total = Column(Float)

    status = Column(String, default="AUTO")  # AUTO / REVIEW
    errors = Column(String)