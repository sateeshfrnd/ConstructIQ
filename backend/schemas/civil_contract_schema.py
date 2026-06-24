from pydantic import BaseModel
from typing import Optional, List


class CivilContractCreate(BaseModel):
    vendor_name: str
    total_sqft: float
    rate_per_chadara: float
    no_of_floors: int
    total_chadaras: float
    total_contract_cost: float
    milestone_percentage: float = 70.0
    no_of_partitions: int = 5
    cost_per_partition: float
    notes: str = ""


class CivilContractPayment(BaseModel):
    contract_id: int
    payment_date: str
    construction_stage: str
    description: str
    payment_mode: str
    amount_paid: float


class CivilContractStage(BaseModel):
    contract_id: int
    stage_name: str
    stage_type: str
    expected_amount: float


class CivilContractStagesList(BaseModel):
    stages: List[CivilContractStage]
