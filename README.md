# Student Management Database System

A PostgreSQL-based student management system built with SQLAlchemy ORM and Alembic migrations. This project implements a complete database solution for tracking students, groups, teachers, subjects, and grades.

## 🎯 Project Overview

This database system manages:
- **Students** - Student records with group assignments
- **Groups** - Student group organization
- **Teachers** - Teacher information
- **Subjects** - Academic subjects taught by teachers
- **Grades** - Student performance tracking with timestamps

## Getting Started

### Prerequisites

- Docker
- Python 3.8+
- Poetry (package manager)

### Database Setup

Start the PostgreSQL Docker container:

```bash
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=123456 -d postgres
```

> **Note**: Replace `postgres` with your preferred container name and `123456` with a secure password.

### Installation

1. Install dependencies using Poetry:
```bash
poetry install
```

2. Configure environment variables in `.env`:
```env
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=university_db
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Seed the database with test data:
```bash
python seed.py
```
