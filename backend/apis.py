from datetime import datetime, date, timedelta
from typing import Any
from sqlmodel import select, and_, or_, func
from backend.storage.database import get_session
from backend.auth import hash_password, verify_password
from backend.schemas import (
    AccountRead, EmployeeRead, StockRead, ExpenditureRead
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
                session.flush()
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
        name: str,
        phone: str,
        email: str,
        password: str,
        role: str
    ) -> dict[str, Any]:
        """Update account details"""
        try:
            with get_session() as session:
                account = session.get(Account, account_id)
                if not account:
                    return {"success": False, "error": "Account not found"}

                # Validate role
                try:
                    user_role = UserRole(role)
                except ValueError:
                    return {"success": False, "error": f"Invalid role: {role}"}

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
                account.role = user_role

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
                session.flush()
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


class StockAPI:
    """CRUD operations for Stock management with business logic"""

    @staticmethod
    def add_stock(
        item_name: str,
        quantity: int,
        cost_price: float,
        selling_price: float,
        category: str = "retail",
        expiry_date: str | None = None
    ) -> dict[str, Any]:
        """Add new stock item"""
        try:
            with get_session() as session:
                try:
                    stock_type = StockType(category)
                except ValueError:
                    return {"success": False, "error": f"Invalid category: {category}"}

                # Parse expiry date
                parsed_expiry = None
                if expiry_date:
                    try:
                        parsed_expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
                    except ValueError:
                        return {"success": False, "error": "Invalid expiry date format (YYYY-MM-DD)"}

                # Check if item already exists
                existing = session.exec(
                    select(Stock).where(Stock.item_name == item_name)
                ).first()

                if existing:
                    # Update existing stock
                    existing.quantity += quantity
                    existing.cost_price = cost_price
                    existing.selling_price = selling_price
                    existing.updated_at = datetime.now()
                    if parsed_expiry:
                        existing.expiry_date = parsed_expiry

                    session.commit()
                    return {"success": True, "stock_item": StockRead.model_validate(existing).model_dump()}
                else:
                    # Create new stock item
                    stock = Stock(
                        item_name=item_name,
                        quantity=quantity,
                        cost_price=cost_price,
                        selling_price=selling_price,
                        category=stock_type,
                        expiry_date=parsed_expiry
                    )

                    session.add(stock)
                    session.flush()
                    session.refresh(stock)

                    return {"success": True, "stock_item": StockRead.model_validate(stock).model_dump()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_stock() -> dict[str, Any]:
        """Get all stock items with calculated values"""
        try:
            with get_session() as session:
                stocks = session.exec(select(Stock)).all()
                wholesale_stocks = [
                    stock
                    for stock in stocks
                    if stock.category == StockType.WHOLESALE
                ]

                retail_stocks = [
                    stock
                    for stock in stocks
                    if stock.category == StockType.RETAIL
                ]

                return {
                    "success": True,
                    "stocks": [
                        StockRead.model_validate(stock).model_dump()
                        for stock in stocks
                    ],
                    "summary": {
                        "wholesale_items": len(wholesale_stocks),
                        "wholesale_cost": sum(stock.total_cost_value for stock in wholesale_stocks),
                        "wholesale_value": sum(stock.total_selling_value for stock in wholesale_stocks),
                        "wholesale_profit": sum(stock.total_profit_potential for stock in wholesale_stocks),
                        "retail_items": len(retail_stocks),
                        "retail_cost": sum(stock.total_cost_value for stock in retail_stocks),
                        "retail_value": sum(stock.total_selling_value for stock in retail_stocks),
                        "retail_profit": sum(stock.total_profit_potential for stock in retail_stocks)
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def filter_stock(search_term: str) -> dict[str, Any]:
        """Filter stock by item name"""
        try:
            with get_session() as session:
                stocks = session.exec(
                    select(Stock).where(Stock.item_name.contains(search_term))
                ).all()

                return {
                    "success": True,
                    "stocks": [
                        StockRead.model_validate(stock).model_dump()
                        for stock in stocks
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_stock(
        stock_id: int,
        item_name: str,
        quantity: int,
        cost_price: float,
        selling_price: float,
        category: str,
        expiry_date: str
    ) -> dict[str, Any]:
        """Update stock item"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                try:
                    stock_type = StockType(category)
                except ValueError:
                    return {"success": False, "error": f"Invalid category: {category}"}

                # Parse expiry date
                parsed_expiry = None
                if expiry_date:
                    try:
                        parsed_expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
                    except ValueError:
                        return {"success": False, "error": "Invalid expiry date format (YYYY-MM-DD)"}

                stock.item_name = item_name
                stock.quantity = quantity
                stock.cost_price = cost_price
                stock.selling_price = selling_price
                stock.category = stock_type
                stock.expiry_date = parsed_expiry
                stock.updated_at = datetime.now()

                session.flush()
                session.refresh(stock)
                return {"success": True, "stock": StockRead.model_validate(stock).model_dump()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_stock(stock_id: int) -> dict[str, Any]:
        """Delete stock item"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                # Check if stock has sales records
                sales_count = session.exec(select(func.count(SaleItem.id)).where(SaleItem.stock_id == stock_id)).first()
                if sales_count and sales_count > 0:
                    return {"success": False, "error": "Cannot delete stock with existing sales records"}

                session.delete(stock)
                return {"success": True, "message": "Stock deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def increase_stock_quantity(stock_id: int, quantity: int) -> dict[str, Any]:
        """Increase stock quantity (for returns)"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                stock.quantity += quantity
                stock.updated_at = datetime.now()

                return {"success": True, "new_quantity": stock.quantity}
        except Exception as e:
            return {"success": False, "error": str(e)}


class SaleAPI:
    """CRUD operations for Sales management with business logic"""

    @staticmethod
    def create_sale(
        cashier_id: int,
        sale_items: list[dict],
        amount_paid: float,
        discount_amount: float = 0,
        payment_method: str = "cash",
        sale_date: str | None = None
    ) -> dict[str, Any]:
        """Create a new sale with multiple items"""
        try:
            with get_session() as session:
                try:
                    pay_method = PaymentMethod(payment_method)
                except ValueError:
                    return {"success": False, "error": f"Invalid payment method: {payment_method}"}

                parsed_date = date.today()
                if sale_date:
                    try:
                        parsed_date = datetime.strptime(sale_date, "%Y-%m-%d").date()
                    except ValueError:
                        return {"success": False, "error": "Invalid sale date format (YYYY-MM-DD)"}

                # Validate cashier exists
                cashier = session.get(Account, cashier_id)
                if not cashier:
                    return {"success": False, "error": "Cashier not found"}

                # Calculate totals and validate stock
                gross_total = 0
                validated_items = []

                for item in sale_items:
                    stock_id = item.get("stock_id")
                    quantity_sold = item.get("quantity_sold", 0)

                    stock = session.get(Stock, stock_id)
                    if not stock:
                        return {"success": False, "error": f"Stock item {stock_id} not found"}

                    if stock.quantity < quantity_sold:
                        return {"success": False, "error": f"Insufficient stock for {stock.item_name}. Available: {stock.quantity}"}

                    item_total = stock.selling_price * quantity_sold
                    gross_total += item_total

                    validated_items.append({
                        "stock": stock,
                        "quantity_sold": quantity_sold,
                        "item_total": item_total
                    })

                total = gross_total - discount_amount
                if amount_paid < total:
                    return {"success": False, "error": f"Insufficient payment. Required: {total}"}

                # Create sale
                sale = Sale(
                    sale_date=parsed_date,
                    discount_amount=discount_amount,
                    amount_paid=amount_paid,
                    change_given=amount_paid - total,
                    payment_method=pay_method,
                    cashier_id=cashier_id
                )

                session.add(sale)
                session.flush()

                items_sold = 0

                # Create sale items and reduce stock
                for item_data in validated_items:
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        stock_id=item_data["stock"].id,
                        quantity_sold=item_data["quantity_sold"]
                    )
                    session.add(sale_item)
                    items_sold += item_data['quantity_sold']

                    # Reduce stock quantity
                    item_data["stock"].quantity -= item_data["quantity_sold"]
                    item_data["stock"].updated_at = datetime.now()

                session.flush()
                session.refresh(sale)

                return {
                    "success": True,
                    "sale_id": sale.id,
                    "gross_total": gross_total,
                    "discount": discount_amount,
                    "total": total,
                    "items_sold": items_sold,
                    "message": "Sale created successfully"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_daily_sales_summary(sale_date: str | None = None) -> dict[str, Any]:
        """Get daily sales summary for LCDs"""
        try:
            with get_session() as session:
                target_date = date.today()
                if sale_date:
                    try:
                        target_date = datetime.strptime(sale_date, "%Y-%m-%d").date()
                    except ValueError:
                        return {"success": False, "error": "Invalid date format (YYYY-MM-DD)"}

                # Get daily sales
                sales = session.exec(select(Sale).where(Sale.sale_date == target_date)).all()

                daily_sales = sum(
                    (sum(
                        item.quantity_sold * session.get(Stock, item.stock_id).selling_price
                        for item in session.exec(select(SaleItem).where(SaleItem.sale_id == sale.id))
                    ) - sale.discount_amount) for sale in sales
                )

                # Calculate total items sold and profit
                total_items_sold = 0
                daily_profit = 0

                for sale in sales:
                    sale_items = session.exec(select(SaleItem).where(SaleItem.sale_id == sale.id)).all()
                    for item in sale_items:
                        stock = session.get(Stock, item.stock_id)
                        total_items_sold += item.quantity_sold
                        daily_profit += (stock.selling_price - stock.cost_price) * item.quantity_sold

                return {
                    "success": True,
                    "daily_sales": daily_sales,
                    "daily_profit": daily_profit,
                    "items_sold": total_items_sold,
                    "total_discount": sum(sale.discount_amount for sale in sales),
                    "transactions_count": len(sales)
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_sale_receipt_data(sale_id: int) -> dict[str, Any]:
        """Get sale data for receipt printing"""
        try:
            with get_session() as session:
                sale = session.get(Sale, sale_id)
                if not sale:
                    return {"success": False, "error": "Sale not found"}

                sale_items = session.exec(select(SaleItem).where(SaleItem.sale_id == sale_id)).all()

                items = []
                gross_total = 0

                for sale_item in sale_items:
                    stock = session.get(Stock, sale_item.stock_id)
                    item_total = stock.selling_price * sale_item.quantity_sold
                    gross_total += item_total

                    items.append({
                        "item_name": stock.item_name,
                        "quantity": sale_item.quantity_sold,
                        "unit_price": stock.selling_price,
                        "total": item_total
                    })

                return {
                    "success": True,
                    "sale_id": sale.id,
                    "sale_date": sale.sale_date,
                    "sale_time": sale.sale_time,
                    "cashier_name": sale.cashier.name,
                    "items": items,
                    "gross_total": gross_total,
                    "discount": sale.discount_amount,
                    "net_total": gross_total - sale.discount_amount,
                    "amount_paid": sale.amount_paid,
                    "change": sale.change_given,
                    "payment_method": sale.payment_method.value
                }
        except Exception as e:
            return {"success": False, "error": str(e)}


class DamageAPI:
    """CRUD operations for Damage management"""

    @staticmethod
    def record_damage(
        stock_id: int,
        quantity_damaged: int,
        status: str = 'broken'
    ) -> dict[str, Any]:
        """Record damaged items and update stock"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                if stock.quantity < quantity_damaged:
                    return {"success": False, "error": f"Cannot damage {quantity_damaged} items. Only {stock.quantity} in stock"}

                try:
                    damage_status = DamageStatus(status)
                except ValueError:
                    return {"success": False, "error": f"Invalid damage satus: {status}"}

                # Create damage record
                damage = Damage(
                    stock_id=stock_id,
                    quantity_damaged=quantity_damaged,
                    damage_status=damage_status
                )

                # Reduce stock quantity
                stock.quantity -= quantity_damaged
                stock.updated_at = datetime.now()

                session.add(damage)
                session.flush()
                session.refresh(damage)

                return {
                    "success": True,
                    "damaged_item": {
                        "id": damage.id,
                        "stock_id": stock.id,
                        "item_name": stock.item_name,
                        "quantity_damaged": quantity_damaged,
                        "unit_price": stock.selling_price,
                        "damage_satus": damage_status.value,
                        "damage_date": damage.damage_date
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_damages(search_term: str | None = None) -> dict[str, Any]:
        """Get damages and optionally filter damages by item name"""
        try:
            with get_session() as session:
                query = select(Damage)

                if search_term:
                    query = select(Damage).join(Stock).where(Stock.item_name.contains(search_term))

                damages = session.exec(query).all()

                total_items = sum(damage.quantity_damaged for damage in damages)
                total_price = sum(
                    damage.quantity_damaged * session.get(Stock, damage.stock_id).selling_price
                    for damage in damages
                )
                total_profit_loss = sum(
                    damage.quantity_damaged * session.get(Stock, damage.stock_id).profit_per_unit
                    for damage in damages
                )

                return {
                    "success": True,
                    "damaged_items": [
                        {
                            "id": damage.id,
                            "stock_id": damage.stock_id,
                            "item_name": session.get(Stock, damage.stock_id).item_name,
                            "quantity_damaged": damage.quantity_damaged,
                            "damage_date": damage.damage_date,
                            "unit_price": session.get(Stock, damage.stock_id).selling_price,
                            "damage_satus": damage.damage_status.value,
                        } for damage in damages
                    ],
                    "summary": {
                        "total_items": total_items,
                        "total_price": total_price,
                        "total_profit_loss": total_profit_loss
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_damage(
        damage_id: int,
        stock_id: int,
        quantity_damaged: int,
        damage_date: str,
        status: str = 'broken'
    ) -> dict[str, Any]:
        """Update damage record and adjust stock accordingly"""
        try:
            with get_session() as session:
                damage = session.get(Damage, damage_id)
                if not damage:
                    return {"success": False, "error": "Damage record not found"}

                old_stock = session.get(Stock, damage.stock_id)
                new_stock = session.get(Stock, stock_id)

                if not new_stock:
                    return {"success": False, "error": "New stock item not found"}

                # Parse damage date
                try:
                    parsed_date = datetime.strptime(damage_date, "%Y-%m-%d").date()
                except ValueError:
                    return {"success": False, "error": "Invalid damage date format (YYYY-MM-DD)"}

                try:
                    damage_status = DamageStatus(status)
                except ValueError:
                    return {"success": False, "error": f"Invalid damage satus: {status}"}

                # Calculate stock adjustments
                old_quantity = damage.quantity_damaged
                quantity_diff = quantity_damaged - old_quantity

                # If changing to different stock item
                if damage.stock_id != stock_id:
                    # Restore quantity to old stock
                    old_stock.quantity += old_quantity
                    old_stock.updated_at = datetime.now()

                    # Check if new stock has sufficient quantity
                    if new_stock.quantity < quantity_damaged:
                        return {"success": False, "error": f"Insufficient stock in {new_stock.item_name}. Available: {new_stock.quantity}"}

                    # Reduce quantity from new stock
                    new_stock.quantity -= quantity_damaged
                    new_stock.updated_at = datetime.now()
                else:
                    # Same stock item, adjust for quantity difference
                    if quantity_diff > 0:  # More damage
                        if old_stock.quantity < quantity_diff:
                            return {"success": False, "error": f"Insufficient stock to increase damage. Available: {old_stock.quantity}"}

                        old_stock.quantity -= quantity_diff
                    else:  # Less damage
                        old_stock.quantity += abs(quantity_diff)

                    old_stock.updated_at = datetime.now()

                # Update damage record
                damage.stock_id = stock_id
                damage.quantity_damaged = quantity_damaged
                damage.damage_date = parsed_date
                damage.damage_status = damage_status

                session.refresh(damage)
                return {
                    "success": True,
                    "damaged_item": {
                        "id": damage.id,
                        "stock_id": damage.stock_id,
                        "item_name": damage.stock.item_name,
                        "quantity_damaged": quantity_damaged,
                        "unit_price": damage.stock.selling_price,
                        "damage_satus": damage_status.value,
                        "damage_date": damage.damage_date
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_damage(damage_id: int) -> dict[str, Any]:
        """Delete damage record and restore stock quantity"""
        try:
            with get_session() as session:
                damage = session.get(Damage, damage_id)
                if not damage:
                    return {"success": False, "error": "Damage record not found"}

                # Restore the damaged quantity back to stock
                stock = session.get(Stock, damage.stock_id)
                stock.quantity += damage.quantity_damaged
                stock.updated_at = datetime.now()

                session.delete(damage)
                return {"success": True, "message": "Damage deleted and stock restored"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ExpenditureAPI:
    """CRUD operations for Expenditure management"""

    @staticmethod
    def create_expenditure(
        description: str,
        amount: float,
        category: str,
        expense_date: str | None = None
    ) -> dict[str, Any]:
        """Create new expenditure record"""
        try:
            with get_session() as session:
                # Validate category
                try:
                    exp_category = ExpenditureCategory(category)
                except ValueError:
                    return {"success": False, "error": f"Invalid category: {category}"}

                # Parse expense date
                parsed_date = date.today()
                if expense_date:
                    try:
                        parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
                    except ValueError:
                        return {"success": False, "error": "Invalid expense date format (YYYY-MM-DD)"}

                expenditure = Expenditure(
                    description=description,
                    amount=amount,
                    category=exp_category,
                    expense_date=parsed_date
                )

                session.add(expenditure)
                session.flush()
                session.refresh(expenditure)

                return {
                    "success": True,
                    "expenditure": ExpenditureRead.model_validate(expenditure).model_dump()
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_expenditures() -> dict[str, Any]:
        """Get all expenditures with period summaries"""
        try:
            with get_session() as session:
                expenditures = session.exec(select(Expenditure)).all()

                # Calculate period totals
                today = date.today()
                current_year = today.year

                # Weekly (last 7 days)
                week_start = today - timedelta(days=7)
                weekly_total = sum(
                    exp.amount for exp in expenditures
                    if exp.expense_date >= week_start
                )

                # Monthly (current month)
                monthly_total = sum(
                    exp.amount for exp in expenditures
                    if exp.expense_date.year == current_year and exp.expense_date.month == today.month
                )

                # Yearly (current year)
                yearly_total = sum(
                    exp.amount for exp in expenditures
                    if exp.expense_date.year == current_year
                )

                return {
                    "success": True,
                    "expenditures": [
                        ExpenditureRead.model_validate(exp).model_dump()
                        for exp in expenditures
                    ],
                    "summary": {
                        "weekly_total": weekly_total,
                        "monthly_total": monthly_total,
                        "yearly_total": yearly_total
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_expenditure(
        expenditure_id: int,
        description: str,
        amount: float,
        category: str,
        expense_date: str
    ) -> dict[str, Any]:
        """Update expenditure record"""
        try:
            with get_session() as session:
                expenditure = session.get(Expenditure, expenditure_id)
                if not expenditure:
                    return {"success": False, "error": "Expenditure not found"}

                # Validate category
                try:
                    exp_category = ExpenditureCategory(category)
                except ValueError:
                    return {"success": False, "error": f"Invalid category: {category}"}

                # Parse expense date
                try:
                    parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
                except ValueError:
                    return {"success": False, "error": "Invalid expense date format (YYYY-MM-DD)"}

                expenditure.description = description
                expenditure.amount = amount
                expenditure.category = exp_category
                expenditure.expense_date = parsed_date
                expenditure.updated_at = datetime.now()

                session.flush()
                return {
                    "success": True,
                    "expenditure": ExpenditureRead.model_validate(expenditure).model_dump()
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_expenditure(expenditure_id: int) -> dict[str, Any]:
        """Delete expenditure record"""
        try:
            with get_session() as session:
                expenditure = session.get(Expenditure, expenditure_id)
                if not expenditure:
                    return {"success": False, "error": "Expenditure not found"}

                session.delete(expenditure)
                return {"success": True, "message": "Expenditure deleted successfully"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def filter_expenditures(search_term: str) -> dict[str, Any]:
        """Filter expenditures by description"""
        try:
            with get_session() as session:
                expenditures = session.exec(
                    select(Expenditure).where(Expenditure.description.contains(search_term))
                ).all()

                return {
                    "success": True,
                    "expenditures": [
                        ExpenditureRead.model_validate(exp).model_dump()
                        for exp in expenditures
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
