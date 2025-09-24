from datetime import datetime, date, timedelta
from typing import Any
from sqlmodel import select, and_, or_, func
from backend.storage.database import get_session
from backend.auth import hash_password, verify_password
from backend.schemas import AccountRead, EmployeeRead, StockRead, ExpenditureRead
from enum import Enum
from sqlalchemy import Column, TEXT
from typing import Dict, Any

from backend.storage.models import (
    Account,
    Employee,
    Stock,
    Sale,
    SaleItem,
    Damage,
    Expenditure,
    Return,
    UserRole,
    EmployeeDesignation,
    PaymentMethod,
    StockType,
    DamageStatus,
    ExpenditureCategory,
    ReturnReason,
)
from backend.storage.models import Account, UserRole, Sale


from backend.schemas import (
    AccountRead,
    EmployeeRead,
    StockRead,
    ExpenditureRead,
    SaleRead,
    SaleItemRead,
    DamageRead,
    ReturnRead,
    ReportRead,
    DashboardKPIRead,
)

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


class AccountAPI:
    """CRUD operations for Account management with authentication logic"""

    @staticmethod
    def create_account(
        name: str, phone: str, email: str, password: str, role: str = "admin"
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
                    return {
                        "success": False,
                        "error": f"Account with this {field} already exists",
                    }

                # Create new account
                account = Account(
                    name=name,
                    phone=phone,
                    email=email,
                    password=hash_password(password),
                    role=user_role,
                )

                session.add(account)
                session.commit()
                session.refresh(account)

                return {
                    "success": True,
                    "account": account.model_dump(exclude={"password"}),
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
                        or_(
                            Account.email == login_credential,
                            Account.phone == login_credential,
                        )
                    )
                ).first()

                if not account:
                    return {"success": False, "error": "Invalid credentials"}

                if not verify_password(password, account.password):
                    return {"success": False, "error": "Invalid password"}

                return {
                    "success": True,
                    "account": account.model_dump(exclude={"password"}),
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
                        acc.model_dump(exclude={"password"}) for acc in accounts
                    ],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_account_by_id(account_id: int) -> dict[str, Any]:
        """Fetch single account by id"""
        try:
            with get_session() as session:
                account = session.get(Account, account_id)
                if not account:
                    return {"success": False, "error": "Account not found"}
                return {
                    "success": True,
                    "account": account.model_dump(exclude={"password"}),
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_account(
        account_id: int,
        name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        password: str | None = None,
        role: str | None = None,
    ) -> dict[str, Any]:
        """Update account details"""
        try:
            with get_session() as session:
                account = session.get(Account, account_id)
                if not account:
                    return {"success": False, "error": "Account not found"}

                # Check for conflicts with other accounts
                if phone or email:
                    existing = session.exec(
                        select(Account).where(
                            and_(
                                Account.id != account_id,
                                or_(
                                    Account.phone == phone if phone else False,
                                    Account.email == email if email else False,
                                ),
                            )
                        )
                    ).first()
                    if existing:
                        field = "phone" if existing.phone == phone else "email"
                        return {
                            "success": False,
                            "error": f"Another account with this {field} already exists",
                        }

                # Apply updates
                if name:
                    account.name = name
                if phone:
                    account.phone = phone
                if email:
                    account.email = email
                if password:
                    account.password = hash_password(password)
                if role:
                    try:
                        account.role = UserRole(role)
                    except ValueError:
                        return {"success": False, "error": f"Invalid role: {role}"}

                account.updated_at = datetime.now()
                session.add(account)
                session.commit()
                session.refresh(account)

                return {
                    "success": True,
                    "account": account.model_dump(exclude={"password"}),
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_account(account_id: int) -> dict[str, Any]:
        """Delete an account if it has no linked sales"""
        try:
            with get_session() as session:
                account = session.get(Account, account_id)
                if not account:
                    return {"success": False, "error": "Account not found"}

                sales_count = session.exec(
                    select(func.count(Sale.id)).where(Sale.cashier_id == account_id)
                ).first()
                if sales_count and sales_count > 0:
                    return {
                        "success": False,
                        "error": "Cannot delete account with existing sales records",
                    }

                session.delete(account)
                session.commit()
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
        designation: str = "admin",
    ) -> dict[str, Any]:
        """Add a new employee"""
        try:
            with get_session() as session:
                try:
                    emp_designation = EmployeeDesignation(designation)
                except ValueError:
                    return {
                        "success": False,
                        "error": f"Invalid designation: {designation}",
                    }

                # Check for existing phone/ghana_card
                existing = session.exec(
                    select(Employee).where(
                        or_(Employee.phone == phone, Employee.ghana_card == ghana_card)
                    )
                ).first()

                if existing:
                    field = "phone" if existing.phone == phone else "ghana_card"
                    return {
                        "success": False,
                        "error": f"Employee with this {field} already exists",
                    }

                employee = Employee(
                    name=name,
                    phone=phone,
                    ghana_card=ghana_card,
                    address=address,
                    salary=salary,
                    designation=emp_designation,
                )

                session.add(employee)
                session.flush()
                session.refresh(employee)

                return {
                    "success": True,
                    "employee": EmployeeRead.model_validate(employee).model_dump(),
                }
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
                    "employees": [emp.model_dump() for emp in employees],
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
                            Employee.ghana_card.contains(search_term),
                        )
                    )
                ).all()

                return {
                    "success": True,
                    "employees": [emp.model_dump() for emp in employees],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_employee_field(
        employee_id: int, field: str, value: Any
    ) -> dict[str, Any]:
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
                        return {
                            "success": False,
                            "error": "Phone number already exists",
                        }
                    employee.phone = str(value)
                elif field == "ghana_card":
                    # Check for duplicate ghana_card
                    existing = session.exec(
                        select(Employee).where(
                            and_(
                                Employee.id != employee_id, Employee.ghana_card == value
                            )
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
                        return {
                            "success": False,
                            "error": f"Invalid designation: {value}",
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Field '{field}' cannot be updated",
                    }

                employee.updated_at = datetime.now()
                return {
                    "success": True,
                    "employee": Employee.model_validate(employee).model_dump(),
                }
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


# ==========================
# STOCK API
# ==========================
class StockAPI:

    @staticmethod
    def get_all() -> dict:
        try:
            with get_session() as session:
                items = session.exec(select(Stock).where(Stock.is_active == True)).all()
                return {
                    "success": True,
                    "items": [StockRead.model_validate(i).model_dump() for i in items],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_stock(
        name: str,
        quantity: int,
        cost_price: float,
        selling_price: float,
        category: str,
        expiry_date: str | None = None,
    ) -> dict:
        try:
            expiry = (
                datetime.strptime(expiry_date, "%Y-%m-%d").date()
                if expiry_date
                else None
            )
            with get_session() as session:
                stock = Stock(
                    item_name=name,
                    quantity=quantity,
                    cost_price=cost_price,
                    selling_price=selling_price,
                    category=StockType(category.lower()),
                    expiry_date=expiry,
                    is_active=True,
                )
                session.add(stock)
                session.commit()
                session.refresh(stock)
                return {
                    "success": True,
                    "stock": StockRead.model_validate(stock).model_dump(),
                }
        except ValueError:
            return {"success": False, "error": "Invalid expiry date format or category"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_stock(
        stock_id: int,
        name: str,
        quantity: int,
        cost_price: float,
        selling_price: float,
        category: str,
        expiry_date: str | None = None,
    ) -> dict:
        try:
            expiry = (
                datetime.strptime(expiry_date, "%Y-%m-%d").date()
                if expiry_date
                else None
            )
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock not found"}
                if not stock.is_active:
                    return {"success": False, "error": "Cannot update archived stock"}
                stock.item_name = name
                stock.quantity = quantity
                stock.cost_price = cost_price
                stock.selling_price = selling_price
                stock.category = StockType(category.lower())
                stock.expiry_date = expiry
                stock.updated_at = datetime.now()
                session.add(stock)
                session.commit()
                return {"success": True}
        except ValueError:
            return {"success": False, "error": "Invalid expiry date format or category"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_stock(stock_id: int) -> dict:
        """
        Delete stock if unused, otherwise archive it to preserve history.
        - If stock has sales, damages, or returns → archive.
        - If stock has no history → permanently delete.
        """
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock not found"}

                # Check usage
                has_sales = bool(stock.sale_items)
                has_damages = bool(stock.damaged_items)
                has_returns = bool(stock.returned_items)

                if has_sales or has_damages or has_returns:
                    # Archive instead of delete
                    stock.is_active = False  # new field in Stock model
                    stock.updated_at = datetime.utcnow()
                    session.add(stock)
                    session.commit()
                    return {
                        "success": True,
                        "message": f"Stock {stock_id} archived (linked to history)",
                        "archived": True,
                    }
                else:
                    # No history → safe to permanently delete
                    session.delete(stock)
                    session.commit()
                    return {
                        "success": True,
                        "message": f"Stock {stock_id} permanently deleted",
                        "archived": False,
                    }

        except Exception as e:
            return {"success": False, "error": str(e)}


# ==========================
# SALE API
# ==========================
class SaleAPI:
    """Sales management API aligned with Sales UI."""

    @staticmethod
    def create_sale(
        cashier_id: int,
        sale_items: list[dict],
        amount_paid: float,
        discount_amount: float = 0,
        payment_method: str = "cash",
        sale_date: str | None = None,
    ) -> dict[str, Any]:
        try:
            with get_session() as session:
                parsed_date = date.today()
                if sale_date:
                    parsed_date = datetime.strptime(sale_date, "%Y-%m-%d").date()

                gross_total, items_sold, profit_total = 0, 0, 0

                sale = Sale(
                    sale_date=parsed_date,
                    discount_amount=discount_amount,
                    amount_paid=amount_paid,
                    payment_method=PaymentMethod(payment_method),
                    cashier_id=cashier_id,
                )
                session.add(sale)
                session.flush()

                sale_items_models = []
                for item in sale_items:
                    stock = session.get(Stock, item["stock_id"])
                    qty = item["quantity_sold"]

                    if not stock:
                        return {
                            "success": False,
                            "error": f"Stock {item['stock_id']} not found",
                        }
                    if stock.quantity < qty:
                        return {
                            "success": False,
                            "error": f"Insufficient stock for {stock.item_name}",
                        }

                    gross_total += stock.selling_price * qty
                    items_sold += qty
                    profit_total += (stock.selling_price - stock.cost_price) * qty

                    sale_item = SaleItem(
                        sale_id=sale.id, stock_id=stock.id, quantity_sold=qty
                    )
                    session.add(sale_item)
                    sale_items_models.append(sale_item)

                    stock.quantity -= qty
                    stock.updated_at = datetime.now()

                total = gross_total - discount_amount
                if amount_paid < total:
                    return {"success": False, "error": "Insufficient payment"}
                sale.change_given = amount_paid - total

                session.commit()

                lcd_summary = {
                    "gross": gross_total,
                    "discount": discount_amount,
                    "total": total,
                    "items_sold": items_sold,
                    "daily_profit": profit_total,
                }

                return {
                    "success": True,
                    "sale": SaleRead.model_validate(sale).model_dump(),
                    "items": [
                        SaleItemRead.model_validate(si).model_dump()
                        for si in sale_items_models
                    ],
                    "lcd": lcd_summary,
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_sales() -> dict[str, Any]:
        try:
            with get_session() as session:
                sales = session.exec(select(Sale)).all()
                return {
                    "success": True,
                    "sales": [SaleRead.model_validate(s).model_dump() for s in sales],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_sale_by_id(sale_id: int) -> dict[str, Any]:
        try:
            with get_session() as session:
                sale = session.get(Sale, sale_id)
                if not sale:
                    return {"success": False, "error": "Sale not found"}

                sale_items = session.exec(
                    select(SaleItem).where(SaleItem.sale_id == sale_id)
                ).all()
                return {
                    "success": True,
                    "sale": SaleRead.model_validate(sale).model_dump(),
                    "items": [
                        SaleItemRead.model_validate(si).model_dump()
                        for si in sale_items
                    ],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_sale(sale_id: int, rollback_stock: bool = True) -> dict[str, Any]:
        try:
            with get_session() as session:
                sale = session.get(Sale, sale_id)
                if not sale:
                    return {"success": False, "error": "Sale not found"}

                sale_items = session.exec(
                    select(SaleItem).where(SaleItem.sale_id == sale_id)
                ).all()
                if rollback_stock:
                    for item in sale_items:
                        stock = session.get(Stock, item.stock_id)
                        if stock:
                            stock.quantity += item.quantity_sold
                            stock.updated_at = datetime.now()

                for si in sale_items:
                    session.delete(si)

                session.delete(sale)
                session.commit()
                return {
                    "success": True,
                    "message": f"Sale {sale_id} deleted successfully",
                }
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==========================
# DAMAGE API
# ==========================

class DamageAPI:
    """Damage management API with stock sync for production use."""

    @staticmethod
    def record_damage(
        stock_id: int, quantity_damaged: int, status: str = "broken"
    ) -> Dict[str, Any]:
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock not found"}
                if stock.quantity < quantity_damaged:
                    return {"success": False, "error": "Insufficient stock to damage"}

                damage = Damage(
                    stock_id=stock_id,
                    quantity_damaged=quantity_damaged,
                    damage_status=DamageStatus(status),
                )
                session.add(damage)

                # Adjust stock
                stock.quantity -= quantity_damaged
                stock.updated_at = datetime.now()

                session.commit()

                return {
                    "success": True,
                    "message": "Damage recorded successfully",
                    "damage": {
                        "id": damage.id,
                        "stock_id": stock_id,
                        "item_name": stock.item_name,
                        "quantity_damaged": quantity_damaged,
                        "price": stock.selling_price,
                        "damage_status": status,
                        "created_at": damage.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    },
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_damage(
        damage_id: int, new_quantity: int, new_status: str
    ) -> Dict[str, Any]:
        try:
            with get_session() as session:
                damage = session.get(Damage, damage_id)
                if not damage:
                    return {"success": False, "error": "Damage record not found"}

                stock = session.get(Stock, damage.stock_id)
                if not stock:
                    return {"success": False, "error": "Stock not found"}

                # Calculate quantity difference to adjust stock properly
                qty_diff = new_quantity - damage.quantity_damaged

                if qty_diff > 0 and stock.quantity < qty_diff:
                    return {
                        "success": False,
                        "error": "Insufficient stock to increase damage quantity",
                    }

                # Update damage record
                damage.quantity_damaged = new_quantity
                damage.damage_status = DamageStatus(new_status)

                # Adjust stock
                stock.quantity -= qty_diff
                stock.updated_at = datetime.now()

                session.commit()

                return {"success": True, "message": "Damage updated successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_damage(damage_id: int) -> Dict[str, Any]:
        try:
            with get_session() as session:
                damage = session.get(Damage, damage_id)
                if not damage:
                    return {"success": False, "error": "Damage record not found"}

                stock = session.get(Stock, damage.stock_id)
                if stock:
                    # Restore stock quantity when damage deleted
                    stock.quantity += damage.quantity_damaged
                    stock.updated_at = datetime.now()

                session.delete(damage)
                session.commit()

                return {"success": True, "message": "Damage deleted and stock restored"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_damages() -> Dict[str, Any]:
        try:
            with get_session() as session:
                damages = session.exec(select(Damage)).all()
                result = []
                for d in damages:
                    stock = session.get(Stock, d.stock_id)
                    result.append(
                        {
                            "id": d.id,
                            "stock_id": d.stock_id,
                            "item_name": stock.item_name if stock else "Unknown",
                            "quantity_damaged": d.quantity_damaged,
                            "price": stock.selling_price if stock else 0,
                            "damage_status": d.damage_status.value,
                            "created_at": d.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
                return {"success": True, "damages": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==========================
# Expenditure API
# ==========================
class ExpenditureAPI:
    """Expenditure management API aligned with Expenditure UI."""

    @staticmethod
    def create_expenditure(
        description: str, amount: float, category: str, expense_date: str | None = None
    ) -> dict[str, Any]:
        try:
            with get_session() as session:
                parsed_date = date.today()
                if expense_date:
                    parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()

                expenditure = Expenditure(
                    description=description,
                    amount=amount,
                    category=ExpenditureCategory(category),
                    expense_date=parsed_date,
                )
                session.add(expenditure)
                session.commit()
                return {
                    "success": True,
                    "expenditure": ExpenditureRead.model_validate(
                        expenditure
                    ).model_dump(),
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_expenditures() -> dict[str, Any]:
        try:
            with get_session() as session:
                expenditures = session.exec(select(Expenditure)).all()
                return {
                    "success": True,
                    "expenditures": [
                        ExpenditureRead.model_validate(e).model_dump()
                        for e in expenditures
                    ],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==========================
# RETURN API
# ==========================
class ReturnAPI:
    """Return management API aligned with Return UI."""

    @staticmethod
    def process_return(
        sale_id: int, stock_id: int, quantity: int, reason: str = "defective"
    ) -> dict[str, Any]:
        try:
            with get_session() as session:
                sale = session.get(Sale, sale_id)
                if not sale:
                    return {"success": False, "error": "Sale not found"}

                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock not found"}

                ret = Return(
                    sale_id=sale_id,
                    stock_id=stock_id,
                    quantity=quantity,
                    reason=ReturnReason(reason),
                )
                session.add(ret)

                stock.quantity += quantity
                stock.updated_at = datetime.now()

                session.commit()
                return {
                    "success": True,
                    "return": ReturnRead.model_validate(ret).model_dump(),
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_returns() -> dict[str, Any]:
        try:
            with get_session() as session:
                returns = session.exec(select(Return)).all()
                return {
                    "success": True,
                    "returns": [
                        ReturnRead.model_validate(r).model_dump() for r in returns
                    ],
                }
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==========================
# REPORT API
# ==========================
class ReportAPI:
    """Report generation API aligned with Report UI."""

    @staticmethod
    def generate_report(
        start_date: str, end_date: str, category: str = "all", as_pdf: bool = False
    ):
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            with get_session() as session:
                data: list[dict] = []

                if category in ["all", "sales"]:
                    sales = session.exec(
                        select(Sale).where(
                            and_(Sale.sale_date >= start, Sale.sale_date <= end)
                        )
                    ).all()
                    total = sum(s.amount_paid - s.change_given for s in sales)
                    data.append(
                        ReportRead(
                            category="sales", total=total, count=len(sales)
                        ).model_dump()
                    )

                if category in ["all", "expenditures"]:
                    exps = session.exec(
                        select(Expenditure).where(
                            and_(
                                Expenditure.expense_date >= start,
                                Expenditure.expense_date <= end,
                            )
                        )
                    ).all()
                    total = sum(e.amount for e in exps)
                    data.append(
                        ReportRead(
                            category="expenditures", total=total, count=len(exps)
                        ).model_dump()
                    )

                if not as_pdf:
                    return {"success": True, "report": data}

                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=A4)
                c.setFont("Helvetica-Bold", 14)
                c.drawString(200, 800, "Business Report")
                y = 760
                for entry in data:
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(50, y, entry["category"].upper())
                    y -= 20
                    c.setFont("Helvetica", 10)
                    for k, v in entry.items():
                        if k != "category":
                            c.drawString(70, y, f"{k}: {v}")
                            y -= 15
                    y -= 10
                c.save()
                return buffer.getvalue()
        except Exception as e:
            return {"success": False, "error": str(e)}


# ==========================
# DASHBOARD API
# ==========================
class DashboardAPI:
    """Dashboard API aligned with Dashboard UI."""

    @staticmethod
    def get_kpis() -> dict[str, Any]:
        try:
            with get_session() as session:
                sales = session.exec(select(Sale)).all()
                revenue = sum(s.amount_paid - s.change_given for s in sales)
                transactions = len(sales)

                sale_items = session.exec(select(SaleItem)).all()
                gross_profit = sum(
                    (
                        session.get(Stock, item.stock_id).selling_price
                        - session.get(Stock, item.stock_id).cost_price
                    )
                    * item.quantity_sold
                    for item in sale_items
                )

                expenditures = session.exec(select(Expenditure)).all()
                net_profit = gross_profit - sum(e.amount for e in expenditures)

                low_stock = session.exec(select(Stock).where(Stock.quantity < 10)).all()

                return {
                    "success": True,
                    "kpis": DashboardKPIRead.model_validate(
                        {
                            "total_revenue": revenue,
                            "total_profit": net_profit,
                            "total_transactions": transactions,
                            "low_stock_count": len(low_stock),
                            "low_stock_items": [s.item_name for s in low_stock],
                        }
                    ).model_dump(),
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
