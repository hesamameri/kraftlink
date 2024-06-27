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

    shares = relationship("SharesTable", back_populates="account")

class SharesTable(Base):
    __tablename__ = "shares"
    id = Column(Integer, primary_key=True, index=True)
    amount_nok = Column(DECIMAL(15, 2))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    percentage_share = Column(DECIMAL(5, 2))
    profit_margin = Column(DECIMAL(5, 2))
    register_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    account = relationship("AccountsTable", back_populates="shares")
    project = relationship("ProjectsTable", back_populates="shares")


class ProjectsTable(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    share_id = Column(Integer, ForeignKey('shares.id'))
    installer_id = Column(Integer, ForeignKey('installers.id'))
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
    location = Column(String)
    name = Column(String(255))
    type_of_facility = Column(String(255))
    capacity = Column(DECIMAL(10, 2))
    realtime_electricity_generation = Column(DECIMAL(10, 2))
    number_of_shares = Column(Integer)
    cost_nok = Column(DECIMAL(15, 2))
    money_required = Column(DECIMAL(15, 2))
    money_spent = Column(DECIMAL(15, 2))
    money_left = Column(DECIMAL(15, 2))
    electricity_generation_prediction = Column(String)
    manufacturer_status = Column(String(50))
    installer_status = Column(String(50))
    funded_status = Column(String(50))
    register_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    shares = relationship("SharesTable", back_populates="project")
    installer = relationship("InstallerTable", back_populates="projects")
    manufacturer = relationship("ManufacturerTable", back_populates="projects")
    products = relationship("ProductsTable", back_populates="project")

class ProductsTable(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    name = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.id'))
    register_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    manufacturer = relationship("ManufacturerTable", back_populates="products")
    project = relationship("ProjectsTable", back_populates="products")
    category = relationship("CategoriesTable", back_populates="products")
    images = relationship("ImagesTable", back_populates="product")

class CategoriesTable(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    register_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    products = relationship("ProductsTable", back_populates="category")
    images = relationship("ImagesTable", back_populates="category")

class ImagesTable(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    register_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    category = relationship("CategoriesTable", back_populates="images")
    product = relationship("ProductsTable", back_populates="images")
