from PySide6 import QtCore, QtGui, QtWidgets, QMessageBox, QMainWindow
from ui.return_ui import Ui_Return
from backend.apis import ReturnAPI, StockAPI
from datetime import datetime

class ReturnController:
    def __init__(self, parent=None):
        self.parent = parent
        self.return_window = QMainWindow()
        self.ui = Ui_Return()
        self.ui.setupUi(self.return_window)

        # Connect UI signals to controller methods
        self.ui.btn_save_return.clicked.connect(self.handle_save_return)
        self.ui.btn_edit_return.clicked.connect(self.handle_edit_return)
        self.ui.btn_delete_return.clicked.connect(self.handle_delete_return)
        self.ui.btn_clear_return.clicked.connect(self.handle_clear)
        self.ui.filter_input_return.textChanged.connect(self.filter_returns)
        self.ui.table_return.clicked.connect(self.fill_form_from_selection)

        # Load initial data and update LCDs
        self.load_returns()
        self.update_lcds()

    def load_returns(self):
        # Clear existing rows
        self.ui.table_return.setRowCount(0)

        # Fetch returns from API
        result = ReturnAPI.get_all_returns()
        if result["success"]:
            self.ui.table_return.setRowCount(len(result["returns"]))
            for row, ret in enumerate(result["returns"]):
                self.ui.table_return.setItem(row, 0, QtWidgets.QTableWidgetItem(str(ret["id"])))
                self.ui.table_return.setItem(row, 1, QtWidgets.QTableWidgetItem(ret["item_name"]))
                self.ui.table_return.setItem(row, 2, QtWidgets.QTableWidgetItem(str(ret["quantity"])))
                self.ui.table_return.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{ret['unit_price']:.2f}"))
                self.ui.table_return.setItem(row, 4, QtWidgets.QTableWidgetItem(ret["reason"]))
                self.ui.table_return.setItem(row, 5, QtWidgets.QTableWidgetItem(ret["return_date"]))

                # Action column with delete button
                delete_btn = QtWidgets.QPushButton()
                delete_btn.setObjectName("ReturnTableBtnDelete")
                delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                delete_btn.setToolTip("Delete")
                delete_btn.setFixedSize(30, 30)
                delete_btn.clicked.connect(lambda checked, r=row: self.handle_table_delete(r))
                self.ui.table_return.setCellWidget(row, 6, delete_btn)
        else:
            QMessageBox.warning(self.return_window, "Error", result["error"])

    def handle_save_return(self):
        item_name = self.ui.return_item_name.text().strip()
        quantity = self.ui.return_quantity.text().strip()
        price = self.ui.return_price.text().strip()
        reason = self.ui.return_reason.currentText()

        # Validate all fields are mandatory
        if not all([item_name, quantity, price, reason]):
            QMessageBox.warning(self.return_window, "Input Error", "All fields are mandatory.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self.return_window, "Input Error", "Quantity must be a positive integer and Price must be a positive number.")
            return

        # Find stock ID by item name
        stock_result = StockAPI.filter_stock(item_name)
        if not stock_result["success"] or not stock_result["stocks"]:
            QMessageBox.warning(self.return_window, "Error", "Item not found in stock.")
            return
        stock_id = stock_result["stocks"][0]["id"]

        # Note: sale_id is assumed to be managed by the system or UI (e.g., selected from a sale record)
        # For simplicity, using a placeholder sale_id (1); in practice, this should be dynamic
        result = ReturnAPI.process_return(1, stock_id, quantity, reason, datetime.now().strftime("%Y-%m-%d"))
        if result["success"]:
            QMessageBox.information(self.return_window, "Success", result["message"])
            self.handle_clear()
            self.load_returns()
            self.update_lcds()
        else:
            QMessageBox.warning(self.return_window, "Error", result["error"])

    def handle_edit_return(self):
        selected_row = self.ui.table_return.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.return_window, "Selection Error", "Please select a return to edit.")
            return

        return_id = int(self.ui.table_return.item(selected_row, 0).text())
        quantity = self.ui.return_quantity.text().strip()
        reason = self.ui.return_reason.currentText()
        date = datetime.now().strftime("%Y-%m-%d")  # Current date as placeholder

        if not all([quantity, reason, date]):
            QMessageBox.warning(self.return_window, "Input Error", "All fields are mandatory.")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self.return_window, "Input Error", "Quantity must be a positive integer.")
            return

        result = ReturnAPI.update_return(return_id, quantity, reason, date)
        if result["success"]:
            QMessageBox.information(self.return_window, "Success", result["message"])
            self.handle_clear()
            self.load_returns()
            self.update_lcds()
        else:
            QMessageBox.warning(self.return_window, "Error", result["error"])

    def handle_delete_return(self):
        selected_row = self.ui.table_return.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.return_window, "Selection Error", "Please select a return to delete.")
            return

        return_id = int(self.ui.table_return.item(selected_row, 0).text())
        reply = QMessageBox.question(self.return_window, "Confirm Delete", "Are you sure you want to delete this return?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = ReturnAPI.delete_return(return_id)
            if result["success"]:
                self.load_returns()
                self.update_lcds()
            else:
                QMessageBox.warning(self.return_window, "Error", result["error"])

    def handle_clear(self):
        self.ui.return_item_name.clear()
        self.ui.return_quantity.clear()
        self.ui.return_price.clear()
        self.ui.return_reason.setCurrentIndex(0)

    def filter_returns(self, search_term):
        result = ReturnAPI.filter_returns(search_term)
        if result["success"]:
            self.ui.table_return.setRowCount(0)
            for row, ret in enumerate(result["returns"]):
                self.ui.table_return.setRowCount(self.ui.table_return.rowCount() + 1)
                self.ui.table_return.setItem(row, 0, QtWidgets.QTableWidgetItem(str(ret["id"])))
                self.ui.table_return.setItem(row, 1, QtWidgets.QTableWidgetItem(ret["item_name"]))
                self.ui.table_return.setItem(row, 2, QtWidgets.QTableWidgetItem(str(ret["quantity"])))
                self.ui.table_return.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{ret['refund_amount'] / ret['quantity']:.2f}"))  # Recalculate unit price
                self.ui.table_return.setItem(row, 4, QtWidgets.QTableWidgetItem(ret["reason"]))
                self.ui.table_return.setItem(row, 5, QtWidgets.QTableWidgetItem(ret["return_date"]))

                delete_btn = QtWidgets.QPushButton()
                delete_btn.setObjectName("ReturnTableBtnDelete")
                delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                delete_btn.setToolTip("Delete")
                delete_btn.setFixedSize(30, 30)
                delete_btn.clicked.connect(lambda checked, r=row: self.handle_table_delete(r))
                self.ui.table_return.setCellWidget(row, 6, delete_btn)
        else:
            QMessageBox.warning(self.return_window, "Error", result["error"])

    def fill_form_from_selection(self):
        selected_row = self.ui.table_return.currentRow()
        if selected_row != -1:
            self.ui.return_item_name.setText(self.ui.table_return.item(selected_row, 1).text())
            self.ui.return_quantity.setText(self.ui.table_return.item(selected_row, 2).text())
            self.ui.return_price.setText(self.ui.table_return.item(selected_row, 3).text())
            self.ui.return_reason.setCurrentText(self.ui.table_return.item(selected_row, 4).text())

    def handle_table_delete(self, row):
        return_id = int(self.ui.table_return.item(row, 0).text())
        reply = QMessageBox.question(self.return_window, "Confirm Delete", "Are you sure you want to delete this return?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = ReturnAPI.delete_return(return_id)
            if result["success"]:
                self.load_returns()
                self.update_lcds()
            else:
                QMessageBox.warning(self.return_window, "Error", result["error"])

    def update_lcds(self):
        result = ReturnAPI.get_all_returns()
        if result["success"]:
            summary = result["summary"]
            self.ui.lcdTotalReturnedItems.display(summary["total_items"])
            self.ui.lcdTotalRefundAmount.display(summary["total_refund"])
            self.ui.lcdTotalLoss.display(summary["total_loss"])

    def show(self):
        self.return_window.show()