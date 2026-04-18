"""Model for peminatan.
Features:
    - Peminatan: The model for database usage.
"""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.enum import JalurEnum

if TYPE_CHECKING:
    from app.models.academic_year import AcademicYear


class Peminatan(SQLModel, table=True):
    """Model for database peminatan table"""

    __tablename__ = "peminatan"

    id: Optional[int] = Field(default=None, primary_key=True)
    jalur: JalurEnum
    peminat: int
    baru: int
    lulus: int
    academic_year_id: Optional[int] = Field(
        default=None, foreign_key="academic_year.id"
    )

    # Relationships
    academic_year: Optional["AcademicYear"] = Relationship(back_populates="peminatan")
