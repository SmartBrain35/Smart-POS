from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True, max_length=50)
    password: str = Field(nullable=False, max_length=200)
    email: str | None = Field(default=None, max_length=100)
    role: str = Field(default="staff", max_length=50)  # staff, admin
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Employee(SQLModel, table=True):
    __tablename__ = 'employees'

    id: int | None = Field(default=None, primary_key=True)
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    position: str | None = Field(default=None, max_length=50)
    salary: float = Field(default=0.0)
    date_hired: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active: bool = Field(default=True)


class Stock(SQLModel, table=True):
    __tablename__ = 'stocks'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    category: str | None = Field(default=None, max_length=100)
    stock_type: str = Field(default="wholesale", max_length=50, nullable=False)  # wholesale, retail
    cost_price: float = Field(nullable=False)
    sell_price: float = Field(nullable=False)
    quantity: int = Field(default=0)
    min_quantity_alert: int = Field(default=5)  # for low stock alert
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    transactions: list["Transaction"] = Relationship(back_populates="stock")


class Transaction(SQLModel, table=True):
    __tablename__ = 'transactions'

    id: int | None = Field(default=None, primary_key=True)
    stock_id: int | None = Field(default=None, foreign_key="stocks.id")
    quantity: int = Field(default=1)
    total_cost: float | None = None  # cost_price * quantity
    total_sell: float | None = None  # selling_price * quantity
    profit: float | None = None
    transaction_type: str = Field(default="sale", max_length=50)  # sale, return
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    stock: Stock | None = Relationship(back_populates="transactions")


class Report(SQLModel, table=True):
    __tablename__ = 'reports'

    id: int | None = Field(default=None, primary_key=True)
    report_type: str | None = Field(default=None, max_length=50)  # daily, monthly, yearly
    total_sales: float | None = None
    total_profit: float | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
