from datetime import datetime, date
from pydantic import BaseModel
from backend.storage.models import (
    UserRole, EmployeeDesignation, StockType, PaymentMethod,
    ExpenditureCategory
)


class AccountRead(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


class EmployeeRead(BaseModel):
    id: int
    name: str
    phone: str
    ghana_card: str
    address: str | None = None
    hire_date: date
    salary: float | None = None
    designation: EmployeeDesignation
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


class StockRead(BaseModel):
    id: int
    item_name: str
    quantity: int
    cost_price: float
    selling_price: float
    category: StockType
    expiry_date: date | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


class SaleRead(BaseModel):
    id: int
    sale_date: date
    sale_time: datetime
    discount_amount: float
    amount_paid: float
    change_given: float
    payment_method: PaymentMethod
    cashier_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


class ExpenditureRead(BaseModel):
    id: int
    description: str
    amount: float
    category: ExpenditureCategory
    expense_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True
