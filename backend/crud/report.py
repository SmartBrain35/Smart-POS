from typing import Any
from datetime import datetime, timezone
from sqlmodel import select, and_, func, desc
from backend.storage.database import get_session
from backend.storage.models import Stock, Transaction, Report
from backend.crud.transaction import TransactionCRUD


class ReportCRUD:
    """CRUD operations and business logic for Report generation"""

    @staticmethod
    def generate_daily_report(date: datetime = None) -> dict[str, Any]:
        """Generate daily sales report"""
        if date is None:
            date = datetime.now(timezone.utc).date()

        start_of_day = datetime.combine(date, datetime.min.time()).replace(tzinfo=timezone.utc)
        end_of_day = datetime.combine(date, datetime.max.time()).replace(tzinfo=timezone.utc)

        try:
            with get_session() as session:
                # Get sales data for the day
                sales_summary = TransactionCRUD.get_sales_summary(start_of_day, end_of_day)

                if not sales_summary["success"]:
                    return sales_summary

                summary_data = sales_summary["data"]

                # Create report record
                report = Report(
                    report_type="daily",
                    report_date=date,
                    total_sales=summary_data["total_sales"],
                    total_profit=summary_data["total_profit"],
                    metadata={
                        "total_transactions": summary_data["total_transactions"],
                        "average_sale": summary_data["average_sale"],
                        "profit_margin": summary_data["profit_margin"]
                    }
                )

                session.add(report)
                session.commit()
                session.refresh(report)

                return {
                    "success": True,
                    "data": {
                        "id": report.id,
                        "report_type": report.report_type,
                        "report_date": report.report_date,
                        "total_sales": report.total_sales,
                        "total_profit": report.total_profit,
                        "generated_at": report.generated_at,
                        "details": summary_data
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def generate_monthly_report(year: int, month: int) -> dict[str, Any]:
        """Generate monthly sales report"""
        try:
            from calendar import monthrange

            # Get first and last day of month
            start_date = datetime(year, month, 1, tzinfo=timezone.utc)
            last_day = monthrange(year, month)[1]
            end_date = datetime(year, month, last_day, 23, 59, 59, tzinfo=timezone.utc)

            with get_session() as session:
                # Get sales summary for the month
                sales_summary = TransactionCRUD.get_sales_summary(start_date, end_date)

                if not sales_summary["success"]:
                    return sales_summary

                summary_data = sales_summary["data"]

                # Get top selling products
                top_products = session.exec(
                    select(
                        Stock.name,
                        func.sum(Transaction.quantity).label("total_sold"),
                        func.sum(Transaction.total_sell).label("total_revenue")
                    ).join(Stock)
                    .where(
                        and_(
                            Transaction.transaction_type == "sale",
                            Transaction.created_at >= start_date,
                            Transaction.created_at <= end_date
                        )
                    )
                    .group_by(Stock.id, Stock.name)
                    .order_by(desc("total_sold"))
                    .limit(10)
                ).all()

                # Create report
                report = Report(
                    report_type="monthly",
                    report_date=start_date.date(),
                    total_sales=summary_data["total_sales"],
                    total_profit=summary_data["total_profit"],
                    metadata={
                        "year": year,
                        "month": month,
                        "total_transactions": summary_data["total_transactions"],
                        "average_sale": summary_data["average_sale"],
                        "profit_margin": summary_data["profit_margin"],
                        "top_products": [
                            {
                                "name": product.name,
                                "quantity_sold": product.total_sold,
                                "revenue": product.total_revenue
                            } for product in top_products
                        ]
                    }
                )

                session.add(report)
                session.commit()
                session.refresh(report)

                return {
                    "success": True,
                    "data": {
                        "id": report.id,
                        "report_type": report.report_type,
                        "report_date": report.report_date,
                        "total_sales": report.total_sales,
                        "total_profit": report.total_profit,
                        "generated_at": report.generated_at,
                        "details": report.metadata
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_report_by_id(report_id: int) -> dict[str, Any]:
        """Get report by ID"""
        try:
            with get_session() as session:
                report = session.get(Report, report_id)
                if not report:
                    return {"success": False, "error": "Report not found"}

                return {
                    "success": True,
                    "data": {
                        "id": report.id,
                        "report_type": report.report_type,
                        "report_date": report.report_date,
                        "total_sales": report.total_sales,
                        "total_profit": report.total_profit,
                        "generated_at": report.generated_at,
                        "metadata": report.metadata
                    }
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_all_reports(report_type: str = None) -> dict[str, Any]:
        """Get all reports, optionally filtered by type"""
        try:
            with get_session() as session:
                query = select(Report)
                if report_type:
                    query = query.where(Report.report_type == report_type)

                reports = session.exec(query.order_by(desc(Report.generated_at))).all()

                return {
                    "success": True,
                    "data": [
                        {
                            "id": report.id,
                            "report_type": report.report_type,
                            "report_date": report.report_date,
                            "total_sales": report.total_sales,
                            "total_profit": report.total_profit,
                            "generated_at": report.generated_at
                        } for report in reports
                    ]
                }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_dashboard_summary() -> dict[str, Any]:
        """Get dashboard summary with key metrics"""
        try:
            with get_session() as session:
                today = datetime.now(timezone.utc).date()
                start_of_day = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)

                # Today's sales
                today_sales = TransactionCRUD.get_sales_summary(start_of_day, datetime.now(timezone.utc))

                # Total stock value
                stock_value = session.exec(
                    select(func.sum(Stock.cost_price * Stock.quantity))
                ).one() or 0

                # Low stock count
                low_stock_count = session.exec(
                    select(func.count(Stock.id)).where(Stock.quantity <= 10)
                ).one() or 0

                # Recent transactions (last 10)
                recent_transactions = session.exec(
                    select(Transaction)
                    .order_by(desc(Transaction.created_at))
                    .limit(10)
                ).all()

                recent_trans_data = []
                for trans in recent_transactions:
                    stock = session.get(Stock, trans.stock_id)
                    recent_trans_data.append({
                        "id": trans.id,
                        "stock_name": stock.name if stock else "Unknown",
                        "quantity": trans.quantity,
                        "type": trans.transaction_type,
                        "amount": trans.total_sell if trans.transaction_type == "sale" else trans.total_cost,
                        "created_at": trans.created_at
                    })

                return {
                    "success": True,
                    "data": {
                        "today_sales": today_sales["data"] if today_sales["success"] else {},
                        "total_stock_value": stock_value,
                        "low_stock_count": low_stock_count,
                        "recent_transactions": recent_trans_data
                    }
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_report(report_id: int) -> dict[str, Any]:
        """Delete report"""
        try:
            with get_session() as session:
                report = session.get(Report, report_id)
                if not report:
                    return {"success": False, "error": "Report not found"}

                session.delete(report)
                session.commit()

                return {"success": True, "message": "Report deleted successfully"}

        except Exception as e:
            return {"success": False, "error": str(e)}
