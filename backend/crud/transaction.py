from typing import Any
from datetime import datetime, timezone
from sqlmodel import select, and_, desc
from backend.storage.database import get_session
from backend.storage.models import Stock, Transaction


class TransactionCRUD:
    """CRUD operations and business logic for Transaction management"""

    @staticmethod
    def create_sale_transaction(data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a sale transaction with automatic calculations

        Args:
            data: dict with keys: stock_id, quantity, user_id (cashier)
        """
        try:
            with get_session() as session:
                # Get stock item
                stock = session.get(Stock, data["stock_id"])
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                quantity = data["quantity"]

                # Business rule: Check stock availability
                if stock.quantity < quantity:
                    return {
                        "success": False,
                        "error": f"Insufficient stock. Available: {stock.quantity}, Requested: {quantity}"
                    }

                # Calculate transaction values
                total_cost = stock.cost_price * quantity
                total_sell = stock.sell_price * quantity
                profit = total_sell - total_cost

                # Create transaction
                transaction = Transaction(
                    stock_id=data["stock_id"],
                    quantity=quantity,
                    total_cost=total_cost,
                    total_sell=total_sell,
                    profit=profit,
                    transaction_type="sale",
                    user_id=data.get("user_id")
                )

                # Update stock quantity
                stock.quantity -= quantity

                session.add(transaction)
                session.add(stock)
                session.commit()
                session.refresh(transaction)

                return {
                    "success": True,
                    "data": {
                        "id": transaction.id,
                        "stock_name": stock.name,
                        "quantity": transaction.quantity,
                        "total_cost": transaction.total_cost,
                        "total_sell": transaction.total_sell,
                        "profit": transaction.profit,
                        "created_at": transaction.created_at,
                        "remaining_stock": stock.quantity
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_restock_transaction(data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a restock transaction

        Args:
            data: dict with keys: stock_id, quantity, user_id
        """
        try:
            with get_session() as session:
                stock = session.get(Stock, data["stock_id"])
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                quantity = data["quantity"]
                total_cost = stock.cost_price * quantity

                # Create restock transaction
                transaction = Transaction(
                    stock_id=data["stock_id"],
                    quantity=quantity,
                    total_cost=total_cost,
                    total_sell=0,
                    profit=-total_cost,  # Negative profit for restocking
                    transaction_type="restock",
                    user_id=data.get("user_id")
                )

                # Update stock quantity
                stock.quantity += quantity

                session.add(transaction)
                session.add(stock)
                session.commit()
                session.refresh(transaction)

                return {
                    "success": True,
                    "data": {
                        "id": transaction.id,
                        "stock_name": stock.name,
                        "quantity": transaction.quantity,
                        "total_cost": transaction.total_cost,
                        "created_at": transaction.created_at,
                        "new_stock_quantity": stock.quantity
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_transaction_by_id(transaction_id: int) -> dict[str, Any]:
        """Get transaction by ID with stock details"""
        try:
            with get_session() as session:
                transaction = session.get(Transaction, transaction_id)
                if not transaction:
                    return {"success": False, "error": "Transaction not found"}

                # Get stock details
                stock = session.get(Stock, transaction.stock_id)

                return {
                    "success": True,
                    "data": {
                        "id": transaction.id,
                        "stock_name": stock.name if stock else "Unknown",
                        "quantity": transaction.quantity,
                        "transaction_type": transaction.transaction_type,
                        "total_cost": transaction.total_cost,
                        "total_sell": transaction.total_sell,
                        "profit": transaction.profit,
                        "created_at": transaction.created_at
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_transactions_by_date_range(start_date: datetime, end_date: datetime) -> dict[str, Any]:
        """Get transactions within date range"""
        try:
            with get_session() as session:
                transactions = session.exec(
                    select(Transaction).where(
                        and_(
                            Transaction.created_at >= start_date,
                            Transaction.created_at <= end_date
                        )
                    ).order_by(desc(Transaction.created_at))
                ).all()

                # Get stock names for each transaction
                result_data = []
                for trans in transactions:
                    stock = session.get(Stock, trans.stock_id)
                    result_data.append({
                        "id": trans.id,
                        "stock_name": stock.name if stock else "Unknown",
                        "quantity": trans.quantity,
                        "transaction_type": trans.transaction_type,
                        "total_cost": trans.total_cost,
                        "total_sell": trans.total_sell,
                        "profit": trans.profit,
                        "created_at": trans.created_at
                    })

                return {"success": True, "data": result_data}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_daily_sales() -> dict[str, Any]:
        """Get today's sales transactions"""
        today = datetime.now(timezone.utc).date()
        start_of_day = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_of_day = datetime.combine(today, datetime.max.time()).replace(tzinfo=timezone.utc)

        return TransactionCRUD.get_transactions_by_date_range(start_of_day, end_of_day)

    @staticmethod
    def get_sales_summary(start_date: datetime, end_date: datetime) -> dict[str, Any]:
        """Get sales summary for a date range"""
        try:
            with get_session() as session:
                # Get sales transactions only
                sales = session.exec(
                    select(Transaction).where(
                        and_(
                            Transaction.transaction_type == "sale",
                            Transaction.created_at >= start_date,
                            Transaction.created_at <= end_date
                        )
                    )
                ).all()

                total_sales = sum(trans.total_sell or 0 for trans in sales)
                total_profit = sum(trans.profit or 0 for trans in sales)
                total_transactions = len(sales)

                return {
                    "success": True,
                    "data": {
                        "total_sales": total_sales,
                        "total_profit": total_profit,
                        "total_transactions": total_transactions,
                        "average_sale": total_sales / total_transactions if total_transactions > 0 else 0,
                        "profit_margin": (total_profit / total_sales * 100) if total_sales > 0 else 0
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def cancel_transaction(transaction_id: int, user_id: int) -> dict[str, Any]:
        """Cancel a transaction and restore stock"""
        try:
            with get_session() as session:
                transaction = session.get(Transaction, transaction_id)
                if not transaction:
                    return {"success": False, "error": "Transaction not found"}

                # Business rule: Only sales can be cancelled
                if transaction.transaction_type != "sale":
                    return {"success": False, "error": "Only sale transactions can be cancelled"}

                # Business rule: Only recent transactions can be cancelled (within 24 hours)
                time_diff = datetime.now(timezone.utc) - transaction.created_at
                if time_diff.total_seconds() > 86400:  # 24 hours
                    return {"success": False, "error": "Transaction too old to cancel"}

                # Restore stock quantity
                stock = session.get(Stock, transaction.stock_id)
                if stock:
                    stock.quantity += transaction.quantity
                    session.add(stock)

                # Delete transaction
                session.delete(transaction)
                session.commit()

                return {"success": True, "message": "Transaction cancelled successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
