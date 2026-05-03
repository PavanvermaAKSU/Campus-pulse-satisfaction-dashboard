# Campus Pulse satisfaction dashboard
## Role-Based Student Feedback, Complaint Intelligence, and Analytics Management System

Campus Pulse 2.0 is a smart campus feedback and complaint management platform built to improve communication, issue tracking, and data-driven decision-making inside an educational institution.

The system supports three major roles:

- **Student**
- **Teacher**
- **Admin**

Students can submit feedback and complaints, teachers can review departmental feedback and take action, and admins can monitor the whole system using dashboards, analytics, facility tracking, reports, announcements, and user management.

---

# 1. Project Overview

Campus Pulse 2.0 is designed to solve common campus management problems such as:

- students giving feedback but no one taking action
- complaints being submitted but not tracked properly
- administrators lacking a centralized analytics dashboard
- teachers not having departmental visibility into issues
- no structured announcement and notification system
- difficulty in identifying weak facilities such as hostel, canteen, lab, classroom, transport, library, etc.

This platform converts raw student opinions into actionable institutional insights.

---

# 2. Main Objectives

The main objectives of this project are:

- collect structured student feedback
- collect and manage complaints efficiently
- provide role-based access for student, teacher, and admin
- allow teachers to review feedback and add remarks
- allow admins to monitor facility health and overall trends
- visualize satisfaction, sentiment, complaint categories, and department performance
- improve accountability using review workflows and action tracking
- provide official communication through announcements and notifications

---

# 3. User Roles and Responsibilities

## 3.1 Student
Student can:

- sign up and log in
- submit feedback on campus facilities
- submit complaints
- view own feedback history
- view complaint status
- view teacher/admin remarks
- see notifications
- see announcements
- access profile page

## 3.2 Teacher
Teacher can:

- sign up and log in
- access department-specific dashboard
- review feedback submitted by students from their department
- update feedback status
- add teacher remarks
- analyze department data
- monitor facility issues
- see announcements
- see notifications

## 3.3 Admin
Admin can:

- sign up using unique admin code
- log in and access executive dashboard
- manage users
- manage complaints
- manage announcements
- monitor analytics and reports
- track facility health
- export reports
- monitor department and campus-wide trends

---

# 4. Core Features

## 4.1 Authentication System
- multi-role login/signup
- student, teacher, admin roles
- protected routes
- remember me support
- admin unique code validation

## 4.2 Feedback Management
- student can submit feedback
- feedback contains facility, score, comments, academic year, major/department
- sentiment analysis supported
- teacher can review feedback
- feedback review statuses:
  - New
  - Reviewed
  - Action Taken
  - Escalated

## 4.3 Complaint Management
- students can raise complaints
- complaints include title, description, category, priority
- admin can update complaint status
- status examples:
  - Open
  - In Review
  - Resolved
  - Rejected

## 4.4 Notifications
- students receive notifications when complaint or feedback status changes
- notifications displayed in timeline/card format

## 4.5 Announcements
- admin can create official announcements
- announcements can target:
  - student
  - teacher
  - admin
  - all
- students and teachers can view role-based announcements

## 4.6 Teacher Review Workflow
- teacher can review departmental feedback
- teacher can add remark
- teacher can update action status
- reviewed feedback becomes visible to student

## 4.7 Facility Issue Tracking
- tracks facility-wise health
- identifies stable, attention-needed, and critical facilities
- uses:
  - average rating
  - negative feedback count
  - reviewed/action status

## 4.8 Analytics and Visualization
System provides visual dashboards using React charts directly from backend data.

Charts include:
- facility ratings
- year-wise trend
- sentiment distribution
- complaint status
- complaint priority
- complaint categories
- department-wise average satisfaction
- department-wise complaint count

## 4.9 Reports
- search and filter data
- feedback reports
- complaint reports
- CSV export
- PDF export

## 4.10 User Management
Admin can:
- view all users
- search/filter users
- create new users
- update role
- update department
- delete users

---

# 5. Modules in the Project

## 5.1 Student Module
Pages:
- Student Dashboard
- Submit Feedback
- My Feedback
- Raise Complaint
- My Complaints
- Notifications
- Announcements
- Profile

## 5.2 Teacher Module
Pages:
- Teacher Dashboard
- Review Feedback
- Department Analytics
- Facility Issues
- Announcements
- Notifications

## 5.3 Admin Module
Pages:
- Executive Dashboard
- Analytics Center
- Reports
- Manage Complaints
- User Management
- Facility Management
- Announcement Management

---

# 6. Technology Stack

## Frontend
- React.js
- React Router DOM
- Axios
- React Icons
- Recharts
- jsPDF
- jspdf-autotable

## Backend
- FastAPI
- SQLAlchemy
- Passlib
- Pydantic

## Database
- SQLite for easy local development
- MySQL supported for production/advanced use

---

# 7. System Architecture

The project follows a three-layer architecture:

## 7.1 Presentation Layer
This is the frontend built using React.
It handles:
- UI
- navigation
- dashboards
- forms
- charts
- role-based pages

