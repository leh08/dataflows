from typing import List
from database import Base, db_session
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey


class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    message = Column(String(80), nullable=False)
    date = Column(DateTime, default=func.now()) # the current timestamp
    status = Column(String)
    
    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False)
    
    @classmethod
    def find_all_by_flow_id(cls, flow_id) -> List["LogModel"]:
        return cls.query.filter_by(flow_id=flow_id).all()

    @classmethod
    def find_by_file(cls, file: str) -> "LogModel":
        return cls.query.filter_by(file=file).first()
    
    @classmethod
    def find_all(cls) -> List["LogModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()

    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()
