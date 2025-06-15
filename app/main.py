from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="Dentist+ Integration Service",
    description="",
    version="1.0"
)

app.include_router(endpoints.router)
