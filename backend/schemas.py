from datetime import datetime, date
from pydantic import BaseModel
from backend.storage.models import (
    UserRole,
    EmployeeDesignation,
    StockType,
    ExpenditureCategory,
    PaymentMethod,
    DamageStatus,
    ReturnReason,
)


# ========================
# ACCOUNT
# ========================
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


# ========================
# EMPLOYEE
# ========================
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


# ========================
# STOCK
# ========================
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


# ========================
# EXPENDITURE
# ========================
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


# ========================
# SALE & SALE ITEM
# ========================
class SaleItemRead(BaseModel):
    id: int
    sale_id: int
    stock_id: int
    quantity_sold: int

    class Config:
        from_attributes = True


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


# ========================
# DAMAGE
# ========================
class DamageRead(BaseModel):
    id: int
    stock_id: int
    quantity_damaged: int
    damage_status: DamageStatus
    damage_date: date
    created_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


# ========================
# RETURN
# ========================
class ReturnRead(BaseModel):
    id: int
    sale_id: int
    stock_id: int
    quantity: int
    reason: ReturnReason
    return_date: date
    created_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True


# ========================
# DASHBOARD KPIs
# ========================
class DashboardKPIRead(BaseModel):
    total_revenue: float
    total_profit: float
    total_transactions: int
    low_stock_count: int
    low_stock_items: list[str]

    class Config:
        from_attributes = True


# ========================
# REPORT
# ========================
class ReportRead(BaseModel):
    category: str
    total: float | None = None
    count: int | None = None

    class Config:
        from_attributes = True
