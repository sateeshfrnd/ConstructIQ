from pydantic import BaseModel

class PaintingExpenses(BaseModel):
    expense_date: str
    category : str
    construction_stage: str
    vendor: str
    amount : int    
    mode: str
    description : str

        
