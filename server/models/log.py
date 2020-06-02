from typing import List
from database import Base, db_session
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from datetime import datetime

import pytz


class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    file = Column(String)
    message = Column(String(80), nullable=False)
    date = Column(DateTime, default=datetime.now(tz=pytz.timezone("NZ"))) # the current timestamp
    status = Column(String)
    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False)

    @classmethod
    def find_by_file(cls, file: str) -> "LogModel":
        return cls.query.filter_by(file=file).first()
    
    @classmethod
    def find_all(cls, status) -> List["LogModel"]:
        return cls.query.filter_by(status=status).all()

    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()

    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()
