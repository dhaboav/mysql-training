from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.academic_year import get_academic_year, get_academic_year_by_year
from app.core.db import SessionDep
from app.models import Keketatan
from app.schemes import KeketatanBase, KeketatanCreate, KeketatanUpdate, Message

router = APIRouter(prefix="/keketatan", tags=["Keketatan"])


def get_keketatan_by_id(session: SessionDep, id: int) -> Keketatan:
    """
    Utility function to get keketatan data by id.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of keketatan.

    Return:
        Keketatan: Information about keketatan data from database.

    Raises:
        HTTPException: HTTP 404 Not Found if data dont exists.
    """
    db_keketatan = session.get(Keketatan, id)
    if not db_keketatan:
        raise HTTPException(status_code=404, detail="keketatan data not found")
    return db_keketatan


@router.post("/", response_model=Message, status_code=201)
def create_new_keketatan(session: SessionDep, request: KeketatanCreate):
    """
    Endpoint to create a new keketatan entry.

    Args:
        session (SessionDep): Database session dependency.
        request (KeketatanCreate): Scheme that contain data about keketatan.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if keketatan already exists.
    """
    academic_year = get_academic_year_by_year(session, request.tahun)
    db_obj = Keketatan.model_validate(request)
    db_obj.academic_year_id = academic_year.id

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="keketatan added successfully")


@router.get("/")
def get_all_keketatan(session: SessionDep) -> list:
    """
    Endpoint to get all keketatan data.

    Args:
        session (SessionDep): Database session dependency.

    Return:
        list: Information about all keketatan data from database.
    """
    stmt = select(Keketatan)
    db_objs = session.exec(stmt).all()
    keketatan_list = []

    for keketatan_obj in db_objs:
        academic_year = get_academic_year(session, keketatan_obj.academic_year_id)
        keketatan_dict = keketatan_obj.model_dump(exclude="academic_year_id")
        keketatan_dict["tahun"] = academic_year.year if academic_year else None
        keketatan_list.append(keketatan_dict)

    return keketatan_list


@router.get("/{id}")
def get_keketatan(session: SessionDep, id: int) -> KeketatanBase:
    """
    Endpoint to get keketatan data by id.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of the keketatan data that to get.
    Return:
        KeketatanBase: Information about keketatan data from database.
    """
    keketatan_obj = get_keketatan_by_id(session, id)
    academic_year = get_academic_year(session, keketatan_obj.academic_year_id)
    keketatan_dict = keketatan_obj.model_dump()
    keketatan_dict["tahun"] = academic_year.year if academic_year else None
    return keketatan_dict


@router.patch("/{id}")
def update_keketatan(session: SessionDep, id: int, request: KeketatanUpdate):
    """
    Endpoint to update keketatan data.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of the keketatan that to update.
        request (KeketatanUpdate): Scheme to update keketatan data.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if NIM already exists.
    """
    db_obj = get_keketatan_by_id(session, id)
    update_data = request.model_dump(exclude_unset=True)
    if "tahun" in update_data:
        tahun = update_data.pop("tahun")
        academic_year = get_academic_year_by_year(session, tahun)
        db_obj.academic_year_id = academic_year.id

    db_obj.sqlmodel_update(update_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="keketatan updated successfully")


@router.delete("/{id}")
def delete_keketatan(session: SessionDep, id: int):
    """
    Endpoint to delete keketatan data.

    Args:
        session (SessionDep): Database session dependency.
        id (int): ID of the keketatan data that to delete.

    Return:
        Message: detail for API Response.
    """
    db_obj = get_keketatan_by_id(session, id)
    session.delete(db_obj)
    session.commit()
    return Message(detail="keketatan data deleted successfully")
