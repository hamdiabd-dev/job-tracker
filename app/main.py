from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

app = FastAPI(
    title="Job Tracker API",
    description="API for tracking job applications",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "name": "Job Tracker API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
async def health_db(db: AsyncSession = Depends(get_db)):
    """Verify the database connection by running SELECT 1."""
    result = await db.execute(text("SELECT 1"))
    value = result.scalar()
    return {"status": "ok", "database": "connected", "test_query": value}