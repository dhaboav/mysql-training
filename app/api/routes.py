"""Routes for API access.
Routers:
    - academic_year
    - mahasiswa
    - peminatan
"""

from fastapi import APIRouter

from app.api import academic_year, mahasiswa, peminatan

router = APIRouter()
router.include_router(academic_year.router)
router.include_router(mahasiswa.router)
router.include_router(peminatan.router)
