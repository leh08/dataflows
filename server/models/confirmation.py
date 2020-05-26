from uuid import uuid4
from time import time
from database import Base, db_session
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

CONFIRMATION_EXPIRATION_DELTA =  1800


class ConfirmationModel(Base):
    __tablename__ = "confirmations"
    
    id = Column(String(50), primary_key=True)
    expire_at = Column(Integer, nullable=False)
    confirmed = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel")
    
    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA
        self.confirmed = False
        
    @classmethod
    def find_by_id(cls, _id: str) -> "ConfirmationModel":
        return cls.query.filter_by(id=_id).first()
    
    @property
    def expired(self) -> bool:
        return time() > self.expire_at
    
    def force_to_expire(self) -> None:
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_db()
            
    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()
        
    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()