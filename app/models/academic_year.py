"""Model for academic_year.
Features:
    - AcademicYear: The model for database usage.
"""

from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models import Keketatan, Mahasiswa, Peminatan


class AcademicYear(SQLModel, table=True):
    """Model for database academic year table"""

    __tablename__ = "academic_year"

    id: Optional[int] = Field(default=None, primary_key=True)
    year: int = Field(unique=True, index=True)

    # Relationships
    mahasiswa: List["Mahasiswa"] = Relationship(back_populates="academic_year")
    peminatan: List["Peminatan"] = Relationship(back_populates="academic_year")
    keketatan: List["Keketatan"] = Relationship(back_populates="academic_year")
