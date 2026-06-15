from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date

from database.db import Base
from utils.constants import PAINTING_EXPENSES_TABLE


class Painting_Expenses(Base):
    __tablename__ = PAINTING_EXPENSES_TABLE
    id = Column(Integer, primary_key=True, index=True)
    expense_date = Column(String)
    category = Column(String)
    construction_stage = Column(String(100))
    vendor=Column(String(100))
    amount=Column(Integer)
    mode = Column(String(50))
    description= Column(String)