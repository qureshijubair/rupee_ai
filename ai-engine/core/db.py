import os
import logging
from sqlmodel import Field, SQLModel, create_engine, Session
from uuid import UUID
import pytz
from datetime import datetime
from sqlalchemy import MetaData
import uuid

# PostgreSQL connection details (replace these with your actual credentials)
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')

# Use our custom logger defined in main.py
logger = logging.getLogger("ai_engine_logger")

# Construct the PostgreSQL URL
postgres_url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create engine for PostgreSQL
engine = create_engine(postgres_url)

# Define Kolkata timezone
kolkata_tz = pytz.timezone('Asia/Kolkata')

# Callable function to return the current time in Kolkata timezone
def get_kolkata_time():
  return datetime.now(kolkata_tz)

def get_session():
  with Session(engine) as session:
    yield session

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

# Define the metadata with schema 'ai_engine'
metadata = MetaData(schema="ai_engine")

class Conversation(SQLModel, table=True):
  # Optional, if you want to specify the table name
  __tablename__ = "conversations"  
  # Specify the schema name
  __table_args__ = {"schema": "ai_engine"}

  conversation_id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
  message_id: str = Field(nullable=False)
  message: str | None = Field(default=None)
  platform: str | None = Field(default=None)
  author: str = Field(nullable=False)
  conversation_metadata: str | None = Field(default=None)  # Renamed from 'metadata'
  created_on: datetime = Field(default_factory=get_kolkata_time, nullable=False)
  updated_on: datetime | None = Field(default=None)