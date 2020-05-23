from database import Base, db_session
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask import request, url_for
from requests import Response
from services.mailgun import Mailgun
from models.confirmation import ConfirmationModel


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(80), nullable=False, unique=True)
    password = Column(String(80), nullable=False)
    
    confirmation = relationship(
        'ConfirmationModel', lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def most_recent_confirmation(self) -> "ConfirmationModel":
        return self.confirmation.order_by(ConfirmationModel.expire_at.desc()).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()
    
    def send_confirmation_email(self) -> Response:
        link = request.url_root[:-1] + url_for(
            "confirmation", confirmation_id=self.most_recent_confirmation.id
        )
        subject = "Signup Confirmation"
        text = f"Please click the link to confirm your signup: {link}"
        html = f'<html>Please click the link to confirm your signup: <a href="{link}">{link}</a></html>'
        
        return Mailgun.send_email([self.email], subject, text, html)
        
    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()

    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()
