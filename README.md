Church Management System API
A robust, query-optimized Django REST Framework backend designed to handle church administration, member directory, ministry structures, event tracking, financial donations, and real-time dashboard analytics.
 **Features**
Member & Family Management: Track congregants, membership statuses (active, inactive, etc.), and household relationships using optimized prefetching.

Ministry Tracking: Manage church groups, ministry leaders, and assigned members with single-query join fetching (select_related and prefetch_related).

Event Management: Schedule and filter upcoming church services, outreach programs, and conferences.

Financial & Donation Tracking: Log tithes, offerings, building funds, and missions with support for multiple payment methods and custom display fields.

Dashboard Analytics API (/dashboard-stats/): High-performance aggregation endpoint that delivers:

Combined member metrics (total vs. active counts).

All-time and 30-day donation totals.

Recent donation logs with preloaded member names.

Upcoming events list using deferred query optimization (.only()).

Purpose-based financial breakdown (Tithe, Offering, Building Fund, Missions, Other).

6-month historical giving trend formatted by month.

** Tech Stack**
Language: Python 3.13+

Framework: Django 5.x / Django REST Framework (DRF)

Filtering: django-filter

CORS Handling: django-cors-headers

Database: SQLite (default for development) / PostgreSQL ready
