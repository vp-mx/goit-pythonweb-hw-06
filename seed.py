"""
Database Seeder Module for Student Management System.

This module provides functionality to populate the university database with
randomly generated test data using the Faker library. It creates a realistic
dataset including groups, teachers, subjects, students, and their grades.

Usage:
    python seed.py

The script will clear existing data and populate the database with:
    - 3 student groups
    - 3-5 teachers
    - 5-8 academic subjects
    - 30-50 students
    - 5-20 grades per student
"""

import logging
import random
from datetime import datetime, timedelta
from typing import List

from faker import Faker
from sqlalchemy.orm import Session

from connect import session
from models import Grades, Groups, Students, Subjects, Teachers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """
    Handles the generation and insertion of test data into the database.

    This class encapsulates all logic for creating fake data and populating
    the database tables with realistic student management information.

    Attributes:
        session: SQLAlchemy session for database operations
        fake: Faker instance for generating random data
        groups_count: Number of student groups to create
        teachers_range: Tuple of (min, max) teachers to create
        subjects_range: Tuple of (min, max) subjects to create
        students_range: Tuple of (min, max) students to create
        grades_range: Tuple of (min, max) grades per student
    """

    # Academic subjects pool for random selection
    ACADEMIC_SUBJECTS = [
        "Mathematics",
        "Physics",
        "Chemistry",
        "Biology",
        "History",
        "Geography",
        "Literature",
        "Computer Science",
        "Philosophy",
        "Economics",
    ]

    def __init__(
        self,
        db_session: Session,
        groups_count: int = 3,
        teachers_range: tuple = (3, 5),
        subjects_range: tuple = (5, 8),
        students_range: tuple = (30, 50),
        grades_range: tuple = (5, 20),
    ):
        """
        Initialize the database seeder with configuration parameters.

        Args:
            db_session: Active SQLAlchemy session
            groups_count: Number of student groups to generate
            teachers_range: Min and max number of teachers
            subjects_range: Min and max number of subjects
            students_range: Min and max number of students
            grades_range: Min and max grades per student
        """
        self.session = db_session
        self.fake = Faker()
        self.groups_count = groups_count
        self.teachers_range = teachers_range
        self.subjects_range = subjects_range
        self.students_range = students_range
        self.grades_range = grades_range

        # Storage for generated entities
        self._groups: List[Groups] = []
        self._teachers: List[Teachers] = []
        self._subjects: List[Subjects] = []
        self._students: List[Students] = []
        self._grades: List[Grades] = []

    def _purge_existing_data(self) -> None:
        """
        Remove all existing records from database tables.

        Deletes data in the correct order to respect foreign key constraints.
        Uses cascade delete where configured in models.
        """
        logger.info("Purging existing database records...")

        try:
            # Delete in reverse dependency order
            for model in [Grades, Students, Subjects, Teachers, Groups]:
                deleted_count = self.session.query(model).delete()
                logger.debug(f"Deleted {deleted_count} records from {model.__tablename__}")

            self.session.commit()
            logger.info("Database purge completed successfully")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error during database purge: {e}")
            raise

    def _generate_groups(self) -> None:
        """Create student group entities with sequential naming."""
        logger.info(f"Generating {self.groups_count} student groups...")

        self._groups = [Groups(name=f"Group {idx + 1}") for idx in range(self.groups_count)]

        self.session.add_all(self._groups)
        self.session.flush()  # Get IDs without committing
        logger.debug(f"Created {len(self._groups)} groups")

    def _generate_teachers(self) -> None:
        """Create teacher entities with unique names and emails."""
        count = random.randint(*self.teachers_range)
        logger.info(f"Generating {count} teachers...")

        self._teachers = [
            Teachers(
                name=self.fake.name(),
                email=self.fake.unique.email(),
            )
            for _ in range(count)
        ]

        self.session.add_all(self._teachers)
        self.session.flush()
        logger.debug(f"Created {len(self._teachers)} teachers")

    def _generate_subjects(self) -> None:
        """
        Create subject entities with realistic names.

        Each subject is randomly assigned to one of the generated teachers.
        """
        count = random.randint(*self.subjects_range)
        logger.info(f"Generating {count} subjects...")

        # Select random subset of available subjects
        selected_subjects = random.sample(self.ACADEMIC_SUBJECTS, count)

        self._subjects = [
            Subjects(
                name=subject_name,
                teacher=random.choice(self._teachers),
            )
            for subject_name in selected_subjects
        ]

        self.session.add_all(self._subjects)
        self.session.flush()
        logger.debug(f"Created {len(self._subjects)} subjects")

    def _generate_students(self) -> None:
        """
        Create student entities with random distribution across groups.

        Each student gets a unique email and is assigned to a random group.
        """
        count = random.randint(*self.students_range)
        logger.info(f"Generating {count} students...")

        self._students = [
            Students(
                name=self.fake.name(),
                email=self.fake.unique.email(),
                group=random.choice(self._groups),
            )
            for _ in range(count)
        ]

        self.session.add_all(self._students)
        self.session.flush()
        logger.debug(f"Created {len(self._students)} students")

    def _generate_grades(self) -> None:
        """
        Create grade records for all students across various subjects.

        Each student receives a random number of grades (within configured range)
        with timestamps distributed over the past year.
        """
        logger.info("Generating student grades...")

        for student in self._students:
            grades_count = random.randint(*self.grades_range)

            for _ in range(grades_count):
                # Random grade value between 1 and 100
                grade_value = random.randint(1, 100)

                # Random date within the past year
                days_ago = random.randint(0, 365)
                grade_date = datetime.now() - timedelta(days=days_ago)

                grade = Grades(
                    student=student,
                    subject=random.choice(self._subjects),
                    value=grade_value,
                    created_at=grade_date,
                )
                self._grades.append(grade)

        self.session.add_all(self._grades)
        logger.debug(f"Created {len(self._grades)} grade records")

    def populate(self) -> None:
        """
        Execute the complete database seeding process.

        This method orchestrates the entire seeding workflow:
        1. Purge existing data
        2. Generate all entities in dependency order
        3. Commit transaction
        4. Report statistics

        Raises:
            Exception: If any step in the seeding process fails
        """
        try:
            logger.info("Starting database seeding process...")
            start_time = datetime.now()

            self._purge_existing_data()
            self._generate_groups()
            self._generate_teachers()
            self._generate_subjects()
            self._generate_students()
            self._generate_grades()

            self.session.commit()

            elapsed = (datetime.now() - start_time).total_seconds()

            logger.info("=" * 60)
            logger.info("Database seeding completed successfully!")
            logger.info("=" * 60)
            logger.info(f"Groups created:    {len(self._groups):>5}")
            logger.info(f"Teachers created:  {len(self._teachers):>5}")
            logger.info(f"Subjects created:  {len(self._subjects):>5}")
            logger.info(f"Students created:  {len(self._students):>5}")
            logger.info(f"Grades created:    {len(self._grades):>5}")
            logger.info(f"Time elapsed:      {elapsed:.2f}s")
            logger.info("=" * 60)

        except Exception as e:
            self.session.rollback()
            logger.error(f"Seeding process failed: {e}")
            raise


def main() -> None:
    """
    Entry point for the database seeding script.

    Creates a DatabaseSeeder instance and executes the population process.
    """
    seeder = DatabaseSeeder(db_session=session)
    seeder.populate()


if __name__ == "__main__":
    main()
