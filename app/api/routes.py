"""Routes for API access.
Routers:
    - academic_year
    - mahasiswa
"""

from fastapi import APIRouter

from app.api import academic_year, mahasiswa

router = APIRouter()
router.include_router(academic_year.router)
router.include_router(mahasiswa.router)
