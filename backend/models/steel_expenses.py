from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import STEEL_EXPENSES_TABLE

class Steel_Expenses(Base):
    __tablename__ = STEEL_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    delivery_date = Column(String)
    construction_stage = Column(String(100))
    vendor_name=Column(String(100))
    steel_type = Column(String)
    size = Column(String)
    num_bundles = Column(Integer)
    price_per_bundle = Column(Float)
    total_weight= Column(Float)
    driver_amount = Column(Float)
    total_amount = Column(Float)
    payment_amount = Column(Float)
    payment_mode = Column(String(50))
    payment_date = Column(String)