from typing import Any
from sqlmodel import select, or_
from backend.storage.database import get_session
from backend.storage.models import Stock, Transaction


class StockCRUD:
    """CRUD operations and business logic for Stock/Inventory management"""

    @staticmethod
    def create_stock_item(data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new stock item with business validation

        Args:
            data: dict with stock information (name, description, cost_price, sell_price, quantity)
        """
        try:
            with get_session() as session:
                # Business rule: Sell price should be higher than cost price
                if data["sell_price"] <= data["cost_price"]:
                    return {"success": False, "error": "Sell price must be higher than cost price"}

                # Check if item with same name already exists
                existing = session.exec(
                    select(Stock).where(Stock.name == data["name"])
                ).first()

                if existing:
                    return {"success": False, "error": "Stock item with this name already exists"}

                stock = Stock(**data)
                session.add(stock)
                session.commit()
                session.refresh(stock)

                return {
                    "success": True,
                    "data": {
                        "id": stock.id,
                        "name": stock.name,
                        "description": stock.description,
                        "cost_price": stock.cost_price,
                        "sell_price": stock.sell_price,
                        "quantity": stock.quantity,
                        "created_at": stock.created_at
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_stock_by_id(stock_id: int) -> dict[str, Any]:
        """Get stock item by ID"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                return {
                    "success": True,
                    "data": {
                        "id": stock.id,
                        "name": stock.name,
                        "description": stock.description,
                        "cost_price": stock.cost_price,
                        "sell_price": stock.sell_price,
                        "quantity": stock.quantity,
                        "created_at": stock.created_at
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_stock() -> dict[str, Any]:
        """Get all stock items"""
        try:
            with get_session() as session:
                stocks = session.exec(select(Stock)).all()
                return {
                    "success": True,
                    "data": [
                        {
                            "id": stock.id,
                            "name": stock.name,
                            "description": stock.description,
                            "cost_price": stock.cost_price,
                            "sell_price": stock.sell_price,
                            "quantity": stock.quantity,
                            "created_at": stock.created_at
                        } for stock in stocks
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_low_stock_items(threshold: int = 10) -> dict[str, Any]:
        """Get items with low stock (business logic for inventory alerts)"""
        try:
            with get_session() as session:
                low_stock = session.exec(
                    select(Stock).where(Stock.quantity <= threshold)
                ).all()

                return {
                    "success": True,
                    "data": [
                        {
                            "id": stock.id,
                            "name": stock.name,
                            "quantity": stock.quantity,
                            "threshold": threshold
                        } for stock in low_stock
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def search_stock(search_term: str) -> dict[str, Any]:
        """Search stock by name or description"""
        try:
            with get_session() as session:
                stocks = session.exec(
                    select(Stock).where(
                        or_(
                            Stock.name.contains(search_term),
                            Stock.description.contains(search_term)
                        )
                    )
                ).all()

                return {
                    "success": True,
                    "data": [
                        {
                            "id": stock.id,
                            "name": stock.name,
                            "description": stock.description,
                            "cost_price": stock.cost_price,
                            "sell_price": stock.sell_price,
                            "quantity": stock.quantity
                        } for stock in stocks
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_stock_item(stock_id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update stock item with business validation"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                # Business validation: sell price > cost price
                cost_price = data.get("cost_price", stock.cost_price)
                sell_price = data.get("sell_price", stock.sell_price)

                if sell_price <= cost_price:
                    return {"success": False, "error": "Sell price must be higher than cost price"}

                # Update fields
                for field, value in data.items():
                    if hasattr(stock, field) and value is not None:
                        setattr(stock, field, value)

                session.add(stock)
                session.commit()
                session.refresh(stock)

                return {
                    "success": True,
                    "data": {
                        "id": stock.id,
                        "name": stock.name,
                        "description": stock.description,
                        "cost_price": stock.cost_price,
                        "sell_price": stock.sell_price,
                        "quantity": stock.quantity
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def adjust_stock_quantity(stock_id: int, adjustment: int, reason: str = "") -> dict[str, Any]:
        """Adjust stock quantity (for restocking or corrections)"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                new_quantity = stock.quantity + adjustment

                # Business rule: Quantity cannot be negative
                if new_quantity < 0:
                    return {"success": False, "error": "Insufficient stock quantity"}

                stock.quantity = new_quantity
                session.add(stock)
                session.commit()

                return {
                    "success": True,
                    "data": {
                        "id": stock.id,
                        "name": stock.name,
                        "old_quantity": stock.quantity - adjustment,
                        "new_quantity": stock.quantity,
                        "adjustment": adjustment
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_stock_item(stock_id: int) -> dict[str, Any]:
        """Delete stock item"""
        try:
            with get_session() as session:
                stock = session.get(Stock, stock_id)
                if not stock:
                    return {"success": False, "error": "Stock item not found"}

                # Business rule: Check if item has transactions
                transactions = session.exec(
                    select(Transaction).where(Transaction.stock_id == stock_id)
                ).all()

                if transactions:
                    return {"success": False, "error": "Cannot delete stock item with existing transactions"}

                session.delete(stock)
                session.commit()

                return {"success": True, "message": "Stock item deleted successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