## 7.2 Application Layer
This is the FastAPI backend.
It handles:
- authentication
- APIs
- business logic
- sentiment logic
- review workflows
- reporting APIs

## 7.3 Data Layer
This is the database layer.
It stores:
- users
- feedback
- complaints
- notifications
- announcements

---

# 8. Database Design

## 8.1 Users Table
Stores user account details.

Fields:
- `id`
- `full_name`
- `email`
- `password`
- `role`
- `department`

## 8.2 Feedback Table
Stores student feedback.

Fields:
- `id`
- `student_email`
- `academic_year`
- `major`
- `facility_rated`
- `satisfaction_score`
- `comment`
- `timestamp`
- `sentiment`
- `status`
- `teacher_remark`
- `assigned_teacher`

## 8.3 Complaints Table
Stores student complaints.

Fields:
- `id`
- `student_email`
- `title`
- `description`
- `category`
- `priority`
- `status`
- `admin_remark`
- `created_at`
- `updated_at`

## 8.4 Notifications Table
Stores user-specific notifications.

Fields:
- `id`
- `user_email`
- `title`
- `message`
- `is_read`
- `created_at`

## 8.5 Announcements Table
Stores public announcements.

Fields:
- `id`
- `title`
- `message`
- `target_role`
- `created_at`

---

# 9. Important Functional Flows

## 9.1 Student Feedback Flow
1. Student logs in
2. Student opens feedback form
3. Student submits feedback
4. Feedback saved in database
5. Sentiment generated
6. Teacher reviews it
7. Student later sees teacher remark and status

## 9.2 Complaint Flow
1. Student raises complaint
2. Complaint stored in database
3. Admin reviews complaint
4. Admin updates complaint status
5. Notification generated for student

## 9.3 Teacher Review Flow
1. Teacher logs in
2. Teacher opens departmental feedback
3. Teacher selects feedback
4. Teacher updates review status
5. Teacher adds remark
6. Student can see the action

## 9.4 Announcement Flow
1. Admin creates announcement
2. Target role is selected
3. System stores announcement
4. Students/teachers/admins see their relevant announcements

---

# 10. Dashboard Difference

## Admin Dashboard
Admin Dashboard is a high-level summary page.  
It shows:
- total feedback
- average satisfaction
- highest/lowest rated facility
- complaint charts
- department charts
- recent comments
- recent complaints

## Analytics Page
Analytics page is for deep analysis.  
It shows:
- more charts
- trend exploration
- department-based comparison
- filtered records
- detailed insights

## Teacher Dashboard
Teacher dashboard is action-oriented.  
It shows:
- department feedback overview
- complaint visibility
- recent departmental records
- facility issue monitoring

## Student Dashboard
Student dashboard is personal activity-oriented.  
It shows:
- own feedback count
- average score
- complaints summary
- notifications
- recent records

---

# 11. API Endpoints Overview

## Authentication
- `POST /signup`
- `POST /login`

## Feedback
- `POST /submit-feedback`
- `GET /feedback`
- `GET /my-feedback`
- `PUT /feedback/{feedback_id}/review`

## Complaints
- `POST /submit-complaint`
- `GET /my-complaints`
- `GET /complaints`
- `PUT /complaints/{complaint_id}`

## Notifications
- `GET /notifications`

## Analytics
- `GET /summary`
- `GET /facility-stats`
- `GET /year-stats`
- `GET /sentiment-stats`
- `GET /complaint-analytics`
- `GET /department-feedback-stats`
- `GET /department-complaint-stats`
- `GET /facility-issue-tracker`
- `GET /admin/facility-management`

## Reports / Comments
- `GET /recent-comments`

## Announcements
- `POST /announcements`
- `GET /announcements`
- `DELETE /announcements/{announcement_id}`

## Users
- `GET /users`
- `POST /admin/users`
- `PUT /users/{user_id}`
- `DELETE /users/{user_id}`

---

# 12. Folder Structure

## Backend
```text
backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
└── requirements.txt

**# 13. frontend structure**

frontend/src/
├── App.js
├── components/
│   ├── ProtectedRoute.js
│   ├── Sidebar.js
│   ├── StudentSidebar.js
│   ├── TeacherSidebar.js
│   ├── StudentTopbar.js
│   ├── TeacherTopbar.js
│   ├── SummaryCards.js
│   ├── AdminCharts.js
│   └── FeedbackForm.js
├── pages/
│   ├── AuthPage.js
│   ├── Dashboard.js
│   ├── Analytics.js
│   ├── Reports.js
│   ├── ManageComplaints.js
│   ├── UserManagement.js
│   ├── FacilityManagement.js
│   ├── AnnouncementManagement.js
│   ├── StudentHome.js
│   ├── MyFeedback.js
│   ├── RaiseComplaint.js
│   ├── MyComplaints.js
│   ├── NotificationsPage.js
│   ├── AnnouncementsPage.js
│   ├── ProfilePage.js
│   ├── TeacherHome.js
│   ├── TeacherReviewFeedback.js
│   ├── TeacherDepartmentAnalytics.js
│   └── FacilityIssueTracking.js
└── styles/
    └── App.css
