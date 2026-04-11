"""Models and schemes for FastAPI application.

This module provides reusable models and schemes for database and routes in application.

Features:
    - MahasiswaBase: The base model for mahasiswa.
    - MahasiswaUpdate: Schemes for updating mahasiswa.
    - Mahasiswa: The model for database usage.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    """Utility Function for UTC timezone"""
    return datetime.now(timezone.utc)


class SexsEnum(str, Enum):
    """Enums for sexs"""

    L = "L"
    P = "P"


class MahasiswaBase(SQLModel):
    """Base model for mahasiswa"""

    nama: str = Field(description="Full name of the student as per KTP")
    NIM: str = Field(
        description="11-digit Student Identification Number",
        min_length=11,
        max_length=11,
    )
    sex: SexsEnum = Field(description="L for Laki-laki, and P for Perempuan")


class MahasiswaUpdate(SQLModel):
    """Scheme for update mahasiswa"""

    nama: Optional[str] = None
    NIM: Optional[str] = Field(default=None, min_length=11, max_length=11)
    sex: Optional[SexsEnum] = None


class Mahasiswa(MahasiswaBase, table=True):
    """Model for database mahasiswa table"""

    NIM: Optional[str] = Field(
        default=None,
        primary_key=True,
        min_length=11,
        max_length=11,
        description="Nomor Induk Mahasiswa (11 digits)",
    )
    created_at: Optional[datetime] = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
    )
