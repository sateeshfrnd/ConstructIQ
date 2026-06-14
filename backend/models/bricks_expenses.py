from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import BRICKS_EXPENSES_TABLE

class Bricks_Expenses(Base):
    __tablename__ = BRICKS_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    purchase_date = Column(String)
    construction_stage = Column(String(100))
    vendor_name = Column(String)
    brick_size = Column(String)
    quantity = Column(Integer)
    price_per_brick = Column(Float)
    driver_amount = Column(Float)
    total_amount = Column(Float)
    payment_amount = Column(Float)
    payment_mode = Column(String(50))
    payment_date = Column(String)