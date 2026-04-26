from fastapi import FastAPI
from app.services.report_service import get_revenue

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/reports/revenue")
def revenue():
    return {"revenue": get_revenue()}
