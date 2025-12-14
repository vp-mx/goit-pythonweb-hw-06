"""
Database Query Functions for Student Management System.

This module provides 10 predefined query functions for analyzing student,
teacher, subject, and grade data. All queries use SQLAlchemy Core select
statements with proper joins and aggregations.

Each function returns specific analytical data from the university database:
- Student performance metrics
- Teacher workload and grading patterns
- Group statistics
- Subject enrollment information

Usage:
    from my_select import select_1, select_2

    # Get top 5 students
    top_students = select_1()

    # Get best student in a subject
    best_student = select_2("Mathematics")
"""

import logging
from typing import Any, List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.engine import Row
from tabulate import tabulate


from connect import session
from models import Grades, Groups, Students, Subjects, Teachers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def select_1() -> List[Row]:
    """
    Find top 5 students with the highest average grade across all subjects.

    This query calculates the average grade for each student across all their
    grades and returns the top 5 performers in descending order.

    Returns:
        List[Row]: List of tuples containing:
            - student_id (int): Student's database ID
            - student_name (str): Student's full name
            - student_email (str): Student's email address
            - avg_grade (float): Average grade across all subjects

    """
    logger.info("Executing select_1: Top 5 students by average grade")

    stmt = (
        select(
            Students.id.label("student_id"),
            Students.name.label("student_name"),
            Students.email.label("student_email"),
            func.round(func.avg(Grades.value), 2).label("avg_grade"),
        )
        .join(Grades, Grades.student_id == Students.id)
        .group_by(Students.id, Students.name, Students.email)
        .order_by(desc(func.avg(Grades.value)))
        .limit(5)
    )

    results = session.execute(stmt).all()
    logger.debug(f"Found {len(results)} top students")
    return results


def select_2(subject_name: str) -> Optional[Row]:
    """
    Find the student with the highest average grade in a specific subject.

    Args:
        subject_name: Name of the subject to query (e.g., "Mathematics")

    Returns:
        Optional[Row]: Single row containing:
            - student_id (int): Student's database ID
            - student_name (str): Student's full name
            - student_email (str): Student's email address
            - avg_grade (float): Average grade in the specified subject
        Returns None if no students found for the subject.

    """
    logger.info(f"Executing select_2: Best student in '{subject_name}'")

    stmt = (
        select(
            Students.id.label("student_id"),
            Students.name.label("student_name"),
            Students.email.label("student_email"),
            func.round(func.avg(Grades.value), 2).label("avg_grade"),
        )
        .join(Grades, Grades.student_id == Students.id)
        .join(Subjects, Subjects.id == Grades.subject_id)
        .where(Subjects.name == subject_name)
        .group_by(Students.id, Students.name, Students.email)
        .order_by(desc(func.avg(Grades.value)))
        .limit(1)
    )

    result = session.execute(stmt).first()

    if result:
        logger.debug(f"Best student in {subject_name}: {result.student_name}")
    else:
        logger.warning(f"No students found for subject: {subject_name}")

    return result


def select_3(subject_name: str) -> List[Row]:
    """
    Find average grade by group for a specific subject.

    Calculates the average grade for each group in a particular subject,
    ordered from highest to lowest performing group.

    Args:
        subject_name: Name of the subject to analyze

    Returns:
        List[Row]: List of tuples containing:
            - group_id (int): Group's database ID
            - group_name (str): Group's name
            - avg_grade (float): Average grade for the group in this subject
    """
    logger.info(f"Executing select_3: Average grades by group for '{subject_name}'")

    stmt = (
        select(
            Groups.id.label("group_id"),
            Groups.name.label("group_name"),
            func.round(func.avg(Grades.value), 2).label("avg_grade"),
        )
        .join(Students, Students.group_id == Groups.id)
        .join(Grades, Grades.student_id == Students.id)
        .join(Subjects, Subjects.id == Grades.subject_id)
        .where(Subjects.name == subject_name)
        .group_by(Groups.id, Groups.name)
        .order_by(desc(func.avg(Grades.value)))
    )

    results = session.execute(stmt).all()
    logger.debug(f"Found {len(results)} groups for {subject_name}")
    return results


def select_4() -> Optional[float]:
    """
    Find overall average grade across all students and subjects.

    Calculates the global average of all grades in the database,
    providing a general performance metric for the entire student body.

    Returns:
        Optional[float]: The overall average grade (0-100), rounded to 2 decimals.
        Returns None if no grades exist in the database.
    """
    logger.info("Executing select_4: Overall average grade")

    stmt = select(func.round(func.avg(Grades.value), 2).label("overall_avg"))
    avg = session.execute(stmt).scalar()

    if avg:
        logger.debug(f"Overall average grade: {avg:.2f}")
    else:
        logger.warning("No grades found in database")

    return avg


