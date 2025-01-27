from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Replace this with your actual database URL
DATABASE_URL = "mysql+pymysql://root:neural@123@localhost/sam_database"

# Create a synchronous engine
engine = create_engine(DATABASE_URL)

# Create a synchronous sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)
