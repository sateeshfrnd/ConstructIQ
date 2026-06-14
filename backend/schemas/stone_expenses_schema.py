from pydantic import BaseModel

class StoneExpenses(BaseModel):
    delivery_date: str
    construction_stage: str
    vendor_name: str
    stone_type: str
    cost_per_truck: float
    no_of_trucks: int
    driver_amount: float
    total_amount: float
    payment_amount: float
    payment_mode: str
    payment_date: str
