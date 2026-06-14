from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import SAND_EXPENSES_TABLE


class Sand_Expenses(Base):
    __tablename__ = SAND_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    delivery_date = Column(String)
    construction_stage = Column(String(100))
    sand_type = Column(String)
    vendor_name=Column(String(100))
    cost_per_truck= Column(Float)
    no_of_trucks = Column(Integer)
    driver_amount = Column(Float)
    total_amount = Column(Float)
    payment_amount = Column(Float)
    payment_mode = Column(String(50))
    payment_date = Column(String)