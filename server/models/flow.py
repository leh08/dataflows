from typing import List

from database import Base, db_session
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship
from models.log import LogModel


class FlowModel(Base):
    __tablename__ = 'flows'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    report = Column(String, nullable=False)
    profile = Column(String)
    parser_name = Column(String, default="Pandas")
    store_name = Column(String, default="Redshift") # Target: "Redshift", "S3-Only"
    is_model = Column(Boolean, default=False)
    schema = Column(String, default='public')
    load_mode = Column(String, default='Replace') # Load mode: Append, Replace, Upsert
    frequency = Column(String, default='Daily') # Frequency: Daily, Weekly, Minutes, Hours, Days, Weeks
    day_unit = Column(String)
    time_unit = Column(Integer)
    sql_script = Column(String)
    status = Column(String, default='Active')
    created_on = Column(DateTime, default=func.now())

    source_name = Column(String, ForeignKey('sources.name'))
    
    authorization_id = Column(Integer, ForeignKey('authorizations.id'))
    authorization = relationship('AuthorizationModel')
    
    logs = relationship('LogModel', lazy='dynamic', cascade='delete,all')
    
    @property
    def most_recent_log(self) -> "LogModel":
        return self.logs.order_by(LogModel.date.desc()).first()
        
    @classmethod
    def find_by_id(cls, _id: str) -> "FlowModel":
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