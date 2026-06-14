from pydantic import BaseModel

class BricksExpenses(BaseModel):
    purchase_date: str
    construction_stage: str
    vendor_name: str
    brick_size: str
    quantity: int
    price_per_brick : float
    driver_amount : float
    total_amount : float
    payment_amount : float       
    payment_mode: str
    payment_date: str

   