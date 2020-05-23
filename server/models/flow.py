from typing import List
from database import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class FlowModel(Base):
    __tablename__ = "flows"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    report = Column(String(80))
    
    user_id = Column(Integer, ForeignKey("users.id"))
    
    logs = relationship('LogModel', lazy="dynamic")
        
    @classmethod
    def find_by_id(cls, _id: int) -> "FlowModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str) -> "FlowModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["FlowModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()

    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()
