"""Model for mahasiswa.
Features:
    - Mahasiswa: The model for database usage.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.enum import ReligionsEnum, SexsEnum
from app.utils import get_datetime_utc

if TYPE_CHECKING:
    from app.models.academic_year import AcademicYear


class Mahasiswa(SQLModel, table=True):
    """Model for database mahasiswa table"""

    __tablename__ = "mahasiswa"

    NIM: str = Field(primary_key=True, max_length=11)
    nama: str
    sex: SexsEnum
    agama: ReligionsEnum
    angkatan: Optional[int] = Field(default=None, foreign_key="academic_year.id")
    created_at: datetime = Field(default_factory=get_datetime_utc)
    updated_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_column_kwargs={"onupdate": get_datetime_utc},
    )

    # Relationships
    academic_year: Optional["AcademicYear"] = Relationship(back_populates="mahasiswa")
