from fastapi import APIRouter
from app.db.mysql import get_mysql_db
from app.db.postgres import get_postgres_db
from app.services.report_service import generate_report

router = APIRouter()

@router.get("/api/report")
def get_report():
    mysql_db = get_mysql_db()
    postgres_db = get_postgres_db()

    try:
        data = generate_report(mysql_db.bind, postgres_db.bind)
        return {
            "status": "success",
            "data": data
        }
    finally:
        mysql_db.close()
        postgres_db.close()
