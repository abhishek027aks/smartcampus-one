::: {align="center"}
`<a href="https://github.com/abhishek027aks/smartcampus-one">`{=html}
`<img src="assets/banner.svg" alt="SmartCampus One" width="100%">`{=html}
`</a>`{=html}

`<br/>`{=html}

`<img src="assets/logo.svg" alt="SmartCampus One Logo" width="110"/>`{=html}

# SmartCampus One

### One Smart Platform for Every Campus

```{=html}
<p>
```
`<strong>`{=html}Multi-College Smart Timetable & Attendance Management
Platform`</strong>`{=html}
```{=html}
</p>
```
```{=html}
<p>
```
`<a href="https://github.com/abhishek027aks/smartcampus-one/stargazers">`{=html}`<img src="https://img.shields.io/github/stars/abhishek027aks/smartcampus-one?style=for-the-badge&logo=github&label=Stars" alt="GitHub Stars">`{=html}`</a>`{=html}
`<a href="https://github.com/abhishek027aks/smartcampus-one/network/members">`{=html}`<img src="https://img.shields.io/github/forks/abhishek027aks/smartcampus-one?style=for-the-badge&logo=github&label=Forks" alt="GitHub Forks">`{=html}`</a>`{=html}
`<img src="https://img.shields.io/badge/Status-Active%20Development-22C55E?style=for-the-badge" alt="Active Development">`{=html}
```{=html}
</p>
```
```{=html}
<p>
```
`<img src="https://img.shields.io/badge/React-18%2B-61DAFB?style=flat-square&logo=react&logoColor=111827" alt="React">`{=html}
`<img src="https://img.shields.io/badge/TypeScript-5%2B-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">`{=html}
`<img src="https://img.shields.io/badge/FastAPI-Python-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">`{=html}
`<img src="https://img.shields.io/badge/PostgreSQL-16%2B-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">`{=html}
`<img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">`{=html}
`<img src="https://img.shields.io/badge/REST-API-111827?style=flat-square&logo=swagger&logoColor=white" alt="REST API">`{=html}
```{=html}
</p>
```
```{=html}
<p>
```
`<a href="#-overview">`{=html}Overview`</a>`{=html} •
`<a href="#-features">`{=html}Features`</a>`{=html} •
`<a href="#-attendance-system">`{=html}Attendance`</a>`{=html} •
`<a href="#-architecture">`{=html}Architecture`</a>`{=html} •
`<a href="#-installation">`{=html}Installation`</a>`{=html} •
`<a href="#-roadmap">`{=html}Roadmap`</a>`{=html}
```{=html}
</p>
```
:::

------------------------------------------------------------------------

## 📌 Overview

**SmartCampus One** is a modern, scalable **multi-tenant college
management platform** built to bring timetable management, lecture-wise
attendance, student/teacher management, analytics, reports and future
college integrations into one centralized system.

The platform is designed for **multiple colleges**, while keeping each
college's academic data logically isolated through a unique **College
Code** and tenant-aware authorization.

### 🏫 Multi-College Model

``` text
                         SMARTCAMPUS ONE
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
          ▼                     ▼                     ▼
      COLLEGE A              COLLEGE B              COLLEGE C
      ABC-7X29               XYZ-4P82               PQR-9K51
          │                     │                     │
          ├─ Students           ├─ Students           ├─ Students
          ├─ Teachers           ├─ Teachers           ├─ Teachers
          ├─ Timetable          ├─ Timetable          ├─ Timetable
          └─ Attendance         └─ Attendance         └─ Attendance
```

> 🔐 **Core principle:** users from one college must never be able to
> access another college's protected data.

------------------------------------------------------------------------

# ✨ Features

  -----------------------------------------------------------------------
  Module                              Highlights
  ----------------------------------- -----------------------------------
  🏫 **Multi-College**                Unique college code, tenant
                                      isolation, college settings

  👥 **Role Management**              Super Admin, College Admin,
                                      Teacher, Student

  📅 **Smart Timetable**              Manual scheduling, automatic
                                      generation, conflict detection

  📸 **Smart Attendance**             Temporary code, expiry timer, live
                                      camera photo

  📝 **Manual Attendance**            Teacher fallback with audit trail

  📊 **Analytics**                    Subject, section, department and
                                      student statistics

  📄 **Reports**                      PDF, Excel and CSV-ready reporting

  🔔 **Notifications**                Attendance, timetable and academic
                                      alerts

  🔌 **Integrations**                 Configurable college ERP/API
                                      integration

  🌐 **Deployment**                   Responsive web/PWA architecture,
                                      Docker and cloud-ready
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 📸 Attendance System

