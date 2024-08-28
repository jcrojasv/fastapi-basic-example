import datetime
from sqlalchemy import Column, DateTime, Integer, String
from config.database import Base

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    nature = Column(String(255), index=True)
    project = Column(String(255), index=True)
    path = Column(String(1000), index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)