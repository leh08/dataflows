from typing import List
from database import Base, db_session
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class SourceModel(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    authorizations = relationship(
        'AuthorizationModel', lazy='dynamic', cascade='delete,all'
    )
    
    @classmethod
    def find_by_name(cls, name: str) -> "SourceModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "SourceModel":
        return cls.query.filter_by(id=_id).first()
   
    @classmethod
    def find_all(cls) -> List["SourceModel"]:
        return cls.query.all()

    
    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()

    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()