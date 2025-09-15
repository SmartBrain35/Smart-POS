# Smart POS API Documentation

Complete reference for PySide frontend developers to consume the CRUD APIs.

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

### Authentication & User Management

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