import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, Boolean, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()
url = os.getenv("DATABASE_URL")
engine = create_engine(url)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class LaunchDB(Base):
    __tablename__ = "launches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sentiment = Column(Float)
    sentiment_label = Column(String)
    details = Column(String)
    success = Column(Boolean)
    created_time=Column(DateTime, default=datetime.utcnow)

class LaunchErrorDB(Base):
    __tablename__ = "launch_error"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sentiment = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)
    details = Column(String)
    success = Column(Boolean)
    created_time = Column(DateTime, default=datetime.utcnow)
    error_message = Column(String)
    raw_data = Column(String)
