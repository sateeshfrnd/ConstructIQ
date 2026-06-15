from pydantic import BaseModel

class LabourExpenses(BaseModel):
    payment_date: str
    construction_stage: str
    labour_type: str
    paid_to: str
    description: str
    reference: str
    payment_amount : float       
    payment_mode: str
    