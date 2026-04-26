from pydantic import BaseModel

class ReportItem(BaseModel):
    user_id: int
    total_spent: float
