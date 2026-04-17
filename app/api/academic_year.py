"""API for academic year.
Features:
    - get_academic_year_by_year: Utility to get academic year data by year.
    - get_academic_year: Utility to get academic year data by ID.
    - [POST] add_new_academic_year: API to create the academic data.
    - [DEL] delete_academic_year: API to delete the academic data.
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.db import SessionDep
from app.models.academic_year import AcademicYear
from app.schemes import AcademicYearBase, Message

router = APIRouter(prefix="/academicYear", tags=["Academic Year"])


def get_academic_year_by_year(
    session: SessionDep, year: int, is_add: bool = False
) -> AcademicYear:
    """
    Utility function to get academic year by year.

    Args:
        session (SessionDep): Database session dependency.
        year (int): Year of academic.
        is_add (bool): Default is False, for adding new data.

    Return:
        AcademicYear: Information about academic year data from database.

    Raises:
        HTTPException: HTTP 400 Not Found if academic year not found dont exists.
    """
    stmt = select(AcademicYear).where(AcademicYear.year == year)
    is_valid = session.exec(stmt).first()
    if not is_valid and not is_add:
        raise HTTPException(status_code=400, detail="Academic year not found")

    return is_valid


def get_academic_year(session: SessionDep, id: int) -> AcademicYear:
    """
    Utility function to get academic year.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of data.

    Return:
        AcademicYear: Information about academic year data from database.

    Raises:
        HTTPException: HTTP 404 Not Found if data dont exists.
    """
    db_obj = session.get(AcademicYear, id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_obj


@router.post("/")
def add_new_academic_year(session: SessionDep, request: AcademicYearBase):
    """
    Endpoint to create a new academic year entry.

    Args:
        session (SessionDep): Database session dependency.
        request (AcademicYearBase): Scheme to create a new academic year entry.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if academic year already exists.
    """
    is_year = get_academic_year_by_year(session, request.year, is_add=True)
    if is_year:
        raise HTTPException(
            status_code=400,
            detail="The year already exists",
        )
    db_obj = AcademicYear.model_validate(request)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="Academic year added successfully")


@router.delete("/{year}")
def delete_academic_year(session: SessionDep, year: int):
    """
    Endpoint to delete academic year data.

    Args:
        session (SessionDep): Database session dependency.
        year (int): ID of the academic year that to delete.

    Return:
        Message: detail for API Response.
    """
    db_obj = get_academic_year_by_year(session, year)
    session.delete(db_obj)
    session.commit()
    return Message(detail="Academic year deleted successfully")
