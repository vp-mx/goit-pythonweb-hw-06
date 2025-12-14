import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables or .env file."""
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: str = "5432"
    db_name: str = "university_db"
    sqlalchemy_echo: bool = False

    @property
    def database_url(self) -> str:
        """Build SQLAlchemy-compatible database URL."""
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


def get_settings() -> Settings:
    """Create Settings instance from environment variables / .env.

    Expected variables in .env or environment:
      - DB_USER
      - DB_PASSWORD
      - DB_HOST (optional, default: localhost)
      - DB_PORT (optional, default: 5432)
      - DB_NAME (optional, default: university_db)
      - SQLALCHEMY_ECHO (optional, true/false)
    """

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    if not db_user or not db_password:
        raise RuntimeError("DB_USER or DB_PASSWORD is not set in environment/.env")

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "university_db")

    echo_raw = os.getenv("SQLALCHEMY_ECHO", "false").lower()
    sqlalchemy_echo = echo_raw in {"1", "true", "yes", "on"}

    return Settings(
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_port=db_port,
        db_name=db_name,
        sqlalchemy_echo=sqlalchemy_echo,
    )

settings = get_settings()

