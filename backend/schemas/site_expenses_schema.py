from pydantic import BaseModel

class SiteExpenses(BaseModel):
    expenses_date: str
    expense_type: str
    expense_category: str
    amount: float
    construction_stage: str
    payment_mode: str
    description: str
    notes: str