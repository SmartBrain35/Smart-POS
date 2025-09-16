from datetime import datetime, date
from pydantic import BaseModel
from backend.storage.models import UserRole, EmployeeDesignation


class AccountRead(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
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
        use_enum_values = True
