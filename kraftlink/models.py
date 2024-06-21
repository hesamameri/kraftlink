from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    user = relationship("UserTable", back_populates="consumer")

class ManufacturerTable(Base):
    __tablename__ = "manufacturers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserTable", back_populates="manufacturer")

class InstallerTable(Base):
    __tablename__ = "installers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserTable", back_populates="installer")
