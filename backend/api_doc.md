# Smart POS API Documentation

Complete reference for PySide frontend developers to consume the CRUD APIs.

## Admin Details
```python
admin = {'id': 1, 'name': 'admin', 'phone': '+11111111111', 'email': 'admin@smartpos.com', 'password': '1234','role': 'admin', 'created_at': datetime.datetime(2025, 9, 16, 11, 36, 32, 843998), 'updated_at': datetime.datetime(2025, 9, 16, 11, 36, 32, 844341)}
```

## Quick Start

```python
from backend.apis import AccountAPI, StockAPI, SaleAPI, EmployeeAPI, DamageAPI, ExpenditureAPI, ReturnAPI, BusinessLogic

# All methods return: {"success": bool, "data/error": any, ...}
result = AccountAPI.authenticate("user@email.com", "password")
if result["success"]:
    user_data = result["account"]
else:
    show_error(result["error"])

# show_error() is just an hypothetical function to show how result is used
```

## Response Format

All API methods return a dictionary with:
- `"success"`: `bool` - Operation status
- `"error"`: `str` - Error message (when success=False)
- Additional data fields (when success=True)

---

## Account Management

```python
# Login (email/phone + password)
AccountAPI.authenticate(login_credential: str, password: str)
# Returns: {"success": bool, "account": {...}, "error": str}
# account: {"id", "name", "phone", "email", "role", "created_at", "updated_at"}

# Register new account
AccountAPI.create_account(name: str, phone: str, email: str, password: str, role: str = "admin")
# role options: "admin", "manager", "cashier", "sales_person"
# Returns: {"success": bool, "account": {...}, "error": str}
# account: {"id", "name", "phone", "email", "role", "created_at", "updated_at"}

# Get all accounts (for table display)
AccountAPI.get_all_accounts()
# Returns: {"success": bool, "accounts": [{}...]}
# account: {"id", "name", "phone", "email", "role", "created_at", "updated_at"}

# Update account
AccountAPI.update_account(account_id: int, name: str = None, phone: str = None, email: str = None, password: str = None, role: str = None)
# Returns: {"success": bool, "account": {...}, "error": str}
# account: {"id", "name", "phone", "email", "role", "created_at", "updated_at"}

# Delete account
AccountAPI.delete_account(account_id: int)
# Returns: {"success": bool, "message": str, "error": str}
```

---

## Employee Management

```python
# Add new employee
EmployeeAPI.create_employee(
    name: str,
    phone: str,
    ghana_card: str,
    address: str | None = None,
    salary: float | None = None,
    designation: str = "admin"
)
# designation options: "admin", "manager", "cashier", "sales_person"
# Returns: {"success": bool, "employee": {...}, "error": str}
# employee: {"id", "name", "phone", "ghana_card", "address", "hire_date", "salary",
#            "designation", "created_at", "updated_at"}

# Get all employees (for table display)
EmployeeAPI.get_all_employees()
# Returns: {"success": bool, "employees": [{}...], "error": str}
# employee: {"id", "name", "phone", "ghana_card", "address", "hire_date", "salary",
#            "designation", "created_at", "updated_at"}

# Filter employees by phone or Ghana card
EmployeeAPI.filter_employees(search_term: str)
# Returns: {"success": bool, "employees": [{}...], "error": str}
# employee: {"id", "name", "phone", "ghana_card", "address", "hire_date", "salary",
#            "designation", "created_at", "updated_at"}

# Update specific employee field (for inline editing)
EmployeeAPI.update_employee_field(employee_id: int, field: str, value: Any)
# Allowed fields: "name", "phone", "ghana_card", "address", "salary", "designation"
# Returns: {"success": bool, "employee": {...}, "error": str}
# employee: {"id", "name", "phone", "ghana_card", "address", "hire_date", "salary",
#            "designation", "created_at", "updated_at"}

# Delete employee
EmployeeAPI.delete_employee(employee_id: int)
# Returns: {"success": bool, "message": str, "error": str}
```

---

## Stock Management

```python
# Add new stock item
StockAPI.add_stock(
    item_name: str,
    quantity: int,
    cost_price: float,
    selling_price: float,
    category: str = "retail",
    expiry_date: str | None = None   # format: YYYY-MM-DD
)
# category options: "retail", "wholesale"
# If item already exists → updates quantity & prices instead of creating new
# Returns: {"success": bool, "stock_item": {...}, "error": str}
# stock_item: {"id", "item_name", "quantity", "cost_price", "selling_price",
#              "category", "expiry_date", "created_at", "updated_at"}

# Get all stock items with summary
StockAPI.get_all_stock()
# Returns: {"success": bool, "stocks": [{}...], "summary": {...}, "error": str}
# stock: {"id", "item_name", "quantity", "cost_price", "selling_price",
#         "category", "expiry_date", "created_at", "updated_at"}
# summary: {
#   "wholesale_items", "wholesale_cost", "wholesale_value", "wholesale_profit",
#   "retail_items", "retail_cost", "retail_value", "retail_profit"
# }

# Filter stock by item name
StockAPI.filter_stock(search_term: str)
# Returns: {"success": bool, "stocks": [{}...], "error": str}
# stock: {"id", "item_name", "quantity", "cost_price", "selling_price",
#         "category", "expiry_date", "created_at", "updated_at"}

# Update stock item
StockAPI.update_stock(
    stock_id: int,
    item_name: str | None = None,
    quantity: int | None = None,
    cost_price: float | None = None,
    selling_price: float | None = None,
    category: str | None = None,
    expiry_date: str | None = None   # format: YYYY-MM-DD
)
# Returns: {"success": bool, "stock": {...}, "error": str}
# stock: {"id", "item_name", "quantity", "cost_price", "selling_price",
#         "category", "expiry_date", "created_at", "updated_at"}

# Delete stock item
StockAPI.delete_stock(stock_id: int)
# Restriction: Cannot delete stock if it has existing sales records
# Returns: {"success": bool, "message": str, "error": str}
```

---

## Sales Management

```python
# Create a new sale with multiple items
SaleAPI.create_sale(
    cashier_id: int,
    sale_items: list[dict],   # [{"stock_id": int, "quantity_sold": int}, ...]
    amount_paid: float,
    discount_amount: float = 0,
    payment_method: str = "cash",
    sale_date: str | None = None   # format: YYYY-MM-DD
)
# payment_method options: "cash", "card", "mobile_money" (etc, depending on enum)
# Returns: {"success": bool, "sale_id": int, "gross_total": float,
#           "discount": float, "total": float, "items_sold": int,
#           "message": str, "error": str}

# Get daily sales summary
SaleAPI.get_daily_sales_summary(sale_date: str | None = None)   # format: YYYY-MM-DD
# If no date is given → defaults to today
# Returns: {"success": bool, "daily_sales": float, "daily_profit": float,
#           "items_sold": int, "total_discount": float,
#           "transactions_count": int, "error": str}

# Get sale receipt data (for printing)
SaleAPI.get_sale_receipt_data(sale_id: int)
# Returns: {"success": bool, "sale_id": int, "sale_date": date,
#           "sale_time": datetime, "cashier_name": str,
#           "items": [{"item_name", "quantity", "unit_price", "total"}, ...],
#           "gross_total": float, "discount": float, "net_total": float,
#           "amount_paid": float, "change": float, "payment_method": str,
#           "error": str}
```

---

## Damage Management

```python

```
