from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON
from datetime import datetime

import pytz


class AuthenticationModel(Base):
    __tablename__ = 'authentications'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now(tz=pytz.timezone("NZ"))) # the current timestamp
    credential = Column(JSON)
    source_id = Column(Integer, ForeignKey('sources.id'))