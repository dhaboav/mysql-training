"""Schemes for Keketatan.
Features:
    - KeketatanBase: The base model for keketatan.
    - KeketatanCreate: Schemes for creating keketatan.
    - KeketatanUpdate: Schemes for updating keketatan.
"""

from typing import Optional

from sqlmodel import Field, SQLModel

from app.utils import get_current_year_utc


class KeketatanBase(SQLModel):
    """Base model for keketatan"""

    tahun: int = Field(ge=1950, le=get_current_year_utc())
    tampung: int
    realisasi: int


class KeketatanCreate(KeketatanBase):
    """Scheme for create keketatan"""

    pass


class KeketatanUpdate(SQLModel):
    """Scheme for update keketatan"""

    tahun: Optional[int] = Field(default=None, ge=1950, le=get_current_year_utc())
    tampung: Optional[int] = None
    realisasi: Optional[int] = None
