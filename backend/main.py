from fastapi import FastAPI

from database.db import Base
from database.db import engine

from routers import auth

# Here it will create the tables in the database if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)