from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import SITE_EXPENSES_TABLE

class Site_Expenses(Base):
    __tablename__ = SITE_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    expenses_date = Column(String)
    expense_type = Column(String(100))
    expense_category = Column(String(100))
    amount = Column(Float)
    construction_stage = Column(String(100))
    payment_mode = Column(String(50))
    description = Column(String(500))
    notes = Column(String(500))