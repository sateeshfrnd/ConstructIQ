from pydantic import BaseModel

class SteelExpenses(BaseModel):
    delivery_date: str
    construction_stage: str
    vendor_name: str
    steel_type: str
    size: str
    num_bundles: int
    price_per_bundle: float
    total_weight: float
    driver_amount: float
    total_amount: float
    payment_amount: float
    payment_mode: str
    payment_date: str