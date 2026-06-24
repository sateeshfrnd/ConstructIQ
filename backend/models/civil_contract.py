from sqlalchemy import Column, Integer, String, Float
from database.db import Base


class Civil_Contract(Base):
    __tablename__ = "civil_contract"
    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(200))
    total_sqft = Column(Float)
    rate_per_chadara = Column(Float)
    no_of_floors = Column(Integer)
    total_chadaras = Column(Float)
    total_contract_cost = Column(Float)
    milestone_percentage = Column(Float, default=70.0)
    no_of_partitions = Column(Integer, default=5)
    cost_per_partition = Column(Float)
    notes = Column(String(500))


class Civil_Contract_Payments(Base):
    __tablename__ = "civil_contract_payments"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, index=True)
    payment_date = Column(String)
    construction_stage = Column(String(100))
    description = Column(String(500))
    payment_mode = Column(String(50))
    amount_paid = Column(Float)


class Civil_Contract_Stages(Base):
    __tablename__ = "civil_contract_stages"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, index=True)
    stage_name = Column(String(100))
    stage_type = Column(String(50))  # "structure" or "plastering" or "additional"
    expected_amount = Column(Float)