SmartCampus One uses a **temporary-code based attendance workflow**
rather than face recognition as the core attendance mechanism.

### Attendance Flow

``` text
Teacher
   │
   ▼
Select Current Lecture
   │
   ▼
Start Attendance
   │
   ▼
Generate Temporary Code
   │
   ▼
Set 1–3 Minute Window
   │
   ▼
Student Enters Code
   │
   ▼
Live Camera Capture
   │
   ▼
Server-Side Verification
   │
   ▼
✅ Attendance Recorded
```

### 🔢 Example Session

``` text
Subject       : Java
Teacher       : Mr. Sharma
Section       : BCA 2A
Session ID    : JVA001
Code          : 583214
Valid For     : 2 Minutes
Status        : ACTIVE
```

When the attendance window expires, the code automatically becomes
invalid.

### 🔎 Verification Checks

-   Student authentication
-   College / tenant
-   Course
-   Semester
-   Section
-   Subject
-   Teacher
-   Lecture session
-   Temporary code
-   Code expiry
-   Duplicate attendance
-   Live photo capture

### 📷 Attendance Record

``` text
Student
Roll Number
College
Course
Semester
Section
Subject
Teacher
Date
Exact Time
Session ID
Live Photo
Attendance Status
```

> 🔒 Live-photo data should be protected with strict access controls,
> retention/deletion rules and appropriate privacy/consent practices in
> real institutional deployments.

------------------------------------------------------------------------

# 📝 Manual Attendance

Teachers can use manual attendance when a student has a technical
problem.

Examples:

-   No smartphone
-   Internet problem
-   Camera problem
-   Device/battery issue
-   Temporary system issue

Manual changes should be recorded through an **audit log**.

------------------------------------------------------------------------

# 📅 Smart Timetable

Administrators can manage:

-   Departments
-   Courses
-   Semesters
-   Sections
-   Subjects
-   Teachers
-   Classrooms
-   Laboratories
-   Working days
-   College hours
-   Period duration
-   Teacher availability
-   Room availability
-   Holidays

### 🤖 Automatic Timetable Generator

The timetable engine is designed to identify:

``` text
❌ Teacher conflicts
❌ Room conflicts
❌ Section conflicts
❌ Room-capacity conflicts
❌ Lab requirement conflicts
❌ Teacher availability conflicts
```

The system should detect conflicts before a timetable is published.

------------------------------------------------------------------------

# 👥 User Roles

### 🔐 Super Admin

-   Manage colleges
-   Global platform configuration
-   System monitoring
-   Global settings

### 🏫 College Admin

-   Students & teachers
-   Departments & courses
-   Subjects & sections
-   Rooms & labs
-   Timetable
-   Attendance rules
-   Reports
-   Branding
-   Integrations

### 👨‍🏫 Teacher

-   Today's timetable
-   Start attendance
-   Generate code
-   Monitor live attendance
-   Manual attendance
-   Attendance reports
-   Correction requests

### 👨‍🎓 Student

-   Today's timetable
-   Join attendance
-   Enter code
-   Capture live photo
-   Attendance percentage
-   Attendance history
-   Notifications
-   Correction requests

------------------------------------------------------------------------

# 📊 Analytics & Reports

### Attendance Formula

``` text
Attendance % =
(Present Classes / Total Conducted Classes) × 100
```

### Example

  Subject         Present   Conducted   Attendance
  ------------- --------- ----------- ------------
  Java                 18          20       🟢 90%
  DBMS                 15          20       🟡 75%
  Python               19          20       🟢 95%
  Mathematics          14          20       🔴 70%

### Reports

-   Student attendance
-   Subject-wise attendance
-   Section-wise attendance
-   Department-wise attendance
-   Teacher-wise reports
-   Monthly reports
-   Semester reports

**Export:** PDF • Excel • CSV

------------------------------------------------------------------------

# 🔔 Notifications

The platform can provide notifications for:

-   Attendance updates
-   Low attendance
-   Timetable changes
-   Room changes
-   Class changes
-   Correction request status
-   Important announcements

------------------------------------------------------------------------

# 🔌 College API Integration

SmartCampus One is designed to support future integrations with college
ERP and academic systems.

