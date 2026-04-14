from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.routes.mahasiswa import router
from app.schemes.message import Message

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health-check", response_model=Message)
def health_check() -> Message:
    """Endpoint for health check"""
    return Message(detail="All system online")
