"""API for mahasiswa.
Features:
    - get_mahasiswa_by_nim: Utility to get mahasiswa data by NIM.
    - [POST] create_new_mahasiswa: API to create the mahasiswa data.
    - [GET] get_all_mahasiswa: API to get all the mahasiswa data.
    - [GET] get_mahasiswa: API to get the mahasiswa data by NIM.
    - [PATCH] update_mahasiswa: API to update the mahasiswa data by NIM.
    - [DEL] delete_mahasiswa: API to delete the mahasiswa data by NIM.
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.academic_year import get_academic_year, get_academic_year_by_year
from app.core.db import SessionDep
from app.models.mahasiswa import Mahasiswa
from app.schemes import MahasiswaBase, MahasiswaCreate, MahasiswaUpdate, Message

router = APIRouter(prefix="/mahasiswa", tags=["Mahasiswa"])


def get_mahasiswa_by_nim(session: SessionDep, NIM: str) -> Mahasiswa:
    """
    Utility function to get mahasiwa data by NIM.

    Args:
        session (SessionDep): Database session dependency.
        NIM (str): ID of mahasiswa.

    Return:
        Mahasiswa: Information about mahasiswa data from database.

    Raises:
        HTTPException: HTTP 404 Not Found if Mahasiswa dont exists.
    """
    db_mahasiswa = session.get(Mahasiswa, NIM)
    if not db_mahasiswa:
        raise HTTPException(status_code=404, detail="Mahasiswa not found")
    return db_mahasiswa


@router.post("/", response_model=Message, status_code=201)
def create_new_mahasiswa(session: SessionDep, request: MahasiswaCreate) -> Message:
    """
    Endpoint to create a new mahasiswa entry.

    Args:
        session (SessionDep): Database session dependency.
        request (MahasiswaCreate): Mahasiswa scheme that contain data about mahasiswa.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if mahasiswa already exists.
    """
    existing_mhs = session.get(Mahasiswa, request.NIM)
    if existing_mhs:
        raise HTTPException(
            status_code=400,
            detail=f"The data already exists for NIM {request.NIM}",
        )

    academic_year = get_academic_year_by_year(session, request.angkatan)
    db_obj = Mahasiswa.model_validate(request)
    db_obj.academic_year_id = academic_year.id

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="Mahasiswa added successfully")


@router.get("/")
def get_all_mahasiswa(session: SessionDep) -> list:
    """
    Endpoint to get all mahasiswa data.

    Args:
        session (SessionDep): Database session dependency.

    Return:
        list: Information about all mahasiswa data from database.
    """
    stmt = select(Mahasiswa)
    db_objs = session.exec(stmt).all()
    mahasiswa_list = []

    for mahasiswa_obj in db_objs:
        academic_year = get_academic_year(session, mahasiswa_obj.academic_year_id)
        mahasiswa_dict = mahasiswa_obj.model_dump(exclude="academic_year_id")
        mahasiswa_dict["angkatan"] = academic_year.year if academic_year else None
        mahasiswa_list.append(mahasiswa_dict)

    return mahasiswa_list


@router.get("/{NIM}")
def get_mahasiswa(session: SessionDep, NIM: str) -> MahasiswaBase:
    """
    Endpoint to get mahasiswa data by NIM.

    Args:
        session (SessionDep): Database session dependency.
        NIM (str): ID of the mahasiswa that to get.
    Return:
        MahasiswaBase: Information about mahasiswa data from database.
    """
    mahasiswa_obj = get_mahasiswa_by_nim(session, NIM)
    academic_year = get_academic_year(session, mahasiswa_obj.academic_year_id)
    mahasiswa_dict = mahasiswa_obj.model_dump()
    mahasiswa_dict["angkatan"] = academic_year.year if academic_year else None
    return mahasiswa_dict


@router.patch("/{NIM}")
def update_mahasiswa(session: SessionDep, NIM: str, request: MahasiswaUpdate):
    """
    Endpoint to update mahasiswa data.

    Args:
        session (SessionDep): Database session dependency.
        NIM (str): ID of the mahasiswa that to update.
        request (MahasiswaUpdate): Mahasiswa scheme to update mahasiswa data.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if NIM already exists.
    """
    db_obj = get_mahasiswa_by_nim(session, NIM)
    update_data = request.model_dump(exclude_unset=True)
    if "angkatan" in update_data:
        angkatan = update_data.pop("angkatan")
        academic_year = get_academic_year_by_year(session, angkatan)
        db_obj.academic_year_id = academic_year.id

    db_obj.sqlmodel_update(update_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="Mahasiswa updated successfully")


@router.delete("/{NIM}")
def delete_mahasiswa(session: SessionDep, NIM: str):
    """
    Endpoint to delete mahasiswa data.

    Args:
        session (SessionDep): Database session dependency.
        NIM (str): ID of the mahasiswa that to delete.

    Return:
        Message: detail for API Response.
    """
    db_obj = get_mahasiswa_by_nim(session, NIM)
    session.delete(db_obj)
    session.commit()
    return Message(detail="Mahasiswa deleted successfully")
