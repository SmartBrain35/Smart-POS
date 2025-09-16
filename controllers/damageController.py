from PySide6 import QtCore, QtGui, QtWidgets, QMessageBox, QMainWindow
from ui.damage_ui import Ui_Damage
from backend.apis import DamageAPI, StockAPI
from datetime import datetime


class DamageController:
    def __init__(self, parent=None):
        self.parent = parent
        self.damage_window = QMainWindow()
        self.ui = Ui_Damage()
        self.ui.setupUi(self.damage_window)

        # Connect UI signals to controller methods
        self.ui.btn_save_damage.clicked.connect(self.handle_save_damage)
        self.ui.btn_edit_damage.clicked.connect(self.handle_edit_damage)
        self.ui.btn_delete_damage.clicked.connect(self.handle_delete_damage)
        self.ui.btn_clear_damage.clicked.connect(self.handle_clear)
        self.ui.filter_input_damage.textChanged.connect(self.filter_damages)

        # Load initial data and update LCDs
        self.load_damages()
        self.update_lcds()

    def load_damages(self):
        # Clear existing rows
        self.ui.table_damage.setRowCount(0)

        # Fetch damages from API
        result = DamageAPI.get_damage_summary()
        if result["success"]:
            self.ui.table_damage.setRowCount(len(result["damages"]))
            for row, damage in enumerate(result["damages"]):
                self.ui.table_damage.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(damage["id"]))
                )
                self.ui.table_damage.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(damage["item_name"])
                )
                self.ui.table_damage.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(damage["quantity_damaged"]))
                )
                self.ui.table_damage.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(f"{damage['unit_price']:.2f}")
                )
                self.ui.table_damage.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(damage["damage_status"])
                )
                self.ui.table_damage.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(damage["damage_date"])
                )

                # Action column with delete button
                delete_btn = QtWidgets.QPushButton()
                delete_btn.setObjectName("DamageTableBtnDelete")
                delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                delete_btn.setToolTip("Delete")
                delete_btn.setFixedSize(30, 30)
                delete_btn.clicked.connect(
                    lambda checked, r=row: self.handle_table_delete(r)
                )
                self.ui.table_damage.setCellWidget(row, 6, delete_btn)
        else:
            QMessageBox.warning(self.damage_window, "Error", result["error"])

    def handle_save_damage(self):
        item_name = self.ui.damage_item_name.text().strip()
        quantity = self.ui.damage_quantity.text().strip()
        price = self.ui.damage_price.text().strip()
        status = self.ui.damage_status.currentText()

        # Validate all fields are mandatory
        if not all([item_name, quantity, price, status]):
            QMessageBox.warning(
                self.damage_window, "Input Error", "All fields are mandatory."
            )
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self.damage_window,
                "Input Error",
                "Quantity must be a positive integer and Price must be a positive number.",
            )
            return

        # Find stock ID by item name
        stock_result = StockAPI.filter_stock(item_name)
        if not stock_result["success"] or not stock_result["stocks"]:
            QMessageBox.warning(self.damage_window, "Error", "Item not found in stock.")
            return
        stock_id = stock_result["stocks"][0]["id"]

        # Record damage and update stock
        result = DamageAPI.record_damage(stock_id, quantity)
        if result["success"]:
            QMessageBox.information(self.damage_window, "Success", result["message"])
            self.handle_clear()
            self.load_damages()
            self.update_lcds()
            # Update stock summary (not directly handled here, assumed API handles it)
        else:
            QMessageBox.warning(self.damage_window, "Error", result["error"])

    def handle_edit_damage(self):
        selected_row = self.ui.table_damage.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self.damage_window,
                "Selection Error",
                "Please select a damage record to edit.",
            )
            return

        damage_id = int(self.ui.table_damage.item(selected_row, 0).text())
        item_name = self.ui.damage_item_name.text().strip()
        quantity = self.ui.damage_quantity.text().strip()
        price = self.ui.damage_price.text().strip()
        status = self.ui.damage_status.currentText()

        if not all([item_name, quantity, price, status]):
            QMessageBox.warning(
                self.damage_window, "Input Error", "All fields are mandatory."
            )
            return

        try:
            quantity = int(quantity)
            price = float(price)
            if quantity <= 0 or price < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self.damage_window,
                "Input Error",
                "Quantity must be a positive integer and Price must be a positive number.",
            )
            return

        # Note: Editing damage is not directly supported by API; this would require reverting previous damage and re-recording
        QMessageBox.warning(
            self.damage_window,
            "Not Implemented",
            "Editing damage is not currently supported. Please delete and re-add if needed.",
        )
        # For full implementation, you'd need to adjust API to support damage updates

    def handle_delete_damage(self):
        selected_row = self.ui.table_damage.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self.damage_window,
                "Selection Error",
                "Please select a damage record to delete.",
            )
            return

        damage_id = int(self.ui.table_damage.item(selected_row, 0).text())
        reply = QMessageBox.question(
            self.damage_window,
            "Confirm Delete",
            "Are you sure you want to delete this damage record?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # Note: Current API does not support deleting damage; this is a placeholder
            QMessageBox.warning(
                self.damage_window,
                "Not Implemented",
                "Deleting damage is not currently supported.",
            )
            # For full implementation, add delete_damage method to DamageAPI and revert stock updates

    def handle_clear(self):
        self.ui.damage_item_name.clear()
        self.ui.damage_quantity.clear()
        self.ui.damage_price.clear()
        self.ui.damage_status.setCurrentIndex(0)

    def filter_damages(self, search_term):
        result = DamageAPI.filter_damages(search_term)
        if result["success"]:
            self.ui.table_damage.setRowCount(0)
            for row, damage in enumerate(result["damages"]):
                self.ui.table_damage.setRowCount(self.ui.table_damage.rowCount() + 1)
                self.ui.table_damage.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(damage["id"]))
                )
                self.ui.table_damage.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(damage["item_name"])
                )
                self.ui.table_damage.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(damage["quantity_damaged"]))
                )
                self.ui.table_damage.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(f"{damage['unit_price']:.2f}")
                )
                self.ui.table_damage.setItem(
                    row, 4, QtWidgets.QTableWidgetItem("N/A")
                )  # Damage status not in filter result
                self.ui.table_damage.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(damage["damage_date"])
                )

                delete_btn = QtWidgets.QPushButton()
                delete_btn.setObjectName("DamageTableBtnDelete")
                delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                delete_btn.setToolTip("Delete")
                delete_btn.setFixedSize(30, 30)
                delete_btn.clicked.connect(
                    lambda checked, r=row: self.handle_table_delete(r)
                )
                self.ui.table_damage.setCellWidget(row, 6, delete_btn)
        else:
            QMessageBox.warning(self.damage_window, "Error", result["error"])

    def handle_table_delete(self, row):
        damage_id = int(self.ui.table_damage.item(row, 0).text())
        reply = QMessageBox.question(
            self.damage_window,
            "Confirm Delete",
            "Are you sure you want to delete this damage record?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # Note: Current API does not support deleting damage; this is a placeholder
            QMessageBox.warning(
                self.damage_window,
                "Not Implemented",
                "Deleting damage is not currently supported.",
            )
            # For full implementation, add delete_damage method to DamageAPI and revert stock updates

    def update_lcds(self):
        result = DamageAPI.get_damage_summary()
        if result["success"]:
            summary = result["summary"]
            self.ui.lcdTotalItems.display(summary["total_items"])
            self.ui.lcdTotalPrice.display(summary["total_price"])
            self.ui.lcdTotalProfit.display(summary["total_profit_loss"])

    def show(self):
        self.damage_window.show()
