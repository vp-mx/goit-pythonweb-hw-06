"""
Database models for the student management system.

This module defines SQLAlchemy ORM models for managing students, groups,
teachers, subjects, and grades in an educational institution database.
"""

from datetime import datetime
from typing import Annotated

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Type aliases for common column patterns
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class Groups(Base):
    """
    Group model representing a student group.

    A group is a collection of students studying together.
    Each group has a unique name and can contain multiple students.

    Attributes:
        id: Primary key, auto-incremented integer
        name: Unique group name (e.g., "Group 1", "AD-101")
        students: List of students belonging to this group
    """

    __tablename__ = "groups"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True, index=True)
    students: Mapped[list["Students"]] = relationship(back_populates="group", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Return string representation of the group."""
        return f"<Group(id={self.id}, name='{self.name}')>"


class Teachers(Base):
    """
    Teacher model representing an instructor.

    Teachers are responsible for teaching subjects. Each teacher
    can teach multiple subjects and has a unique email address.

    Attributes:
        id: Primary key, auto-incremented integer
        name: Full name of the teacher
        email: Unique email address for the teacher
        subjects: List of subjects taught by this teacher
    """

    __tablename__ = "teachers"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    subjects: Mapped[list["Subjects"]] = relationship(back_populates="teacher", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Return string representation of the teacher."""
        return f"<Teacher(id={self.id}, name='{self.name}', email='{self.email}')>"


class Subjects(Base):
    """
    Subject model representing a course or subject.

    Each subject is taught by one teacher and can have multiple
    students receiving grades in it.

    Attributes:
        id: Primary key, auto-incremented integer
        name: Unique subject name (e.g., "Mathematics", "Physics")
        teacher_id: Foreign key referencing the teacher who teaches this subject
        teacher: Teacher instance who teaches this subject
        grades: List of grades given in this subject
    """

    __tablename__ = "subjects"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    teacher: Mapped["Teachers"] = relationship(back_populates="subjects")
    grades: Mapped[list["Grades"]] = relationship(back_populates="subject", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Return string representation of the subject."""
        return f"<Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})>"


class Students(Base):
    """
    Student model representing a student in the system.

    Each student belongs to one group, has a unique email address,
    and receives grades in various subjects.

    Attributes:
        id: Primary key, auto-incremented integer
        name: Full name of the student
        email: Unique email address for the student
        group_id: Foreign key referencing the group the student belongs to
        group: Group instance this student belongs to
        grades: List of grades this student has received
    """

    __tablename__ = "students"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    group: Mapped["Groups"] = relationship(back_populates="students")
    grades: Mapped[list["Grades"]] = relationship(back_populates="student", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Return string representation of the student."""
        return f"<Student(id={self.id}, name='{self.name}', email='{self.email}', group_id={self.group_id})>"


class Grades(Base):
    """
    Grade model representing a student's grade in a subject.

    Each grade links a student to a subject with a numeric value
    and timestamp indicating when the grade was received.

    Attributes:
        id: Primary key, auto-incremented integer
        student_id: Foreign key referencing the student who received the grade
        subject_id: Foreign key referencing the subject for which the grade was given
        value: Numeric grade value (typically 1-100)
        created_at: Timestamp when the grade was recorded (defaults to current time)
        student: Student instance who received this grade
        subject: Subject instance for which this grade was given
    """

    __tablename__ = "grades"
    __table_args__ = (CheckConstraint("value >= 0 AND value <= 100", name="check_grade_value"),)

    id: Mapped[intpk]
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True)
    value: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), server_default=func.now())
    student: Mapped["Students"] = relationship(back_populates="grades")
    subject: Mapped["Subjects"] = relationship(back_populates="grades")

    def __repr__(self) -> str:
        """Return string representation of the grade."""
        return f"<Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, value={self.value})>"
