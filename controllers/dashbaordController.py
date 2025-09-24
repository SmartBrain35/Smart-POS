from PySide6.QtWidgets import QMessageBox
from backend.apis import DashboardAPI


class DashboardController:
    def __init__(self, ui):
        self.ui = ui
        self.load_kpis()

        # Connect refresh button
        self.ui.btnRefreshDashboard.clicked.connect(self.load_kpis)

    def load_kpis(self):
        """Load dashboard KPIs and display them."""
        resp = DashboardAPI.get_kpis()
        if not resp.get("success"):
            QMessageBox.warning(
                self.ui, "Error", resp.get("error", "Failed to load dashboard data")
            )
            return

        kpis = resp["kpis"]

        # Update UI labels with KPI values
        self.ui.lblRevenue.setText(f"{kpis['total_revenue']:.2f}")
        self.ui.lblProfit.setText(f"{kpis['total_profit']:.2f}")
        self.ui.lblTransactions.setText(str(kpis["total_transactions"]))
        self.ui.lblLowStock.setText(str(kpis["low_stock_count"]))

        # Show list of low stock items
        low_items = (
            ", ".join(kpis["low_stock_items"]) if kpis["low_stock_items"] else "None"
        )
        self.ui.lblLowStockItems.setText(low_items)
