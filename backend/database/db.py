from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

username = ""
password = ""
database_name = "construct_iq"

MYSQL_DATABASE_URL = (
    f"mysql+pymysql://{username}:{password}@localhost/{database_name}"
)
DATABASE_URL = (
    f"postgresql://{username}:{password}@ep-rapid-rain-aod99pje-pooler.c-2.ap-southeast-1.aws.neon.tech/{database_name}?sslmode=require&channel_binding=require"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()