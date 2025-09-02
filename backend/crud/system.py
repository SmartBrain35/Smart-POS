from typing import Any
from datetime import datetime, timezone
from sqlmodel import select, func
from backend.storage.database import get_session
from backend.storage.models import User, Employee, Stock, Transaction, Report


class SystemCRUD:
    """System-wide operations and maintenance"""

    @staticmethod
    def backup_data() -> dict[str, Any]:
        """Create a data backup (returns summary for UI)"""
        try:
            with get_session() as session:
                # Count all records
                user_count = session.exec(select(func.count(User.id))).one()
                employee_count = session.exec(select(func.count(Employee.id))).one()
                stock_count = session.exec(select(func.count(Stock.id))).one()
                transaction_count = session.exec(select(func.count(Transaction.id))).one()
                report_count = session.exec(select(func.count(Report.id))).one()

                return {
                    "success": True,
                    "data": {
                        "backup_timestamp": datetime.now(timezone.utc),
                        "records": {
                            "users": user_count,
                            "employees": employee_count,
                            "stock_items": stock_count,
                            "transactions": transaction_count,
                            "reports": report_count
                        }
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_system_stats() -> dict[str, Any]:
        """Get system statistics for admin dashboard"""
        try:
            with get_session() as session:
                stats = {
                    "total_users": session.exec(select(func.count(User.id))).one(),
                    "total_employees": session.exec(select(func.count(Employee.id))).one(),
                    "total_stock_items": session.exec(select(func.count(Stock.id))).one(),
                    "total_transactions": session.exec(select(func.count(Transaction.id))).one(),
                    "low_stock_items": session.exec(
                        select(func.count(Stock.id)).where(Stock.quantity <= 10)
                    ).one(),
                    "out_of_stock_items": session.exec(
                        select(func.count(Stock.id)).where(Stock.quantity == 0)
                    ).one()
                }

                # Get database size (approximate)
                total_records = sum([
                    stats["total_users"],
                    stats["total_employees"],
                    stats["total_stock_items"],
                    stats["total_transactions"]
                ])

                return {
                    "success": True,
                    "data": {
                        **stats,
                        "total_records": total_records,
                        "last_updated": datetime.now(timezone.utc)
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def cleanup_old_data(days_old: int = 365) -> dict[str, Any]:
        """Clean up old data (reports and transactions older than specified days)"""
        try:
            with get_session() as session:
                cutoff_date = datetime.now(timezone.utc) - datetime.timedelta(days=days_old)

                # Count old records before deletion
                old_transactions = session.exec(
                    select(func.count(Transaction.id)).where(Transaction.created_at < cutoff_date)
                ).one()

                old_reports = session.exec(
                    select(func.count(Report.id)).where(Report.generated_at < cutoff_date)
                ).one()

                # Delete old records (business rule: keep recent data for analysis)
                session.exec(
                    select(Transaction).where(Transaction.created_at < cutoff_date)
                )
                for trans in session.exec(
                    select(Transaction).where(Transaction.created_at < cutoff_date)
                ).all():
                    session.delete(trans)

                session.exec(
                    select(Report).where(Report.generated_at < cutoff_date)
                )
                for report in session.exec(
                    select(Report).where(Report.generated_at < cutoff_date)
                ).all():
                    session.delete(report)

                session.commit()

                return {
                    "success": True,
                    "data": {
                        "deleted_transactions": old_transactions,
                        "deleted_reports": old_reports,
                        "cutoff_date": cutoff_date
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}


# Usage Examples for PySide Integration:
"""
# Example usage in PySide components:

# Login
result = UserCRUD.authenticate_user("admin", "password123")
if result["success"]:
    user_data = result["data"]
    # Proceed with login
else:
    # Show error message

# Create sale
cart = [
    {"stock_id": 1, "quantity": 2},
    {"stock_id": 3, "quantity": 1}
]
sale_result = POSCRUD.process_sale(cart, current_user_id)

# Check stock before sale
availability = POSCRUD.check_stock_availability(cart)
if availability["data"]["all_available"]:
    # Proceed with sale
else:
    # Show availability issues

# Get dashboard data
dashboard_data = ReportCRUD.get_dashboard_summary()

# Add new stock item
new_item = {
    "name": "New Product",
    "description": "Product description",
    "cost_price": 10.0,
    "sell_price": 15.0,
    "quantity": 100
}
result = StockCRUD.create_stock_item(new_item)

# Generate daily report
report = ReportCRUD.generate_daily_report()
"""
