from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from database import Base, engine, get_db
from models import User, Feedback
from schemas import UserSignup, UserLogin, UserOut, FeedbackCreate
from auth import hash_password, verify_password, ADMIN_SIGNUP_CODE
from models import User, Feedback, Complaint, Notification, Announcement
from schemas import (
    UserSignup,
    UserLogin,
    UserOut,
    FeedbackCreate,
    ComplaintCreate,
    ComplaintUpdate,
    UserCreateByAdmin,
    UserUpdateByAdmin,
    AnnouncementCreate,
    FeedbackReviewUpdate,
)

app = FastAPI(title="Campus Pulse API")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


POSITIVE_WORDS = {
    "good", "great", "excellent", "clean", "helpful", "satisfied",
    "useful", "nice", "best", "improved", "amazing", "on time"
}

NEGATIVE_WORDS = {
    "bad", "poor", "slow", "crowded", "worst", "dirty",
    "problem", "late", "average", "need improvement", "delay"
}


def analyze_sentiment(comment: str) -> str:
    text = (comment or "").lower()

    positive_score = sum(1 for word in POSITIVE_WORDS if word in text)
    negative_score = sum(1 for word in NEGATIVE_WORDS if word in text)

    if positive_score > negative_score:
        return "Positive"
    elif negative_score > positive_score:
        return "Negative"
    return "Neutral"


@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc()).all()

    return [
        {
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "role": u.role,
            "department": getattr(u, "department", None),
        }
        for u in users
    ]

