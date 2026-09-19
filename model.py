from database import Base
from sqlalchemy import Column, Integer, String


class Account(Base):
	__tablename__ = "accounts"

	id = Column(Integer, primary_key=True)
	owner_name = Column(String, nullable=False)
	balance_cents = Column(Integer, default=0)