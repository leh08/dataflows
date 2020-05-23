from typing import List
from database import Base, db_session
from sqlalchemy import Column, Integer, String, ForeignKey


class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    flow_id = Column(Integer, ForeignKey("flows.id"), nullable=False)

    @classmethod
    def find_by_name(cls, name: str) -> "LogModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["LogModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db_session.add(self)
        db_session.commit()

    def delete_from_db(self) -> None:
        db_session.delete(self)
        db_session.commit()