@app.post("/admin/users")
def create_user_by_admin(payload: UserCreateByAdmin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = payload.role.lower().strip()
    if role not in ["admin", "student", "teacher"]:
         raise HTTPException(status_code=400, detail="Invalid role")

    if role == "admin":
        if not payload.admin_unique_id or payload.admin_unique_id.strip() != ADMIN_SIGNUP_CODE:
            raise HTTPException(status_code=403, detail="Invalid admin unique ID")

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        password=hash_password(payload.password),
        role=role,
        department=payload.department,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@app.put("/users/{user_id}")
def update_user(user_id: int, payload: UserUpdateByAdmin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = payload.role.lower().strip()
    if role not in ["admin", "student"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user.role = role
    user.department = payload.department
    db.commit()
    db.refresh(user)

    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}



@app.get("/")
def home():
    return {"message": "Campus Pulse API is running"}


# ---------------- AUTH ----------------

@app.post("/signup", response_model=UserOut)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = user.role.lower().strip()

    if role not in ["admin", "student", "teacher"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    if role == "admin":
        if not user.admin_unique_id or user.admin_unique_id.strip() != ADMIN_SIGNUP_CODE:
            raise HTTPException(status_code=403, detail="Invalid admin unique ID")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role=role,
        department=user.department
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "full_name": db_user.full_name,
            "email": db_user.email,
            "role": db_user.role
        }
    }


# ---------------- FEEDBACK ----------------

@app.post("/submit-feedback")
def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(feedback.comment)

    new_feedback = Feedback(
        student_email=feedback.student_email,
        academic_year=feedback.academic_year,
        major=feedback.major,
        facility_rated=feedback.facility_rated,
        satisfaction_score=feedback.satisfaction_score,
        comment=feedback.comment,
        timestamp=datetime.now().strftime("%Y-%m-%d"),
        sentiment=sentiment,
        status="New",
        teacher_remark="",
        assigned_teacher=""
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return {"message": "Feedback submitted successfully"}


@app.get("/feedback")
def get_all_feedback(db: Session = Depends(get_db)):
    records = db.query(Feedback).all()

    return [
        {
            "id": item.id,
            "student_email": item.student_email,
            "academic_year": item.academic_year,
            "major": item.major,
            "facility_rated": item.facility_rated,
            "satisfaction_score": item.satisfaction_score,
            "comment": item.comment,
            "timestamp": item.timestamp,
            "sentiment": item.sentiment or analyze_sentiment(item.comment),
            "status": item.status,
            "teacher_remark": item.teacher_remark,
            "assigned_teacher": item.assigned_teacher,
        }
        for item in records
    ]


@app.get("/my-feedback")
def get_my_feedback(student_email: str, db: Session = Depends(get_db)):
    records = (
        db.query(Feedback)
        .filter(Feedback.student_email == student_email)
        .order_by(Feedback.id.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "student_email": item.student_email,
            "academic_year": item.academic_year,
            "major": item.major,
            "facility_rated": item.facility_rated,
            "satisfaction_score": item.satisfaction_score,
            "comment": item.comment,
            "timestamp": item.timestamp,
            "sentiment": item.sentiment or analyze_sentiment(item.comment),
            "status": item.status,
            "teacher_remark": item.teacher_remark,
            "assigned_teacher": item.assigned_teacher,
        }
        for item in records
    ]

@app.put("/feedback/{feedback_id}/review")
def review_feedback(feedback_id: int, payload: FeedbackReviewUpdate, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    allowed_status = ["New", "Reviewed", "Action Taken", "Escalated"]
    if payload.status not in allowed_status:
        raise HTTPException(status_code=400, detail="Invalid feedback status")

    feedback.status = payload.status
    feedback.teacher_remark = payload.teacher_remark or ""
    feedback.assigned_teacher = payload.assigned_teacher or feedback.assigned_teacher

    db.commit()
    db.refresh(feedback)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notification = Notification(
        user_email=feedback.student_email,
        title="Feedback Reviewed",
        message=f"Your feedback on '{feedback.facility_rated}' is now marked as '{feedback.status}'.",
        is_read="No",
        created_at=now
    )
    db.add(notification)
    db.commit()

    return {"message": "Feedback reviewed successfully"}


# ---------------- DASHBOARD ----------------

@app.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    records = db.query(Feedback).all()

    if not records:
        return {
            "overall_average_satisfaction": 0,
            "highest_rated_facility": "N/A",
            "highest_rated_score": 0,
            "lowest_rated_facility": "N/A",
            "lowest_rated_score": 0,
            "total_feedback": 0
        }

    total_feedback = len(records)
    overall_avg = round(sum(r.satisfaction_score for r in records) / total_feedback, 2)

    facility_map = {}
    for r in records:
        facility_map.setdefault(r.facility_rated, []).append(r.satisfaction_score)

    facility_avg = {
        facility: round(sum(scores) / len(scores), 2)
        for facility, scores in facility_map.items()
    }

    highest_rated_facility = max(facility_avg, key=facility_avg.get)
    lowest_rated_facility = min(facility_avg, key=facility_avg.get)

    return {
        "overall_average_satisfaction": overall_avg,
        "highest_rated_facility": highest_rated_facility,
        "highest_rated_score": facility_avg[highest_rated_facility],
        "lowest_rated_facility": lowest_rated_facility,
        "lowest_rated_score": facility_avg[lowest_rated_facility],
        "total_feedback": total_feedback
    }


@app.get("/facility-stats")
def get_facility_stats(db: Session = Depends(get_db)):
    data = (
        db.query(
            Feedback.facility_rated,
            func.avg(Feedback.satisfaction_score).label("avg_score")
        )
        .group_by(Feedback.facility_rated)
        .all()
    )

    return [
        {
            "facility_rated": row[0],
            "satisfaction_score": round(float(row[1]), 2)
        }
        for row in data
    ]


@app.get("/year-stats")
def get_year_stats(db: Session = Depends(get_db)):
    data = (
        db.query(
            Feedback.academic_year,
            func.avg(Feedback.satisfaction_score).label("avg_score")
        )
        .group_by(Feedback.academic_year)
        .all()
    )

    return [
        {
            "academic_year": row[0],
            "satisfaction_score": round(float(row[1]), 2)
        }
        for row in data
    ]


@app.get("/sentiment-stats")
def get_sentiment_stats(db: Session = Depends(get_db)):
    records = db.query(Feedback).all()

    counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for r in records:
        sentiment = analyze_sentiment(r.comment)
        counts[sentiment] += 1

    return [
        {"sentiment": key, "count": value}
        for key, value in counts.items()
    ]


@app.get("/recent-comments")
def get_recent_comments(db: Session = Depends(get_db)):
    records = (
        db.query(Feedback)
        .order_by(Feedback.id.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "student_email": r.student_email,
            "facility_rated": r.facility_rated,
            "comment": r.comment,
            "sentiment": analyze_sentiment(r.comment),
            "timestamp": r.timestamp
        }
        for r in records
    ]


@app.get("/filtered-feedback")
def get_filtered_feedback(
    facility: str | None = Query(default=None),
    academic_year: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Feedback)

    if facility:
        query = query.filter(Feedback.facility_rated == facility)

    if academic_year:
        query = query.filter(Feedback.academic_year == academic_year)

    records = query.all()

    result = []
    for r in records:
        row = {
            "id": r.id,
            "student_email": r.student_email,
            "academic_year": r.academic_year,
            "major": r.major,
            "facility_rated": r.facility_rated,
            "satisfaction_score": r.satisfaction_score,
            "comment": r.comment,
            "timestamp": r.timestamp,
            "sentiment": analyze_sentiment(r.comment)
        }

        if search:
            search_lower = search.lower()
            text = " ".join([
                str(row["student_email"]),
                str(row["academic_year"]),
                str(row["major"]),
                str(row["facility_rated"]),
                str(row["comment"])
            ]).lower()

            if search_lower not in text:
                continue

        result.append(row)

    return result

@app.post("/submit-complaint")
def submit_complaint(complaint: ComplaintCreate, db: Session = Depends(get_db)):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_complaint = Complaint(
        student_email=complaint.student_email,
        title=complaint.title,
        description=complaint.description,
        category=complaint.category,
        priority=complaint.priority,
        status="Open",
        admin_remark="",
        created_at=now,
        updated_at=now
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    new_notification = Notification(
        user_email=complaint.student_email,
        title="Complaint Submitted",
        message=f"Your complaint '{complaint.title}' has been submitted successfully.",
        is_read="No",
        created_at=now
    )
    db.add(new_notification)
    db.commit()

    return {"message": "Complaint submitted successfully"}

@app.get("/my-complaints")
def get_my_complaints(student_email: str, db: Session = Depends(get_db)):
    complaints = (
        db.query(Complaint)
        .filter(Complaint.student_email == student_email)
        .order_by(Complaint.id.desc())
        .all()
    )

    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "category": c.category,
            "priority": c.priority,
            "status": c.status,
            "admin_remark": c.admin_remark,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        for c in complaints
    ]

@app.get("/complaints")
def get_all_complaints(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).order_by(Complaint.id.desc()).all()

    return [
        {
            "id": c.id,
            "student_email": c.student_email,
            "title": c.title,
            "description": c.description,
            "category": c.category,
            "priority": c.priority,
            "status": c.status,
            "admin_remark": c.admin_remark,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        for c in complaints
    ]

@app.put("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, payload: ComplaintUpdate, db: Session = Depends(get_db)):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    complaint.status = payload.status
    complaint.admin_remark = payload.admin_remark or ""
    complaint.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.commit()
    db.refresh(complaint)

    notification = Notification(
        user_email=complaint.student_email,
        title="Complaint Updated",
        message=f"Your complaint '{complaint.title}' status is now '{complaint.status}'.",
        is_read="No",
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.add(notification)
    db.commit()

    return {"message": "Complaint updated successfully"}

@app.get("/complaint-analytics")
def complaint_analytics(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).all()

    status_counts = {"Open": 0, "In Review": 0, "Resolved": 0, "Rejected": 0}
    priority_counts = {"Low": 0, "Medium": 0, "High": 0}
    category_counts = {}

    for c in complaints:
        if c.status in status_counts:
            status_counts[c.status] += 1

        if c.priority in priority_counts:
            priority_counts[c.priority] += 1

        category_counts[c.category] = category_counts.get(c.category, 0) + 1

    return {
        "status_counts": [{"status": k, "count": v} for k, v in status_counts.items()],
        "priority_counts": [{"priority": k, "count": v} for k, v in priority_counts.items()],
        "category_counts": [{"category": k, "count": v} for k, v in category_counts.items()],
    }

@app.get("/notifications")
def get_notifications(user_email: str, db: Session = Depends(get_db)):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_email == user_email)
        .order_by(Notification.id.desc())
        .all()
    )

    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifications
    ]

@app.get("/department-feedback-stats")
def department_feedback_stats(db: Session = Depends(get_db)):
    users = db.query(User).all()
    feedback = db.query(Feedback).all()

    email_to_department = {
        u.email: (u.department if getattr(u, "department", None) else "Unassigned")
        for u in users
    }

    dept_scores = {}
    for item in feedback:
        dept = email_to_department.get(item.student_email, "Unassigned")
        dept_scores.setdefault(dept, []).append(item.satisfaction_score)

    return [
        {
            "department": dept,
            "avg_score": round(sum(scores) / len(scores), 2),
            "count": len(scores),
        }
        for dept, scores in dept_scores.items()
    ]

@app.get("/department-complaint-stats")
def department_complaint_stats(db: Session = Depends(get_db)):
    users = db.query(User).all()
    complaints = db.query(Complaint).all()

    email_to_department = {
        u.email: (u.department if getattr(u, "department", None) else "Unassigned")
        for u in users
    }

    dept_counts = {}
    for item in complaints:
        dept = email_to_department.get(item.student_email, "Unassigned")
        dept_counts[dept] = dept_counts.get(dept, 0) + 1

    return [
        {"department": dept, "count": count}
        for dept, count in dept_counts.items()
    ]

@app.post("/announcements")
def create_announcement(payload: AnnouncementCreate, db: Session = Depends(get_db)):
    role = payload.target_role.lower().strip()
    if role not in ["student", "admin", "all"]:
        raise HTTPException(status_code=400, detail="Invalid target role")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_announcement = Announcement(
        title=payload.title,
        message=payload.message,
        target_role=role,
        created_at=now
    )
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)

    return {"message": "Announcement created successfully"}

@app.get("/announcements")
def get_announcements(target_role: str = "all", db: Session = Depends(get_db)):
    role = target_role.lower().strip()

    announcements = db.query(Announcement).order_by(Announcement.id.desc()).all()

    filtered = []
    for item in announcements:
        if item.target_role == "all" or item.target_role == role:
            filtered.append({
                "id": item.id,
                "title": item.title,
                "message": item.message,
                "target_role": item.target_role,
                "created_at": item.created_at,
            })

    return filtered

@app.delete("/announcements/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    db.delete(announcement)
    db.commit()

    return {"message": "Announcement deleted successfully"}

@app.get("/facility-issue-tracker")
def facility_issue_tracker(db: Session = Depends(get_db)):
    feedback_records = db.query(Feedback).all()

    facility_map = {}

    for item in feedback_records:
        facility = item.facility_rated

        if facility not in facility_map:
            facility_map[facility] = {
                "facility": facility,
                "total_feedback": 0,
                "avg_score_sum": 0,
                "negative_count": 0,
                "reviewed_count": 0,
                "action_taken_count": 0,
                "escalated_count": 0,
            }

        facility_map[facility]["total_feedback"] += 1
        facility_map[facility]["avg_score_sum"] += item.satisfaction_score

        sentiment = item.sentiment or analyze_sentiment(item.comment)
        if sentiment == "Negative":
            facility_map[facility]["negative_count"] += 1

        if item.status == "Reviewed":
            facility_map[facility]["reviewed_count"] += 1
        elif item.status == "Action Taken":
            facility_map[facility]["action_taken_count"] += 1
        elif item.status == "Escalated":
            facility_map[facility]["escalated_count"] += 1

    result = []
    for facility, values in facility_map.items():
        avg_score = round(values["avg_score_sum"] / values["total_feedback"], 2)

        if avg_score < 2.5 or values["negative_count"] >= 3:
            health = "Critical"
        elif avg_score < 3.5 or values["negative_count"] >= 1:
            health = "Needs Attention"
        else:
            health = "Stable"

        result.append({
            "facility": facility,
            "total_feedback": values["total_feedback"],
            "avg_score": avg_score,
            "negative_count": values["negative_count"],
            "reviewed_count": values["reviewed_count"],
            "action_taken_count": values["action_taken_count"],
            "escalated_count": values["escalated_count"],
            "health": health,
        })

    return result

@app.get("/admin/facility-management")
def admin_facility_management(db: Session = Depends(get_db)):
    feedback_records = db.query(Feedback).all()

    facility_map = {}

    for item in feedback_records:
        facility = item.facility_rated

        if facility not in facility_map:
            facility_map[facility] = {
                "facility": facility,
                "total_feedback": 0,
                "score_sum": 0,
                "negative_count": 0,
                "new_count": 0,
                "reviewed_count": 0,
                "action_taken_count": 0,
                "escalated_count": 0,
            }

        facility_map[facility]["total_feedback"] += 1
        facility_map[facility]["score_sum"] += item.satisfaction_score

        sentiment = item.sentiment or analyze_sentiment(item.comment)
        if sentiment == "Negative":
            facility_map[facility]["negative_count"] += 1

        status = item.status or "New"
        if status == "New":
            facility_map[facility]["new_count"] += 1
        elif status == "Reviewed":
            facility_map[facility]["reviewed_count"] += 1
        elif status == "Action Taken":
            facility_map[facility]["action_taken_count"] += 1
        elif status == "Escalated":
            facility_map[facility]["escalated_count"] += 1

    result = []
    for _, values in facility_map.items():
        avg_score = round(values["score_sum"] / values["total_feedback"], 2)

        if avg_score < 2.5 or values["negative_count"] >= 3:
            health = "Critical"
        elif avg_score < 3.5 or values["negative_count"] >= 1:
            health = "Needs Attention"
        else:
            health = "Stable"

        result.append({
            "facility": values["facility"],
            "total_feedback": values["total_feedback"],
            "avg_score": avg_score,
            "negative_count": values["negative_count"],
            "new_count": values["new_count"],
            "reviewed_count": values["reviewed_count"],
            "action_taken_count": values["action_taken_count"],
            "escalated_count": values["escalated_count"],
            "health": health,
        })

    return result