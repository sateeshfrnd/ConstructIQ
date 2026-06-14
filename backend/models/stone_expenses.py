from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import STONE_EXPENSES_TABLE


class Stone_Expenses(Base):
    __tablename__ = STONE_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    delivery_date = Column(String)
    construction_stage = Column(String(100))
    vendor_name=Column(String(100))
    stone_type = Column(String)
    num_of_trucks = Column(Integer)
    cost_per_trucks = Column(Float)
    total_weight= Column(Float)
    driver_amount = Column(Float)
    total_amount = Column(Float)
    payment_amount = Column(Float)
    payment_mode = Column(String(50))
    payment_date = Column(String)