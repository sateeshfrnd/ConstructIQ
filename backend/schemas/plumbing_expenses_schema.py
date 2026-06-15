from pydantic import BaseModel

class PlumbingExpenses(BaseModel):
    expense_date: str
    category : str
    construction_stage: str
    vendor: str
    amount : float    
    payment_mode: str
    description : str

        
