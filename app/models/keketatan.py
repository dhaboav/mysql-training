"""Model for keketatan.
Features:
    - Keketatan: The model for database usage.
"""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.academic_year import AcademicYear


class Keketatan(SQLModel, table=True):
    """Model for database keketatan table"""

    __tablename__ = "keketatan"

    id: Optional[int] = Field(default=None, primary_key=True)
    academic_year_id: Optional[int] = Field(
        default=None, foreign_key="academic_year.id"
    )
    tampung: int
    realisasi: int

    # Relationships
    academic_year: Optional["AcademicYear"] = Relationship(back_populates="keketatan")
