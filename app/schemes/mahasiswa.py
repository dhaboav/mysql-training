"""Schemes for mahasiswa.
Features:
    - MahasiswaBase: The base model for mahasiswa.
    - MahasiswaCreate: Schemes for creating mahasiswa.
    - MahasiswaUpdate: Schemes for updating mahasiswa.
"""

from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.enum import ReligionsEnum, SexsEnum
from app.utils import get_current_year_utc


class MahasiswaBase(SQLModel):
    """Base model for mahasiswa"""

    NIM: str = Field(min_length=11, max_length=11)
    nama: str = Field(min_length=4)
    sex: SexsEnum
    agama: ReligionsEnum
    angkatan: int = Field(ge=1950, le=get_current_year_utc())


class MahasiswaCreate(MahasiswaBase):
    """Scheme for create mahasiswa"""

    pass


class MahasiswaUpdate(SQLModel):
    """Scheme for update mahasiswa"""

    nama: Optional[str] = None
    sex: Optional[SexsEnum] = None
    agama: Optional[ReligionsEnum] = None
    angkatan: Optional[int] = Field(default=None, ge=1950, le=get_current_year_utc())
