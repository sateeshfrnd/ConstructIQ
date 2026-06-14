from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import CEMENT_EXPENSES_TABLE

class Cement_Expenses(Base):
    __tablename__ = CEMENT_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    delivery_date = Column(String)
    construction_stage = Column(String(100))
    vendor_name = Column(String)
    cement_company_name = Column(String)
    price_per_bag = Column(Integer)
    no_of_bags = Column(Integer)
    driver_amount = Column(Float)
    total_amount = Column(Float)
    payment_amount = Column(Float)
    payment_mode = Column(String(50))
    payment_date = Column(String)