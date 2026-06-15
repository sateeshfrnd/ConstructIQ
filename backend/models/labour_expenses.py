from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import LABOUR_EXPENSES_TABLE


class Labour_Expenses(Base):
    __tablename__ = LABOUR_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    payment_date = Column(String)
    construction_stage = Column(String(100))
    labour_type=Column(String(100))
    paid_to= Column(String)
    description = Column(String)
    reference = Column(String)
    payment_amount = Column(Float)
    payment_mode = Column(String)
    