``` text
College Admin
     │
     ▼
Integration Settings
     │
     ├── API Name
     ├── Base URL
     ├── Auth Type
     ├── API Key / Token
     └── Endpoint
             │
             ▼
       Secure Backend
             │
             ▼
       External College API
```

> 🔐 API keys, tokens and other credentials must remain server-side and
> must never be committed to Git or exposed in frontend code.

------------------------------------------------------------------------

# 🏗️ Architecture

``` text
┌────────────────────────────────────────────────────┐
│              Student / Teacher / Admin             │
└──────────────────────────┬─────────────────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ React + TypeScript   │
                │      Frontend        │
                └──────────┬───────────┘
                           │ REST / JSON
                           ▼
                ┌──────────────────────┐
                │   FastAPI Backend    │
                │   Business Logic     │
                └──────────┬───────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌───────────┐ ┌─────────────┐
        │PostgreSQL│ │  Secure   │ │ External    │
        │ Database │ │  Storage  │ │ APIs / ERP  │
        └──────────┘ └───────────┘ └─────────────┘
```

------------------------------------------------------------------------

# 💻 Technology Stack

  Layer               Technology
  ------------------- -------------------------
  Frontend            React + TypeScript
  Build Tool          Vite
  Backend             Python + FastAPI
  Database            PostgreSQL
  API                 REST + JSON
  Authentication      JWT
  Password Security   Secure Password Hashing
  Camera              HTML5 Camera API
  Charts              Recharts / Chart.js
  Reports             Python
  Containerization    Docker
  Deployment          Linux / Cloud

------------------------------------------------------------------------

# 📁 Project Structure

``` text
smartcampus-one/
│
├── frontend/                  # React + TypeScript
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── types/
│   │   └── assets/
│   └── public/
│
├── backend/                   # FastAPI
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── middleware/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── database/                  # Migrations & seeds
│   ├── migrations/
│   └── seeds/
│
├── modules/
│   ├── timetable/
│   ├── attendance/
│   ├── reports/
│   ├── notifications/
│   └── integrations/
│
├── storage/                   # Runtime file storage
├── docs/                      # Project documentation
├── tests/                     # Integration & E2E tests
├── deployment/                # Docker / Nginx / scripts
│
├── assets/                    # README branding assets
│   ├── logo.svg
│   └── banner.svg
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

------------------------------------------------------------------------

# 🔐 Security

Security is a core requirement.

### Security Principles

-   🔑 JWT authentication
-   👥 Role-based authorization
-   🔒 Password hashing
-   🏢 Tenant isolation
-   🛡️ API authorization
-   ✅ Input validation
-   📝 Audit logging
-   🔐 Environment-based secrets
-   📁 Protected file access
-   🌐 HTTPS in production
-   🔑 Server-side API credentials

### 🚫 Never Commit

``` text
.env
API Keys
Database Passwords
JWT Secrets
College API Credentials
Production Tokens
Student Photos
Private Credentials
```

Use `.env.example` as the configuration template.

------------------------------------------------------------------------

# 🚀 Installation

> The installation guide will evolve as the project moves through
> development phases.

### 1. Clone

``` bash
git clone https://github.com/abhishek027aks/smartcampus-one.git
cd smartcampus-one
```

### 2. Backend

``` bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Frontend

``` bash
cd frontend

npm install
npm run dev
```

### 4. Docker

``` bash
docker compose up --build
```

------------------------------------------------------------------------

# 🛣️ Roadmap

## Phase 1 --- Foundation

-   [x] GitHub repository
-   [ ] Architecture
-   [ ] Frontend setup
-   [ ] Backend setup
-   [ ] PostgreSQL setup
-   [ ] Docker setup

## Phase 2 --- Authentication

-   [ ] Login
-   [ ] JWT authentication
-   [ ] Role-based access
-   [ ] Password security

## Phase 3 --- College Management

-   [ ] College creation
-   [ ] Unique college code
-   [ ] Departments
-   [ ] Courses
-   [ ] Semesters
-   [ ] Sections
-   [ ] Students
-   [ ] Teachers
-   [ ] Subjects
-   [ ] Rooms

## Phase 4 --- Timetable

-   [ ] Manual timetable
-   [ ] Automatic timetable generator
-   [ ] Conflict detection
-   [ ] Room management
-   [ ] Teacher availability
-   [ ] Holiday management

## Phase 5 --- Attendance

