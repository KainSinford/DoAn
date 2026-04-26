from fastapi import FastAPI
from app.api.report import router as report_router

app = FastAPI()

app.include_router(report_router)
