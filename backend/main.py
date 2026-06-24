from fastapi import FastAPI

from database.db import Base
from database.db import engine
from models.user import User
from models.cement_expenses import Cement_Expenses
from models.steel_expenses import Steel_Expenses
from models.bricks_expenses import Bricks_Expenses
from models.sand_expenses import Sand_Expenses
from models.stone_expenses import Stone_Expenses
from models.labour_expenses import Labour_Expenses
from models.electric_expenses import Electric_Expenses
from models.plumbing_expenses import Plumbing_Expenses
from models.painting_expenses import Painting_Expenses
from models.civil_contract import Civil_Contract, Civil_Contract_Payments, Civil_Contract_Stages
from routers import(
     auth, 
     site_expenses, 
     steel_expenses, 
     cement_expenses,
     bricks_expenses,
     sand_expenses,
     stone_expenses,
     labour_expenses,
     electric_expenses,
     plumbing_expenses,
     painting_expenses,
     bulk_load,
     dashboard,
     crud_operations,
     civil_contract
)

# Here it will create the tables in the database if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(site_expenses.router)
app.include_router(steel_expenses.router)
app.include_router(cement_expenses.router)
app.include_router(bricks_expenses.router)
app.include_router(sand_expenses.router)
app.include_router(stone_expenses.router)
app.include_router(labour_expenses.router)
app.include_router(electric_expenses.router)
app.include_router(plumbing_expenses.router)
app.include_router(painting_expenses.router)
app.include_router(bulk_load.router)
app.include_router(dashboard.router)
app.include_router(crud_operations.router)
app.include_router(civil_contract.router)