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

## Queries

The `select_statements.py` file contains 10 predefined query functions:

1. **select_1()** - Find top 5 students with the highest average grade across all subjects
2. **select_2(subject_name)** - Find the student with the highest average grade in a specific subject
3. **select_3(subject_name)** - Find average grade by group for a specific subject
4. **select_4()** - Find overall average grade across all students
5. **select_5(teacher_name)** - Find courses taught by a specific teacher
6. **select_6(group_name)** - Find list of students in a specific group
7. **select_7(group_name, subject_name)** - Find grades for students in a group for a specific subject
8. **select_8(teacher_name)** - Find average grade given by a specific teacher
9. **select_9(student_name)** - Find list of courses taken by a specific student
10. **select_10(student_name, teacher_name)** - Find courses a student takes from a specific teacher

### Create a new migration

After modifying models in `models.py`:

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```