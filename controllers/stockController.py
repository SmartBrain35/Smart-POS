from PySide6 import QMessageBox, QMainWindow, QtWidgets
from PySide6.QtCore import Qt, QTimer, QtCore
from ui.stock_ui import Ui_Stock
from backend.apis import StockAPI
from PySide6.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime

class StockController:
    def __init__(self, parent=None):
        self.parent = parent
        self.stock_window = QMainWindow()
        self.ui = Ui_Stock()
        self.ui.setupUi(self.stock_window)

        # Connect UI signals to controller methods
        self.ui.btn_add_stock.clicked.connect(self.handle_add_stock)
        self.ui.btn_edit_stock.clicked.connect(self.handle_edit_stock)
        self.ui.btn_delete_stock.clicked.connect(self.handle_delete_stock)
        self.ui.btn_clear_stock.clicked.connect(self.handle_clear)
        self.ui.table_stock.clicked.connect(self.fill_form_from_selection)
        self.ui.stock_filter_input.textChanged.connect(self.filter_stock)

        # Setup model for table
        self.model = QStandardItemModel()
        self.ui.table_stock.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["ID", "Item Name", "Quantity", "Cost Price", "Selling Price", "Category", "Expiry Date"])
        self.ui.table_stock.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # Load initial data
        self.load_stock_data()

        # Setup auto-update for LCDs
        self.update_lcds()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lcds)
        self.timer.start(1000)  # Update every second

    def load_stock_data(self):
        result = StockAPI.get_all_stock()
        if result["success"]:
            self.model.removeRows(0, self.model.rowCount())
            for stock in result["stocks"]:
                items = [
                    QStandardItem(str(stock["id"])),
                    QStandardItem(stock["item_name"]),
                    QStandardItem(str(stock["quantity"])),
                    QStandardItem(f"{stock['cost_price']:.2f}"),
                    QStandardItem(f"{stock['selling_price']:.2f}"),
                    QStandardItem(stock["category"]),
                    QStandardItem(stock["expiry_date"] if stock["expiry_date"] else "")
                ]
                self.model.appendRow(items)
                # Add progress bar for quantity
                progress = QtWidgets.QProgressBar()
                progress.setRange(0, 100)
                progress.setValue(stock["quantity"])
                self.ui.table_stock.setIndexWidget(self.model.index(self.model.rowCount() - 1, 2), progress)
        else:
            QMessageBox.warning(self.stock_window, "Error", result["error"])

    def handle_add_stock(self):
        item_name = self.ui.stock_name_input.text().strip()
        quantity = self.ui.stock_qty_input.text().strip()
        cost_price = self.ui.stock_cost_input.text().strip()
        selling_price = self.ui.stock_selling_input.text().strip()
        category = self.ui.stock_category_input.currentText()
        expiry_date = self.ui.stock_expiry_date.date().toString("yyyy-MM-dd") if self.ui.stock_expiry_checkbox.isChecked() else None

        # Validate all fields
        if not all([item_name, quantity, cost_price, selling_price, category]):
            QMessageBox.warning(self.stock_window, "Input Error", "All fields are compulsory.")
            return

        try:
            quantity = int(quantity)
            cost_price = float(cost_price)
            selling_price = float(selling_price)
            if quantity <= 0 or cost_price < 0 or selling_price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self.stock_window, "Input Error", "Invalid numeric values.")
            return

        result = StockAPI.add_stock(item_name, quantity, cost_price, selling_price, category, expiry_date)
        if result["success"]:
            QMessageBox.information(self.stock_window, "Success", result["message"])
            self.handle_clear()
            self.load_stock_data()
        else:
            QMessageBox.warning(self.stock_window, "Error", result["error"])

    def handle_edit_stock(self):
        selected_row = self.ui.table_stock.currentIndex().row()
        if selected_row == -1:
            QMessageBox.warning(self.stock_window, "Selection Error", "Please select a stock item to edit.")
            return

        stock_id = int(self.model.data(self.model.index(selected_row, 0)))
        item_name = self.ui.stock_name_input.text().strip()
        quantity = self.ui.stock_qty_input.text().strip()
        cost_price = self.ui.stock_cost_input.text().strip()
        selling_price = self.ui.stock_selling_input.text().strip()
        category = self.ui.stock_category_input.currentText()
        expiry_date = self.ui.stock_expiry_date.date().toString("yyyy-MM-dd") if self.ui.stock_expiry_checkbox.isChecked() else None

        if not all([item_name, quantity, cost_price, selling_price, category]):
            QMessageBox.warning(self.stock_window, "Input Error", "All fields are compulsory.")
            return

        try:
            quantity = int(quantity)
            cost_price = float(cost_price)
            selling_price = float(selling_price)
            if quantity < 0 or cost_price < 0 or selling_price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self.stock_window, "Input Error", "Invalid numeric values.")
            return

        result = StockAPI.update_stock(stock_id, item_name, quantity, cost_price, selling_price, category, expiry_date)
        if result["success"]:
            QMessageBox.information(self.stock_window, "Success", result["message"])
            self.handle_clear()
            self.load_stock_data()
        else:
            QMessageBox.warning(self.stock_window, "Error", result["error"])

    def handle_delete_stock(self):
        selected_row = self.ui.table_stock.currentIndex().row()
        if selected_row == -1:
            QMessageBox.warning(self.stock_window, "Selection Error", "Please select a stock item to delete.")
            return

        stock_id = int(self.model.data(self.model.index(selected_row, 0)))
        reply = QMessageBox.question(self.stock_window, "Confirm Delete", "Are you sure you want to delete this stock?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = StockAPI.delete_stock(stock_id)
            if result["success"]:
                self.load_stock_data()
            else:
                QMessageBox.warning(self.stock_window, "Error", result["error"])

    def handle_clear(self):
        self.ui.stock_id_input.clear()
        self.ui.stock_name_input.clear()
        self.ui.stock_qty_input.clear()
        self.ui.stock_cost_input.clear()
        self.ui.stock_selling_input.clear()
        self.ui.stock_category_input.setCurrentIndex(0)
        self.ui.stock_expiry_checkbox.setChecked(False)
        self.ui.stock_expiry_date.setEnabled(False)

    def fill_form_from_selection(self):
        selected_row = self.ui.table_stock.currentIndex().row()
        if selected_row != -1:
            self.ui.stock_id_input.setText(self.model.data(self.model.index(selected_row, 0)))
            self.ui.stock_name_input.setText(self.model.data(self.model.index(selected_row, 1)))
            self.ui.stock_qty_input.setText(self.model.data(self.model.index(selected_row, 2)))
            self.ui.stock_cost_input.setText(self.model.data(self.model.index(selected_row, 3)))
            self.ui.stock_selling_input.setText(self.model.data(self.model.index(selected_row, 4)))
            self.ui.stock_category_input.setCurrentText(self.model.data(self.model.index(selected_row, 5)))
            expiry_date = self.model.data(self.model.index(selected_row, 6))
            if expiry_date:
                self.ui.stock_expiry_checkbox.setChecked(True)
                self.ui.stock_expiry_date.setDate(QtCore.QDate.fromString(expiry_date, "yyyy-MM-dd"))
                self.ui.stock_expiry_date.setEnabled(True)
            else:
                self.ui.stock_expiry_checkbox.setChecked(False)
                self.ui.stock_expiry_date.setEnabled(False)

    def filter_stock(self, text):
        result = StockAPI.filter_stock(text)
        if result["success"]:
            self.model.removeRows(0, self.model.rowCount())
            for stock in result["stocks"]:
                items = [
                    QStandardItem(str(stock["id"])),
                    QStandardItem(stock["item_name"]),
                    QStandardItem(str(stock["quantity"])),
                    QStandardItem(f"{stock['cost_price']:.2f}"),
                    QStandardItem(f"{stock['selling_price']:.2f}"),
                    QStandardItem(stock["category"]),
                    QStandardItem(stock["expiry_date"] if stock["expiry_date"] else "")
                ]
                self.model.appendRow(items)
                progress = QtWidgets.QProgressBar()
                progress.setRange(0, 100)
                progress.setValue(stock["quantity"])
                self.ui.table_stock.setIndexWidget(self.model.index(self.model.rowCount() - 1, 2), progress)
        else:
            QMessageBox.warning(self.stock_window, "Error", result["error"])

    def update_lcds(self):
        result = StockAPI.get_all_stock()
        if result["success"]:
            summary = result["summary"]
            # Wholesale LCDs
            wholesale_stocks = [s for s in result["stocks"] if s["category"] == "Wholesale"]
            self.ui.lcd1.display(len(wholesale_stocks))  # Wholesale Items
            self.ui.lcd2.display(sum(s["total_cost_value"] for s in wholesale_stocks))  # Wholesale Costs
            self.ui.lcd3.display(sum(s["total_selling_value"] for s in wholesale_stocks))  # Wholesale Value
            self.ui.lcd4.display(sum(s["total_profit_potential"] for s in wholesale_stocks))  # Wholesale Profit

            # Retail LCDs
            retail_stocks = [s for s in result["stocks"] if s["category"] == "Retail"]
            self.ui.lcd5.display(len(retail_stocks))  # Retail Items
            self.ui.lcd6.display(sum(s["total_cost_value"] for s in retail_stocks))  # Retail Costs
            self.ui.lcd7.display(sum(s["total_selling_value"] for s in retail_stocks))  # Retail Value
            self.ui.lcd8.display(sum(s["total_profit_potential"] for s in retail_stocks))  # Retail Profit

    def show(self):
        self.stock_window.show()
