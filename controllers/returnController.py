from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from backend.apis import ReturnAPI


class ReturnController:
    def __init__(self, ui):
        self.ui = ui
        self.load_returns()

        # Connect buttons
        self.ui.btnProcessReturn.clicked.connect(self.process_return)
        self.ui.btnRefreshReturns.clicked.connect(self.load_returns)

    def load_returns(self):
        """Load all product returns into the table."""
        resp = ReturnAPI.get_all_returns()
        if not resp.get("success"):
            QMessageBox.warning(
                self.ui, "Error", resp.get("error", "Failed to fetch returns")
            )
            return

        returns = resp["returns"]
        self.ui.tableReturns.setRowCount(0)

        for row, ret in enumerate(returns):
            self.ui.tableReturns.insertRow(row)
            self.ui.tableReturns.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(ret["id"]))
            )
            self.ui.tableReturns.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(ret["sale_id"]))
            )
            self.ui.tableReturns.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(ret["stock_id"]))
            )
            self.ui.tableReturns.setItem(
                row, 3, QtWidgets.QTableWidgetItem(str(ret["quantity"]))
            )
            self.ui.tableReturns.setItem(
                row, 4, QtWidgets.QTableWidgetItem(ret["reason"])
            )
            self.ui.tableReturns.setItem(
                row, 5, QtWidgets.QTableWidgetItem(ret["return_date"])
            )

    def process_return(self):
        """Process a new return request."""
        sale_id = int(self.ui.txtSaleID.text())
        stock_id = int(self.ui.txtStockID.text())
        qty = int(self.ui.spinQuantity.value())
        reason = self.ui.cboReason.currentText().lower()

        resp = ReturnAPI.process_return(sale_id, stock_id, qty, reason)
        if not resp.get("success"):
            QMessageBox.warning(
                self.ui, "Error", resp.get("error", "Failed to process return")
            )
            return

        QMessageBox.information(self.ui, "Success", "Return processed successfully")
        self.load_returns()