def select_5(teacher_name: str) -> List[Row]:
    """
    Find all courses (subjects) taught by a specific teacher.

    Args:
        teacher_name: Full name of the teacher

    Returns:
        List[Row]: List of tuples containing:
            - subject_id (int): Subject's database ID
            - subject_name (str): Name of the subject/course
    """
    logger.info(f"Executing select_5: Courses taught by '{teacher_name}'")

    stmt = (
        select(
            Subjects.id.label("subject_id"),
            Subjects.name.label("subject_name"),
        )
        .join(Teachers, Subjects.teacher_id == Teachers.id)
        .where(Teachers.name == teacher_name)
        .order_by(Subjects.name)
    )

    results = session.execute(stmt).all()
    logger.debug(f"Found {len(results)} courses for teacher {teacher_name}")
    return results


def select_6(group_name: str) -> List[Row]:
    """
    Find list of all students in a specific group.

    Args:
        group_name: Name of the student group (e.g., "Group 1")

    Returns:
        List[Row]: List of tuples containing:
            - student_id (int): Student's database ID
            - student_name (str): Student's full name
            - student_email (str): Student's email address

    """
    logger.info(f"Executing select_6: Students in group '{group_name}'")

    stmt = (
        select(
            Students.id.label("student_id"),
            Students.name.label("student_name"),
            Students.email.label("student_email"),
        )
        .join(Groups, Students.group_id == Groups.id)
        .where(Groups.name == group_name)
        .order_by(Students.name)
    )

    results = session.execute(stmt).all()
    logger.debug(f"Found {len(results)} students in {group_name}")
    return results


def select_7(group_name: str, subject_name: str) -> List[Row]:
    """
    Find grades for students in a specific group for a specific subject.

    Returns all individual grade records for students in the specified group
    and subject combination, ordered by student ID.

    Args:
        group_name: Name of the student group
        subject_name: Name of the subject

    Returns:
        List[Row]: List of tuples containing:
            - student_id (int): Student's database ID
            - student_name (str): Student's full name
            - grade_value (int): The grade received (0-100)
            - grade_date (datetime): When the grade was recorded

    """
    logger.info(f"Executing select_7: Grades for '{group_name}' in '{subject_name}'")

    stmt = (
        select(
            Students.id.label("student_id"),
            Students.name.label("student_name"),
            Grades.value.label("grade_value"),
            Grades.created_at.label("grade_date"),
        )
        .join(Groups, Students.group_id == Groups.id)
        .join(Grades, Grades.student_id == Students.id)
        .join(Subjects, Subjects.id == Grades.subject_id)
        .where(Groups.name == group_name, Subjects.name == subject_name)
        .order_by(Students.id, Grades.created_at)
    )

    results = session.execute(stmt).all()
    logger.debug(f"Found {len(results)} grade records")
    return results


def select_8(teacher_name: str) -> Optional[float]:
    """
    Find average grade given by a specific teacher across all their subjects.

    Calculates the average of all grades given in subjects taught by the
    specified teacher, providing insight into grading patterns.

    Args:
        teacher_name: Full name of the teacher

    Returns:
        Optional[float]: Average grade given by teacher (0-100), rounded to 2 decimals.
        Returns None if teacher has no graded subjects.

    """
    logger.info(f"Executing select_8: Average grade by teacher '{teacher_name}'")

    stmt = (
        select(func.round(func.avg(Grades.value), 2).label("avg_grade"))
        .join(Subjects, Subjects.id == Grades.subject_id)
        .join(Teachers, Subjects.teacher_id == Teachers.id)
        .where(Teachers.name == teacher_name)
    )

    avg = session.execute(stmt).scalar()

    if avg:
        logger.debug(f"Average grade by {teacher_name}: {avg:.2f}")
    else:
        logger.warning(f"No grades found for teacher: {teacher_name}")

    return avg


def select_9(student_name: str) -> List[Row]:
    """
    Find list of all courses (subjects) taken by a specific student.

    Returns unique subjects where the student has at least one grade,
    representing their course enrollment.

    Args:
        student_name: Full name of the student

    Returns:
        List[Row]: List of tuples containing:
            - subject_id (int): Subject's database ID
            - subject_name (str): Name of the subject/course

    """
    logger.info(f"Executing select_9: Courses taken by '{student_name}'")

    stmt = (
        select(
            Subjects.id.label("subject_id"),
            Subjects.name.label("subject_name"),
        )
        .join(Grades, Grades.subject_id == Subjects.id)
        .join(Students, Grades.student_id == Students.id)
        .where(Students.name == student_name)
        .group_by(Subjects.id, Subjects.name)
        .order_by(Subjects.name)
    )

    results = session.execute(stmt).all()
    logger.debug(f"Student {student_name} is taking {len(results)} courses")
    return results


