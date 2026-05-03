from sqlalchemy import Column, Integer, String, Text
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    department = Column(String(100), nullable=True)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String(120), nullable=False)
    academic_year = Column(String(50), nullable=False)
    major = Column(String(50), nullable=False)
    facility_rated = Column(String(100), nullable=False)
    satisfaction_score = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    timestamp = Column(String(30), nullable=False)

    sentiment = Column(String(20), nullable=True)
    status = Column(String(30), nullable=False, default="New")
    teacher_remark = Column(Text, nullable=True)
    assigned_teacher = Column(String(120), nullable=True)


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String(120), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    priority = Column(String(20), nullable=False)
    status = Column(String(30), nullable=False, default="Open")
    admin_remark = Column(Text, nullable=True)
    created_at = Column(String(30), nullable=False)
    updated_at = Column(String(30), nullable=False)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(120), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(String(10), nullable=False, default="No")
    created_at = Column(String(30), nullable=False)

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    target_role = Column(String(20), nullable=False)   # admin / student / all
    created_at = Column(String(30), nullable=False)