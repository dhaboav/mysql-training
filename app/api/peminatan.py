from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.academic_year import get_academic_year, get_academic_year_by_year
from app.core.db import SessionDep
from app.models.peminatan import Peminatan
from app.schemes import Message, PeminatanBase, PeminatanCreate, PeminatanUpdate

router = APIRouter(prefix="/peminatan", tags=["Peminatan"])


def get_peminatan_by_id(session: SessionDep, id: int) -> Peminatan:
    """
    Utility function to get peminatan data by id.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of peminatan.

    Return:
        Peminatan: Information about peminatan data from database.

    Raises:
        HTTPException: HTTP 404 Not Found if data dont exists.
    """
    db_peminatan = session.get(Peminatan, id)
    if not db_peminatan:
        raise HTTPException(status_code=404, detail="Peminatan data not found")
    return db_peminatan


@router.post("/", response_model=Message, status_code=201)
def create_new_peminatan(session: SessionDep, request: PeminatanCreate):
    """
    Endpoint to create a new peminatan entry.

    Args:
        session (SessionDep): Database session dependency.
        request (PeminatanCreate): Scheme that contain data about peminatan.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if peminatan already exists.
    """
    academic_year = get_academic_year_by_year(session, request.tahun)
    db_obj = Peminatan.model_validate(request)
    db_obj.academic_year_id = academic_year.id

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="Peminatan added successfully")


@router.get("/")
def get_all_peminatan(session: SessionDep) -> list:
    """
    Endpoint to get all peminatan data.

    Args:
        session (SessionDep): Database session dependency.

    Return:
        list: Information about all peminatan data from database.
    """
    stmt = select(Peminatan)
    db_objs = session.exec(stmt).all()
    peminatan_list = []

    for peminatan_obj in db_objs:
        academic_year = get_academic_year(session, peminatan_obj.academic_year_id)
        peminatan_dict = peminatan_obj.model_dump(exclude="academic_year_id")
        peminatan_dict["tahun"] = academic_year.year if academic_year else None
        peminatan_list.append(peminatan_dict)

    return peminatan_list


@router.get("/{id}")
def get_peminatan(session: SessionDep, id: int) -> PeminatanBase:
    """
    Endpoint to get peminatan data by id.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of the peminatan data that to get.
    Return:
        PeminatanBase: Information about peminatan data from database.
    """
    peminatan_obj = get_peminatan_by_id(session, id)
    academic_year = get_academic_year(session, peminatan_obj.academic_year_id)
    peminatan_dict = peminatan_obj.model_dump()
    peminatan_dict["tahun"] = academic_year.year if academic_year else None
    return peminatan_dict


@router.patch("/{id}")
def update_peminatan(session: SessionDep, id: int, request: PeminatanUpdate):
    """
    Endpoint to update peminatan data.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of the peminatan that to update.
        request (PeminatanUpdate): Scheme to update peminatan data.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if NIM already exists.
    """
    db_obj = get_peminatan_by_id(session, id)
    update_data = request.model_dump(exclude_unset=True)
    if "tahun" in update_data:
        tahun = update_data.pop("tahun")
        academic_year = get_academic_year_by_year(session, tahun)
        db_obj.academic_year_id = academic_year.id

    db_obj.sqlmodel_update(update_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="Peminatan updated successfully")


@router.delete("/{id}")
def delete_peminatan(session: SessionDep, id: int):
    """
    Endpoint to delete peminatan data.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of the peminatan data that to delete.

    Return:
        Message: detail for API Response.
    """
    db_obj = get_peminatan_by_id(session, id)
    session.delete(db_obj)
    session.commit()
    return Message(detail="Peminatan data deleted successfully")