-   [ ] Lecture sessions
-   [ ] Temporary code
-   [ ] Expiry timer
-   [ ] Live photo capture
-   [ ] Verification
-   [ ] Manual attendance
-   [ ] Attendance history
-   [ ] Audit logs

## Phase 6 --- Analytics & Reports

-   [ ] Attendance percentage
-   [ ] Student dashboard
-   [ ] Teacher dashboard
-   [ ] Admin dashboard
-   [ ] Analytics
-   [ ] PDF
-   [ ] Excel
-   [ ] CSV

## Phase 7 --- Advanced Features

-   [ ] Low attendance alerts
-   [ ] Correction requests
-   [ ] Notifications
-   [ ] Location verification
-   [ ] Wi-Fi verification
-   [ ] College branding
-   [ ] Custom domain
-   [ ] API integrations
-   [ ] Attendance prediction

## Phase 8 --- Production

-   [ ] Production Docker
-   [ ] PostgreSQL deployment
-   [ ] Secure photo storage
-   [ ] HTTPS
-   [ ] Domain
-   [ ] Backup
-   [ ] Monitoring
-   [ ] Performance optimization

------------------------------------------------------------------------

# 📱 Responsive Experience

The platform is designed for:

-   💻 Desktop
-   🖥️ Laptop
-   📱 Android
-   🍎 iPhone
-   📟 Tablet

The first release can use a responsive web/PWA architecture, with a
dedicated Android application as a future enhancement.

------------------------------------------------------------------------

# 🔮 Future Enhancements

-   📱 Android Application
-   📝 Assignments
-   📚 Study Material
-   🧾 Examination Management
-   📊 Internal Marks
-   🎓 Results
-   📢 Notices
-   📖 Library Management
-   🏠 Hostel Management
-   🚌 Transport Management
-   📈 Advanced Analytics
-   🔌 ERP Integration
-   📧 Email Integration
-   💬 SMS / WhatsApp Integration
-   💳 Subscription Management

------------------------------------------------------------------------

# 🧪 Testing Strategy

``` text
Unit Testing
     ↓
Integration Testing
     ↓
API Testing
     ↓
End-to-End Testing
     ↓
Security Testing
     ↓
Production Testing
```

Critical areas:

-   Authentication
-   Authorization
-   Tenant isolation
-   Timetable conflicts
-   Code expiry
-   Duplicate attendance
-   Live photo capture
-   Reports
-   API integrations

------------------------------------------------------------------------

# 📚 Documentation

Documentation will be maintained under:

``` text
docs/
├── architecture/
├── api/
├── database/
├── setup/
└── project-report/
```

Planned documentation:

-   System architecture
-   Database design
-   API documentation
-   Installation guide
-   Deployment guide
-   User guide
-   BCA project report
-   Development notes

------------------------------------------------------------------------

# 🤝 Contributing

Contributions, suggestions, bug reports and improvements are welcome.

``` text
Fork
  ↓
Create Feature Branch
  ↓
Make Changes
  ↓
Test
  ↓
Commit
  ↓
Pull Request
```

Please test changes before opening a pull request.

------------------------------------------------------------------------

# 🎓 Academic Project

  Detail          Information
  --------------- ------------------------
  Project         SmartCampus One
  Type            BCA Final Year Project
  Architecture    Multi-Tenant
  Primary Focus   Timetable + Attendance
  Frontend        React + TypeScript
  Backend         FastAPI + Python
  Database        PostgreSQL

### Project Title

**SmartCampus One: A Multi-College Smart Timetable and Attendance
Management Platform**

### Tagline

> **One Smart Platform for Every Campus**

------------------------------------------------------------------------

# 👨‍💻 Author

::: {align="center"}
`<img src="assets/logo.svg" width="70" alt="SmartCampus One">`{=html}

### ABHISHEK KUMAR SINGH

Developer & Project Author

`<a href="https://github.com/abhishek027aks">`{=html}
`<img src="https://img.shields.io/badge/GitHub-abhishek027aks-181717?style=for-the-badge&logo=github" alt="GitHub">`{=html}
`</a>`{=html}
:::

------------------------------------------------------------------------

# ⭐ Support

If you find **SmartCampus One** useful:

⭐ Star the repository\
🍴 Fork the project\
🐛 Report a bug\
💡 Suggest a feature

------------------------------------------------------------------------

::: {align="center"}
### 🎓 SmartCampus One

**One Smart Platform for Every Campus**

Built with ❤️ by **ABHISHEK KUMAR SINGH**

**Code • Learn • Build • Innovate**
:::
