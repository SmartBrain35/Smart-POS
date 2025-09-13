from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from sqlalchemy import Column, TEXT


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    CASHIER = "cashier"
    SALES_PERSON = "sales_person"


class EmployeeDesignation(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SALES_REP = "sales_rep"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    MOMO = "momo"


class StockType(str, Enum):
    RETAIL = "retail"
    WHOLESALE = "wholesale"


class DamageStatus(str, Enum):
    LEAKAGE = "leakage"
    BROKEN = "broken"
    EXPIRED = "expired"


class ExpenditureCategory(str, Enum):
    UTILITIES = "utilities"
    SUPPLIES = "supplies"
    SALARIES = "salaries"


class ReturnReason(str, Enum):
    DEFECTIVE = "defective"
    WRONG_ITEM = "wrong_item"
    MIND_CHANGE = "mind_change"


class Account(SQLModel, table=True):
    __tablename__ = 'accounts'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    phone: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str
    role: UserRole = Field(default=UserRole.SALES_PERSON)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    sales: list["Sale"] = Relationship(back_populates="cashier")


class Employee(SQLModel, table=True):
    __tablename__ = 'employees'

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    phone: str = Field(unique=True, index=True)
    ghana_card: str = Field(unique=True, index=True)
    address: str | None = None
    hire_date: date = Field(default_factory=date.today)
    salary: float | None = None
    designation: EmployeeDesignation = Field(default=EmployeeDesignation.ADMIN)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Stock(SQLModel, table=True):
    __tablename__ = 'stocks'

    id: int | None = Field(default=None, primary_key=True)
    item_name: str = Field(index=True)
    quantity: int = Field(ge=0)
    cost_price: float = Field(ge=0)
    selling_price: float = Field(ge=0)
    category: StockType = Field(default=StockType.RETAIL)
    expiry_date: date | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    sale_item: "SaleItem" = Relationship(back_populates="stock")
    damaged_item: "Damage" = Relationship(back_populates="stock")
    returned_item: "Return" = Relationship(back_populates="stock")

    @property
    def profit_per_unit(self) -> float:
        return self.selling_price - self.cost_price

    @property
    def total_cost_value(self) -> float:
        return self.quantity * self.cost_price

    @property
    def total_selling_value(self) -> float:
        return self.quantity * self.selling_price

    @property
    def total_profit_potential(self) -> float:
        return self.quantity * self.profit_per_unit


class Sale(SQLModel, table=True):
    __tablename__ = 'sales'

    id: int | None = Field(default=None, primary_key=True)
    sale_date: date = Field(default_factory=date.today, index=True)
    sale_time: datetime = Field(default_factory=datetime.now)
    discount_amount: float = Field(ge=0, default=0)
    amount_paid: float = Field(ge=0)
    change_given: float = Field(ge=0, default=0)
    payment_method: PaymentMethod = Field(default=PaymentMethod.CASH)
    cashier_id: int = Field(foreign_key="accounts.id")
    created_at: datetime = Field(default_factory=datetime.now)

    cashier: Account = Relationship(back_populates='sales')
    sale_items: list["SaleItem"] = Relationship(back_populates="sale")
    returned_items: list["Return"] = Relationship(back_populates="sale")


class SaleItem(SQLModel, table=True):
    __tablename__ = 'sale_items'

    id: int | None = Field(default=None, primary_key=True)
    sale_id: int = Field(foreign_key="sales.id")
    stock_id: int = Field(foreign_key="stocks.id")
    quantity_sold: int = Field(ge=1)

    sale: Sale = Relationship(back_populates="sale_items")
    stock: Stock = Relationship(back_populates="sale_item")


class Damage(SQLModel, table=True):
    __tablename__ = 'damages'

    id: int | None = Field(default=None, primary_key=True)
    stock_id: int = Field(foreign_key="stocks.id")
    quantity_damaged: int = Field(ge=1)
    damage_date: date = Field(default_factory=date.today, index=True)
    created_at: datetime = Field(default_factory=datetime.now)

    stock: Stock = Relationship(back_populates="damage")


class Expenditure(SQLModel, table=True):
    __tablename__ = 'expenditures'

    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(sa_column=Column(TEXT, nullable=False, index=True))
    amount: float = Field(ge=0)
    category: ExpenditureCategory = Field(default=ExpenditureCategory.UTILITIES)
    expense_date: date = Field(default_factory=date.today, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Return(SQLModel, table=True):
    __tablename__ = 'returns'

    id: int | None = Field(default=None, primary_key=True)
    sale_id: int = Field(foreign_key="sales.id")
    stock_id: int = Field(foreign_key="stocks.id")
    quantity: int = Field(ge=1)
    reason: ReturnReason = Field(default=ReturnReason.DEFECTIVE)
    return_date: date = Field(default_factory=date.today, index=True)
    created_at: datetime = Field(default_factory=datetime.now)

    stock: Stock = Relationship(back_populates="returned_item")
    sale: Sale = Relationship(back_populates="returned_items")
