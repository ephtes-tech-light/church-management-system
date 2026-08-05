# ⛪ Church Management System (CMS) API

A robust, scalable backend RESTful API built with **Django** and **Django REST Framework (DRF)** designed to streamline church administration, congregant tracking, ministry coordination, event scheduling, and financial donation tracking.

---

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Database & Performance Optimization](#-database--performance-optimization)
- [API Endpoints Overview](#-api-endpoints-overview)
- [Installation & Setup](#-installation--setup)
- [Environment Configuration](#-environment-configuration)
- [API Usage Examples](#-api-usage-examples)


---

## ✨ Features

### 👨‍👩‍👧‍👦 Family & Congregant Management
* Organize congregants into household/family units (`Family`).
* Detailed member profile tracking (`Member`) including contact details, membership status (`ACTIVE`, `INACTIVE`, `PROSPECTIVE`), and family linkages.
* Full-text search across member names, emails, and phone numbers.

### 🏛️ Ministry & Small Groups
* Department and ministry tracking (`Ministry`) with assigned leaders and associated members.
* Optimized relational queries connecting ministries, leaders, and volunteers.

### 📅 Event Scheduling
* Church event calendar management (`Event`) with timestamp tracking.
* Dynamic query filtering for upcoming vs. past events via URL parameters (`?upcoming=true`).

### 💰 Financial & Donation Management
* Transparent record-keeping of tithes, offerings, and special pledges (`Donation`).
* Tracking payment methods, dates, and donor references.
* Sorted chronological access for auditing and reporting.

---

## 🛠️ Tech Stack

* **Framework:** Python 3.10+ | Django 4.2+ | Django REST Framework 3.14+
* **Database:** PostgreSQL / SQLite (Development)
* **Filtering & Search:** `django-filter`, DRF `SearchFilter`, DRF `OrderingFilter`
* **Authentication & Authorization:** DRF TokenAuth / JWT (Session & Bearer)
* **Version Control:** Git & GitHub

---

## 🏗️ Project Architecture

```
church-management-system/
│
├── congregants/                  # Main application module
│   ├── migrations/               # Database migration files
│   ├── models.py                 # Family, Member, Ministry, Event, Donation models
│   ├── serializers.py            # DRF ModelSerializers for data validation & JSON representation
│   ├── views.py                  # Optimized ModelViewSets and custom API views
│   ├── urls.py                   # App-level routing and ViewSet registering
│   └── tests.py                  # Unit and integration test suites
│
├── church_system/                # Core Django project configuration
│   ├── settings.py               # Application settings, DRF configuration
│   ├── urls.py                   # Root URL routing
│   └── wsgi.py / asgi.py         # Deployment gateways
│
├── manage.py                     # Django administrative utility
├── requirements.txt              # Project Python dependencies
└── README.md                     # Project documentation
```

---

## ⚡ Database & Performance Optimization

To avoid performance bottlenecks like the **N+1 query problem** when fetching related database models, this API implements DRF and Django ORM query optimizations:

1. **`select_related` (SQL `JOIN`):**
   * Used for single-valued relationships (Foreign Keys).
   * Applied in `MemberViewSet` (`select_related('family')`) and `MinistryViewSet` (`select_related('leader')`).
2. **`prefetch_related` (Separate Query Join):**
   * Used for multi-valued relationships (Reverse Foreign Keys & Many-to-Many).
   * Applied in `FamilyViewSet` (`prefetch_related('members')`) and `MinistryViewSet` (`prefetch_related('members')`).

---

## 🔗 API Endpoints Overview

Default Base URL: `http://localhost:8000/api/`

| Endpoint | HTTP Method | Description | Filter / Search Parameters |
| :--- | :--- | :--- | :--- |
| `/api/families/` | `GET`, `POST` | List or create family units | `?search=<name>` |
| `/api/families/{id}/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete family | - |
| `/api/members/` | `GET`, `POST` | List or register congregants | `?membership_status=ACTIVE`, `?search=<query>`, `?ordering=name` |
| `/api/members/{id}/` | `GET`, `PUT`, `DELETE` | Retrieve, update, or delete member | - |
| `/api/ministries/` | `GET`, `POST` | List or create church ministries | `?search=<name>` |
| `/api/events/` | `GET`, `POST` | List or schedule church events | `?upcoming=true` |
| `/api/donations/` | `GET`, `POST` | List or record financial gifts | Sorted by `-date`, `-created_at` |

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.10 or higher
* `pip` package manager
* `virtualenv` or Python `venv` module

### Step-by-Step Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ephtes-tech-light/church-management-system.git
   cd church-management-system
   ```

2. **Create and Activate Virtual Environment:**
   * **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Superuser (Admin Access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```
   Access the API at `http://127.0.0.1:8000/api/` and Django Admin at `http://127.0.0.1:8000/admin/`.

---

## 💡 API Usage Examples

### 1. Fetch Active Members with Search
**Request:**
`GET /api/members/?membership_status=ACTIVE&search=John`

**Response (`200 OK`):**
```json
[
  {
    "id": 15,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+15551234567",
    "membership_status": "ACTIVE",
    "family": {
      "id": 4,
      "name": "Doe Family"
    }
  }
]
```

### 2. Fetch Upcoming Events Only
**Request:**
`GET /api/events/?upcoming=true`

**Response (`200 OK`):**
```json
[
  {
    "id": 8,
    "title": "Sunday Worship & Communion",
    "start_time": "2026-08-09T09:00:00Z",
    "end_time": "2026-08-09T11:30:00Z",
    "location": "Main Sanctuary"
  }
]
