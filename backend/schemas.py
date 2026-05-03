from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str
    department: str | None = None
    admin_unique_id: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    department: str | None = None

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    student_email: EmailStr
    academic_year: str
    major: str
    facility_rated: str
    satisfaction_score: int
    comment: str


class ComplaintCreate(BaseModel):
    student_email: EmailStr
    title: str
    description: str
    category: str
    priority: str


class ComplaintUpdate(BaseModel):
    status: str
    admin_remark: str | None = None

class UserCreateByAdmin(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str
    department: str | None = None
    admin_unique_id: str | None = None


class UserUpdateByAdmin(BaseModel):
    role: str
    department: str | None = None

class AnnouncementCreate(BaseModel):
    title: str
    message: str
    target_role: str

class FeedbackReviewUpdate(BaseModel):
    status: str
    teacher_remark: str | None = None
    assigned_teacher: str | None = None