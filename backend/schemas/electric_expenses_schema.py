from pydantic import BaseModel

class ElectricExpenses(BaseModel):
    expense_date: str
    construction_stage: str
    category : str
    vendor: str
    amount : int    
    payment_mode: str
    description : str

        
