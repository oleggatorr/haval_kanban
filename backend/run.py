import uvicorn
from src.config.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )