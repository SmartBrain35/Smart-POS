from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Enum for Stock Type
class StockType(enum.Enum):
    RETAIL = "retail"
    WHOLESALE = "wholesale"

# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(100))
    role = Column(String(50), default="staff")  # staff, admin
    created_at = Column(DateTime, default=datetime.utcnow)

# Employee Model
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    position = Column(String(50))
    salary = Column(Float, default=0.0)
    date_hired = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)

# Stock Model
class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100))
    stock_type = Column(Enum(StockType), nullable=False)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    min_quantity_alert = Column(Integer, default=5)  # for low stock alert
    created_at = Column(DateTime, default=datetime.utcnow)

    def is_low_stock(self):
        return self.quantity <= self.min_quantity_alert

# Transaction Model
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock.id'))
    quantity = Column(Integer, default=1)
    total_cost = Column(Float)  # cost_price * quantity
    total_sell = Column(Float)  # selling_price * quantity
    profit = Column(Float)
    transaction_type = Column(String(50), default="sale")  # sale, return
    created_at = Column(DateTime, default=datetime.utcnow)

    stock = relationship("Stock")

# Report Model (optional for future reporting)
class Report(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    report_type = Column(String(50))  # daily, monthly, yearly
    total_sales = Column(Float)
    total_profit = Column(Float)
    generated_at = Column(DateTime, default=datetime.utcnow)
