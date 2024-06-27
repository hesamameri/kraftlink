from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    user_type = Column(String)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define one-to-one relationships
    consumer = relationship("ConsumerTable", uselist=False, back_populates="user")
    manufacturer = relationship("ManufacturerTable", uselist=False, back_populates="user")
    installer = relationship("InstallerTable", uselist=False, back_populates="user")

class ConsumerTable(Base):
    __tablename__ = "consumers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    address = Column(String)
    phone_number = Column(String)
    user = relationship("UserTable", back_populates="consumer")

class ManufacturerTable(Base):
    __tablename__ = "manufacturers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company_name = Column(String)
    industry = Column(String)
    user = relationship("UserTable", back_populates="manufacturer")

class InstallerTable(Base):
    __tablename__ = "installers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    service_area = Column(String)
    experience_years = Column(Integer)
    user = relationship("UserTable", back_populates="installer")



# New tables
class AccountsTable(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(255))
    surname = Column(String(255))
    company_name = Column(String(255))
    balance_nok = Column(DECIMAL(15, 2))
    register_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    bank_card_number = Column(String(20))
    bank = Column(String(255))
    cvv = Column(String(3))

class SharesTable(Base):
    __tablename__ = "shares"
    id = Column(Integer, primary_key=True, index=True)
    amount_nok = Column(DECIMAL(15, 2))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    project_id = Column(Integer)
    percentage_share = Column(DECIMAL(5, 2))
    profit_margin = Column(DECIMAL(5, 2))
    register_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))