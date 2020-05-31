from typing import List
from database import Base, db_session
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz


class AuthorizationModel(Base):
    __tablename__ = 'authorizations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now(tz=pytz.timezone("NZ"))) # the current timestamp
    credential = Column(JSON)
    
    source_id = Column(Integer, ForeignKey('sources.id'))
    source = relationship("SourceModel")
    
    @classmethod
    def find_by_id(cls, _id: int) -> "AuthorizationModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_name(cls, name: str) -> "AuthorizationModel":
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_all(cls) -> List["AuthorizationModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()
        
    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()