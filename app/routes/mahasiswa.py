from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.db import SessionDep
from app.models.mahasiswa import Mahasiswa
from app.schemes.mahasiswa import MahasiswaCreate, MahasiswaUpdate
from app.schemes.message import Message

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
def create_new_mahasiswa(
    session: SessionDep, mahasiswa_data: MahasiswaCreate
) -> Message:
    """
    Endpoint to create a new mahasiswa entry.

    Args:
        session (SessionDep): Database session dependency.
        mahasiswa_data (MahasiswaBase): Mahasiswa scheme that contain data about mahasiswa.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if mahasiswa already exists.
    """
    existing_mhs = session.get(Mahasiswa, mahasiswa_data.NIM)
    if existing_mhs:
        raise HTTPException(
            status_code=400,
            detail=f"The data already exists for NIM {mahasiswa_data.NIM}",
        )
    db_obj = Mahasiswa.model_validate(mahasiswa_data)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return Message(detail="Mahasiswa added successfully")


@router.get("/")
def get_all_mahasiswa(session: SessionDep):
    """
    Endpoint to get all mahasiswa data.

    Args:
        session (SessionDep): Database session dependency.
    """
    stmt = select(Mahasiswa)
    return session.exec(stmt).all()


@router.get("/{NIM}")
def get_mahasiswa(session: SessionDep, NIM: str) -> Mahasiswa:
    """
    Endpoint to get mahasiswa data by NIM.

    Args:
        session (SessionDep): Database session dependency.
        NIM (str): ID of the mahasiswa that to get.
    Return:
        Mahasiswa: Information about mahasiswa data from database.
    """
    mahasiswa_data = get_mahasiswa_by_nim(session, NIM)
    return {
        "NIM": mahasiswa_data.NIM,
        "nama": mahasiswa_data.nama,
        "sex": mahasiswa_data.sex,
        "agama": mahasiswa_data.agama,
        "angkatan": (
            mahasiswa_data.academic_year.year if mahasiswa_data.academic_year else None
        ),
    }


@router.patch("/{NIM}", response_model=Message)
def update_mahasiswa(
    session: SessionDep, NIM: str, mahasiswa_data_in: MahasiswaUpdate
) -> Message:
    """
    Endpoint to update mahasiswa data.

    Args:
        session (SessionDep): Database session dependency.
        NIM (str): ID of the mahasiswa that to update.
        mahasiswa_data_in (MahasiswaUpdate): Mahasiswa scheme to update mahasiswa data.

    Return:
        Message: detail for API Response.

    Raises:
        HTTPException: HTTP 400 Bad Request if NIM already exists.
    """
    Mahasiswa = get_mahasiswa_by_nim(session, NIM)
    update_data = mahasiswa_data_in.model_dump(exclude_unset=True)
    Mahasiswa.sqlmodel_update(update_data)
    session.add(Mahasiswa)
    session.commit()
    session.refresh(Mahasiswa)

    return Message(detail="Mahasiswa updated successfully")


@router.delete("/{NIM}")
def delete_Mahasiswa(session: SessionDep, NIM: str) -> Message:
    """
    Endpoint to delete mahasiswa data.

    Args:
        session (SessionDep): Database session dependency.
        NIM (str): ID of the mahasiswa that to delete.

    Return:
        Message: detail for API Response.
    """
    Mahasiswa = get_mahasiswa_by_nim(session, NIM)
    session.delete(Mahasiswa)
    session.commit()
    return Message(detail="Mahasiswa deleted successfully")