def select_10(student_name: str, teacher_name: str) -> List[Row]:
    """
    Find courses that a specific student takes from a specific teacher.

    Returns the intersection of courses taught by the teacher and
    courses the student is enrolled in (has grades for).

    Args:
        student_name: Full name of the student
        teacher_name: Full name of the teacher

    Returns:
        List[Row]: List of tuples containing:
            - subject_id (int): Subject's database ID
            - subject_name (str): Name of the subject/course
    """
    logger.info(f"Executing select_10: Courses for '{student_name}' from '{teacher_name}'")

    stmt = (
        select(
            Subjects.id.label("subject_id"),
            Subjects.name.label("subject_name"),
        )
        .join(Grades, Grades.subject_id == Subjects.id)
        .join(Students, Grades.student_id == Students.id)
        .join(Teachers, Subjects.teacher_id == Teachers.id)
        .where(Students.name == student_name, Teachers.name == teacher_name)
        .group_by(Subjects.id, Subjects.name)
        .order_by(Subjects.name)
    )

    results = session.execute(stmt).all()
    logger.debug(f"Found {len(results)} matching courses")
    return results


def display_results(
    results: Any, title: str = "Query Results", headers: Optional[List[str]] = None, tablefmt: str = "fancy_grid"
) -> None:
    """
    Display query results in a formatted table using tabulate library.

    Args:
        results: Query results (can be list of rows or single value)
        title: Title to display above the results
        headers: Optional list of column headers. If None, uses keys from Row objects
        tablefmt: Table format style. Popular options:
            - "fancy_grid" (default): Beautiful box-drawing characters
            - "grid": Simple ASCII grid
            - "simple": Clean minimal style
            - "github": GitHub Markdown format
            - "pretty": Pretty tables style
            - "psql": PostgreSQL-like format
            - "rst": reStructuredText format

    Example:
        >>> results = select_1()
        >>> display_results(results, "Top 5 Students")
        >>> display_results(results, "Top 5", headers=["ID", "Name", "Email", "Avg"])
        >>> display_results(results, "Top 5", tablefmt="github")
    """
    print(f"\n{'=' * 100}")
    print(f"{title:^100}")
    print(f"{'=' * 100}\n")

    if not results:
        print("No results found")
    elif isinstance(results, list):
        table_data = [list(row) for row in results]
        print(
            tabulate(
                table_data,
                headers=headers or [],
                tablefmt=tablefmt,
                showindex="never",
                numalign="right",
                stralign="left",
            )
        )
    elif isinstance(results, Row):
        # Single row result
        headers = list(results._mapping.keys()) if headers is None else headers
        print(tabulate([list(results)], headers=headers, tablefmt=tablefmt, numalign="right", stralign="left"))
    else:
        # Handle scalar values (int, float, Decimal, etc.)
        print(tabulate([[results]], headers=["Result"], tablefmt=tablefmt, numalign="right"))

    print(f"\n{'=' * 100}\n")


if __name__ == "__main__":
    # Query 1: Top 5 students
    display_results(select_1(), "Top 5 Students by Average Grade")
    # Query 2: Best student in a subject
    display_results(select_2("Mathematics"), "Best Student in Mathematics")
    # Query 3: Average by group
    display_results(select_3("Physics"), "Average Grades by Group in Physics")
    # Query 4: Overall average
    display_results(select_4(), "Overall Average Grade")
    # Query 5: Teacher's courses (get first teacher from DB)
    first_teacher = session.execute(select(Teachers.name).limit(1)).scalar()
    if first_teacher:
        display_results(select_5(first_teacher), f"Courses Taught by {first_teacher}")

    # Query 6: Students in a group
    display_results(select_6("Group 1"), "Students in Group 1")
    # Query 7: Grades for group in subject
    display_results(
        select_7("Group 1", "Mathematics")[:5], "Sample Grades for Group 1 in Mathematics"  # Limit to 5 for demo
    )

    # Query 8: Teacher's average grade
    if first_teacher:
        pass

    # Query 9: Student's courses (get first student from DB)
    display_results(select_8(first_teacher), f"Average Grade by {first_teacher}")
    first_student = session.execute(select(Students.name).limit(1)).scalar()
    if first_student:
        display_results(select_9(first_student), f"Courses Taken by {first_student}")

    # Query 10: Student-Teacher course intersection
    if first_student and first_teacher:
        display_results(select_10(first_student, first_teacher), f"Courses for {first_student} from {first_teacher}")
