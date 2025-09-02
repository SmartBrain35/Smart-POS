from backend.storage.models import Transaction, Stock
from backend.crud.transaction import TransactionCRUD
from typing import Any
from datetime import datetime, timezone
from backend.storage.database import get_session


class POSCRUD:
    """Main POS operations combining multiple entities"""

    @staticmethod
    def process_sale(cart_items: list[dict[str, Any]], user_id: int) -> dict[str, Any]:
        """
        Process a complete sale with multiple items

        Args:
            cart_items: list of dicts with keys: stock_id, quantity
            user_id: ID of the cashier processing the sale

        Returns:
            dict with sale receipt data
        """
        try:
            receipt_items = []
            total_amount = 0
            total_profit = 0

            # Process each item in the cart
            for item in cart_items:
                result = TransactionCRUD.create_sale_transaction({
                    "stock_id": item["stock_id"],
                    "quantity": item["quantity"],
                    "user_id": user_id
                })

                if not result["success"]:
                    return {
                        "success": False,
                        "error": f"Failed to process item: {result['error']}"
                    }

                item_data = result["data"]
                receipt_items.append(item_data)
                total_amount += item_data["total_sell"]
                total_profit += item_data["profit"]

            return {
                "success": True,
                "data": {
                    "receipt_items": receipt_items,
                    "total_amount": total_amount,
                    "total_profit": total_profit,
                    "transaction_count": len(receipt_items),
                    "processed_at": datetime.now(timezone.utc),
                    "cashier_id": user_id
                }
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def check_stock_availability(items: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Check if all items in cart are available in sufficient quantity

        Args:
            items: list of dicts with keys: stock_id, quantity
        """
        try:
            with get_session() as session:
                availability_issues = []

                for item in items:
                    stock = session.get(Stock, item["stock_id"])
                    if not stock:
                        availability_issues.append({
                            "stock_id": item["stock_id"],
                            "issue": "Stock item not found"
                        })
                        continue

                    if stock.quantity < item["quantity"]:
                        availability_issues.append({
                            "stock_id": item["stock_id"],
                            "stock_name": stock.name,
                            "requested": item["quantity"],
                            "available": stock.quantity,
                            "issue": "Insufficient quantity"
                        })

                return {
                    "success": len(availability_issues) == 0,
                    "data": {
                        "all_available": len(availability_issues) == 0,
                        "issues": availability_issues
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_sale_receipt(transaction_ids: list[int]) -> dict[str, Any]:
        """Generate receipt for multiple transaction IDs"""
        try:
            with get_session() as session:
                receipt_items = []
                total_amount = 0

                for trans_id in transaction_ids:
                    transaction = session.get(Transaction, trans_id)
                    if transaction and transaction.transaction_type == "sale":
                        stock = session.get(Stock, transaction.stock_id)
                        receipt_items.append({
                            "name": stock.name if stock else "Unknown",
                            "quantity": transaction.quantity,
                            "unit_price": stock.sell_price if stock else 0,
                            "total": transaction.total_sell
                        })
                        total_amount += transaction.total_sell or 0

                return {
                    "success": True,
                    "data": {
                        "items": receipt_items,
                        "total_amount": total_amount,
                        "generated_at": datetime.now(timezone.utc)
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}
