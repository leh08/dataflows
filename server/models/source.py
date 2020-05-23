from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class SourceModel(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    authentications = relationship(
        'AuthenticationModel', lazy='dynamic', cascade="all, delete-orphan"
    )