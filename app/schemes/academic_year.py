"""Schemes for academic year.
Features:
    - AcademicYearBase: The base model for academic year.
"""

from sqlmodel import Field, SQLModel

from app.utils import get_current_year_utc


class AcademicYearBase(SQLModel):
    """Base model for academic year"""

    year: int = Field(ge=1950, le=get_current_year_utc())
