from typing import Any
from datetime import datetime, timezone, timedelta
from sqlmodel import select, and_, or_, func, desc
from backend.storage.database import get_session
from backend.storage.models import Stock, Transaction


class AnalyticsCRUD:
    """Advanced analytics and business intelligence operations"""

    @staticmethod
    def get_product_performance(days: int = 30) -> dict[str, Any]:
        """Get product performance analytics"""
        try:
            with get_session() as session:
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

                # Get product performance data
                performance = session.exec(
                    select(
                        Stock.id,
                        Stock.name,
                        Stock.sell_price,
                        Stock.cost_price,
                        Stock.quantity,
                        func.sum(Transaction.quantity).label("total_sold"),
                        func.sum(Transaction.total_sell).label("total_revenue"),
                        func.sum(Transaction.profit).label("total_profit"),
                        func.count(Transaction.id).label("transaction_count")
                    ).outerjoin(Transaction)
                    .where(
                        or_(
                            Transaction.created_at >= cutoff_date,
                            Transaction.created_at.is_(None)
                        )
                    )
                    .group_by(Stock.id)
                    .order_by(desc("total_revenue"))
                ).all()

                return {
                    "success": True,
                    "data": [
                        {
                            "stock_id": p.id,
                            "name": p.name,
                            "current_stock": p.quantity,
                            "sell_price": p.sell_price,
                            "cost_price": p.cost_price,
                            "total_sold": p.total_sold or 0,
                            "total_revenue": p.total_revenue or 0,
                            "total_profit": p.total_profit or 0,
                            "transaction_count": p.transaction_count or 0,
                            "profit_margin": ((p.sell_price - p.cost_price) / p.sell_price * 100) if p.sell_price > 0 else 0
                        } for p in performance
                    ]
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_sales_trends(days: int = 30) -> dict[str, Any]:
        """Get daily sales trends"""
        try:
            with get_session() as session:
                cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

                # Get daily sales data
                daily_sales = session.exec(
                    select(
                        func.date(Transaction.created_at).label("sale_date"),
                        func.sum(Transaction.total_sell).label("daily_sales"),
                        func.sum(Transaction.profit).label("daily_profit"),
                        func.count(Transaction.id).label("transaction_count")
                    ).where(
                        and_(
                            Transaction.transaction_type == "sale",
                            Transaction.created_at >= cutoff_date
                        )
                    )
                    .group_by(func.date(Transaction.created_at))
                    .order_by("sale_date")
                ).all()

                return {
                    "success": True,
                    "data": [
                        {
                            "date": str(day.sale_date),
                            "sales": day.daily_sales or 0,
                            "profit": day.daily_profit or 0,
                            "transactions": day.transaction_count or 0
                        } for day in daily_sales
                    ]
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_inventory_valuation() -> dict[str, Any]:
        """Get current inventory valuation"""
        try:
            with get_session() as session:
                valuation = session.exec(
                    select(
                        func.sum(Stock.cost_price * Stock.quantity).label("cost_value"),
                        func.sum(Stock.sell_price * Stock.quantity).label("sell_value"),
                        func.count(Stock.id).label("total_items"),
                        func.sum(Stock.quantity).label("total_quantity")
                    )
                ).one()

                potential_profit = (valuation.sell_value or 0) - (valuation.cost_value or 0)

                return {
                    "success": True,
                    "data": {
                        "cost_value": valuation.cost_value or 0,
                        "sell_value": valuation.sell_value or 0,
                        "potential_profit": potential_profit,
                        "total_items": valuation.total_items or 0,
                        "total_quantity": valuation.total_quantity or 0,
                        "margin_percentage": (potential_profit / valuation.sell_value * 100) if valuation.sell_value else 0
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}
