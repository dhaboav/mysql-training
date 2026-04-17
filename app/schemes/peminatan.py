"""Schemes for peminatan.
Features:
    - PeminatanBase: The base model for peminatan.
    - PeminatanCreate: Schemes for creating peminatan.
    - PeminatanUpdate: Schemes for updating peminatan.
"""

from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.enum import JalurEnum
from app.utils import get_current_year_utc


class PeminatanBase(SQLModel):
    """Base model for peminatan"""

    tahun: int = Field(ge=1950, le=get_current_year_utc())
    jalur: JalurEnum
    peminat: int
    lulus: int
    baru: int


class PeminatanCreate(PeminatanBase):
    """Scheme for create peminatan"""

    pass


class PeminatanUpdate(SQLModel):
    """Scheme for update peminatan"""

    tahun: Optional[int] = Field(default=None, ge=1950, le=get_current_year_utc())
    jalur: Optional[JalurEnum] = None
    peminat: Optional[int] = None
    lulus: Optional[int] = None
    baru: Optional[int] = None
