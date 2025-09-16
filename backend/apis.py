from datetime import datetime, date
from typing import Any
from sqlmodel import select, and_, or_, func
from backend.storage.database import get_session
from backend.auth import hash_password, verify_password
from backend.schemas import (
    AccountRead, EmployeeRead
)

from backend.storage.models import (
    Account, Employee, Stock, Sale, SaleItem, Damage,
    Expenditure, Return, UserRole, EmployeeDesignation,
    PaymentMethod, StockType, DamageStatus, ExpenditureCategory, ReturnReason
)



class AccountAPI:
    """CRUD operations for Account management with authentication logic"""

    @staticmethod
    def create_account(
        name: str,
        phone: str,
        email: str,
        password: str,
        role: str = "admin"
    ) -> dict[str, Any]:
        """Register a new account with validation"""
        try:
            with get_session() as session:
                # Validate role
                try:
                    user_role = UserRole(role)
                except ValueError:
                    return {"success": False, "error": f"Invalid role: {role}"}

                # Check for existing phone/email
                existing = session.exec(
                    select(Account).where(
                        or_(Account.phone == phone, Account.email == email)
                    )
                ).first()

                if existing:
                    field = "phone" if existing.phone == phone else "email"
                    return {"success": False, "error": f"Account with this {field} already exists"}

                # Create new account
                account = Account(
                    name=name,
                    phone=phone,
                    email=email,
                    password=hash_password(password),
                    role=user_role
                )

                session.add(account)
                session.commit()
                session.refresh(account)

                return {
                    "success": True,
                    "account": AccountRead.model_validate(account).model_dump()
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def authenticate(login_credential: str, password: str) -> dict[str, Any]:
        """Login with email/phone and password"""
        try:
            with get_session() as session:
                account = session.exec(
                    select(Account).where(
                        or_(Account.email == login_credential, Account.phone == login_credential)
                    )
                ).first()

                if not account:
                    return {"success": False, "error": "Invalid credentials"}

                if not verify_password(password, account.password):
                    return {'success': False, 'error': 'Invalid password'}

                return {
                    "success": True,
                    "account": AccountRead.model_validate(account).model_dump()
                }
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_accounts() -> dict[str, Any]:
        """Get all accounts for table display"""
        try:
            with get_session() as session:
                accounts = session.exec(select(Account)).all()
                return {
                    "success": True,
                    "accounts": [
                        AccountRead.model_validate(acc).model_dump()  for acc in accounts
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_account(
        account_id: int,
        name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        password: str | None = None
    ) -> dict[str, Any]:
        """Update account details"""
        try:
            with get_session() as session:
                account = session.get(Account, account_id)
                if not account:
                    return {"success": False, "error": "Account not found"}

                # # Validate role
                # try:
                #     user_role = UserRole(role)
                # except ValueError:
                #     return {"success": False, "error": f"Invalid role: {role}"}

                # Check for conflicts with other accounts
                existing = session.exec(
                    select(Account).where(
                        and_(
                            Account.id != account_id,
                            or_(Account.phone == phone, Account.email == email)
                        )
                    )
                ).first()

                if existing:
                    field = "phone" if existing.phone == phone else "email"
                    return {"success": False, "error": f"Another account with this {field} already exists"}

                # Update account
                account.name = name
                account.phone = phone
                account.email = email
                account.password = password
                account.updated_at = datetime.now()

                return {
                    "success": True,
                    "account": AccountRead.model_validate(account).model_dump()
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_account(account_id: int) -> dict[str, Any]:
        """Delete an account"""
        try:
            with get_session() as session:
                account = session.get(Account, account_id)
                if not account:
                    return {"success": False, "error": "Account not found"}

                # Check if account has sales records
                sales_count = session.exec(select(func.count(Sale.id)).where(Sale.cashier_id == account_id)).first()
                if sales_count and sales_count > 0:
                    return {"success": False, "error": "Cannot delete account with existing sales records"}

                session.delete(account)
                return {"success": True, "message": "Account deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class EmployeeAPI:
    """CRUD operations for Employee management"""

    @staticmethod
    def create_employee(
        name: str,
        phone: str,
        ghana_card: str,
        address: str | None = None,
        salary: float | None = None,
        designation: str = "admin"
    ) -> dict[str, Any]:
        """Add a new employee"""
        try:
            with get_session() as session:
                try:
                    emp_designation = EmployeeDesignation(designation)
                except ValueError:
                    return {"success": False, "error": f"Invalid designation: {designation}"}

                # Check for existing phone/ghana_card
                existing = session.exec(
                    select(Employee).where(
                        or_(Employee.phone == phone, Employee.ghana_card == ghana_card)
                    )
                ).first()

                if existing:
                    field = "phone" if existing.phone == phone else "ghana_card"
                    return {"success": False, "error": f"Employee with this {field} already exists"}

                employee = Employee(
                    name=name,
                    phone=phone,
                    ghana_card=ghana_card,
                    address=address,
                    salary=salary,
                    designation=emp_designation
                )

                session.add(employee)
                session.commit()
                session.refresh(employee)

                return {"success": True, "employee": EmployeeRead.model_validate(employee).model_dump()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_employees() -> dict[str, Any]:
        """Get all employees"""
        try:
            with get_session() as session:
                employees = session.exec(select(Employee)).all()
                return {
                    "success": True,
                    "employees": [
                        Employee.model_validate(emp).model_dump()
                        for emp in employees
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def filter_employees(search_term: str) -> dict[str, Any]:
        """Filter employees by phone or Ghana card"""
        try:
            with get_session() as session:
                employees = session.exec(
                    select(Employee).where(
                        or_(
                            Employee.phone.contains(search_term),
                            Employee.ghana_card.contains(search_term)
                        )
                    )
                ).all()

                return {
                    "success": True,
                    "employees": [
                        Employee.model_validate(emp).model_dump()
                        for emp in employees
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_employee_field(employee_id: int, field: str, value: Any) -> dict[str, Any]:
        """Update a specific field of an employee (for double-click editing)"""
        try:
            with get_session() as session:
                employee = session.get(Employee, employee_id)
                if not employee:
                    return {"success": False, "error": "Employee not found"}

                # Validate field and set value
                if field == "name":
                    employee.name = str(value)
                elif field == "phone":
                    # Check for duplicate phone
                    existing = session.exec(
                        select(Employee).where(
                            and_(Employee.id != employee_id, Employee.phone == value)
                        )
                    ).first()
                    if existing:
                        return {"success": False, "error": "Phone number already exists"}
                    employee.phone = str(value)
                elif field == "ghana_card":
                    # Check for duplicate ghana_card
                    existing = session.exec(
                        select(Employee).where(
                            and_(Employee.id != employee_id, Employee.ghana_card == value)
                        )
                    ).first()
                    if existing:
                        return {"success": False, "error": "Ghana card already exists"}
                    employee.ghana_card = str(value)
                elif field == "address":
                    employee.address = str(value) if value else None
                elif field == "salary":
                    employee.salary = float(value) if value else None
                elif field == "designation":
                    try:
                        employee.designation = EmployeeDesignation(value)
                    except ValueError:
                        return {"success": False, "error": f"Invalid designation: {value}"}
                else:
                    return {"success": False, "error": f"Field '{field}' cannot be updated"}

                employee.updated_at = datetime.now()
                return {"success": True, "employee": Employee.model_validate(employee).model_dump()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_employee(employee_id: int) -> dict[str, Any]:
        """Delete an employee"""
        try:
            with get_session() as session:
                employee = session.get(Employee, employee_id)
                if not employee:
                    return {"success": False, "error": "Employee not found"}

                session.delete(employee)
                return {"success": True, "message": "Employee deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}
