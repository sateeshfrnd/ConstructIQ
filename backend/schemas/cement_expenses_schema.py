from pydantic import BaseModel

class CementExpenses(BaseModel):
    delivery_date: str
    construction_stage: str
    vendor_name: str
    cement_company_name: str
    price_per_bag : float
    no_of_bags : int
    driver_amount : float
    total_amount : float
    payment_amount : float       
    payment_mode: str
    payment_date: str