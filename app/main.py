from fastapi import FastAPI

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