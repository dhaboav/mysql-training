from sqlmodel import SQLModel


class Message(SQLModel):
    """Scheme model for API response"""

    detail: str
