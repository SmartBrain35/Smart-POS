from datetime import datetime, date
from typing import Any
from sqlmodel import select, and_, or_, func
from sqlalchemy.exc import IntegrityError
from backend.storage.database import get_session
from backend.auth import hash_password, verify_password
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

                account_return = account.model_dump(exclude={'password'})
                account_return['role'] = account.role.value

                return {
                    "success": True,
                    "account": account_return
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

                account_return = account.model_dump(exclude={'password'})
                account_return['role'] = account.role.value

                return {
                    "success": True,
                    "account": account_return
                }
        except Exception as e:
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
                        {
                            "id": acc.id,
                            "name": acc.name,
                            "phone": acc.phone,
                            "email": acc.email,
                            "role": acc.role.value,
                            "created_at": acc.created_at.isoformat(),
                            "updated_at": acc.updated_at.isoformat()
                        } for acc in accounts
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_account(
        account_id: int,
        name: str = None,
        phone: str = None,
        email: str = None,
        password: str = None
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

                account_return = account.model_dump(exclude={'password'})
                account_return['role'] = account.role.value

                return {
                    "success": True,
                    "account": account_return
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
