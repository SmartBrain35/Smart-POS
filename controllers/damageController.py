import os
from datetime import datetime
from PySide6 import QtWidgets, QtGui, QtCore
from backend.apis import DamageAPI, StockAPI


class DamageController:
    def __init__(self, ui, page):
        self.ui = ui
        self.page = page  # QWidget parent for QMessageBox dialogs
        self.current_item_id = None

        self.delete_icon_path = "assets/icons/delete.png"
        self.damages = []
        self.stocks = []

        # Load initial data
        self.load_stocks()
        self.load_damages()
        self.setup_item_autocomplete()

        # Connect signals
        self.ui.btn_save_damage.clicked.connect(self.save_damage)
        self.ui.btn_clear_damage.clicked.connect(self.clear_inputs)
        self.ui.filter_input_damage.textChanged.connect(self.filter_damages)
        self.ui.damage_item_name.textChanged.connect(self.auto_fill_price)
        self.ui.table_damage.cellDoubleClicked.connect(self.fill_inputs_for_edit)

        print("DamageController instantiated")

    # ------------------ Load Stocks & Damages -------------------
    def load_stocks(self):
        resp = StockAPI.get_all()
        self.stocks = resp["items"] if resp.get("success") else []

    def load_damages(self):
        resp = DamageAPI.get_all_damages()
        self.damages = resp["damages"] if resp.get("success") else []
        self.populate_damage_table(self.damages)

    # ------------------ Auto-Suggestions -------------------
    def setup_item_autocomplete(self):
        item_names = [stock["item_name"] for stock in self.stocks]
        completer = QtWidgets.QCompleter(item_names)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        self.ui.damage_item_name.setCompleter(completer)

    # ------------------ Auto-fill Price -------------------
    def auto_fill_price(self):
        item_name = self.ui.damage_item_name.text().strip()
        if not item_name:
            self.ui.damage_price.clear()
            return

        stock = next(
            (s for s in self.stocks if s["item_name"].lower() == item_name.lower()),
            None,
        )
        if stock:
            self.ui.damage_price.setText(str(stock["selling_price"]))
        else:
            self.ui.damage_price.clear()

    # ------------------ Populate Table -------------------
    def populate_damage_table(self, data):
        self.ui.table_damage.setRowCount(0)
        for row_idx, d in enumerate(data):
            self._insert_damage_row(row_idx, d)
        self.update_lcds()

    def _insert_damage_row(self, row_idx, damage):
        self.ui.table_damage.insertRow(row_idx)
        self.ui.table_damage.setItem(
            row_idx, 0, QtWidgets.QTableWidgetItem(str(damage["id"]))
        )
        self.ui.table_damage.setItem(
            row_idx, 1, QtWidgets.QTableWidgetItem(damage["item_name"])
        )
        self.ui.table_damage.setItem(
            row_idx, 2, QtWidgets.QTableWidgetItem(str(damage["quantity_damaged"]))
        )
        self.ui.table_damage.setItem(
            row_idx, 3, QtWidgets.QTableWidgetItem(f'{damage["price"]:.2f}')
        )
        self.ui.table_damage.setItem(
            row_idx, 4, QtWidgets.QTableWidgetItem(damage["damage_status"])
        )
        self.ui.table_damage.setItem(
            row_idx, 5, QtWidgets.QTableWidgetItem(damage["created_at"])
        )

        btn_delete = QtWidgets.QPushButton()
        btn_delete.setObjectName("btnDeleteDamageRow")
        btn_delete.setStyleSheet(
            """
                        QPushButton {
                            border: none;
                            background: transparent;
                            padding: 3px;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 0, 0, 40);
                            border-radius: 6px;
                        }
                        QPushButton:pressed {
                            background-color: rgba(255, 0, 0, 80);
                            border-radius: 6px;
                        }
                    """
        )
        btn_delete.setIcon(
            QtGui.QIcon(
                self.delete_icon_path if os.path.exists(self.delete_icon_path) else ""
            )
        )
        btn_delete.setToolTip("Delete this damage record")
        btn_delete.clicked.connect(
            lambda _, did=damage["id"], name=damage["item_name"], qty=damage[
                "quantity_damaged"
            ]: self.delete_damage(did, name, qty)
        )
        self.ui.table_damage.setCellWidget(row_idx, 6, btn_delete)

    # ------------------ Update LCD Totals -------------------
    def update_lcds(self):
        total_items = total_price = total_profit = 0
        for row in range(self.ui.table_damage.rowCount()):
            try:
                qty = int(self.ui.table_damage.item(row, 2).text())
                price = float(self.ui.table_damage.item(row, 3).text())
                profit = price * qty * 0.2
            except (ValueError, AttributeError):
                continue
            total_items += qty
            total_price += price * qty
            total_profit += profit

        self.ui.lcdTotalItems.display(total_items)
        self.ui.lcdTotalPrice.display(total_price)
        self.ui.lcdTotalProfit.display(total_profit)

    # ------------------ Save Damage -------------------
    def save_damage(self):
        item_name = self.ui.damage_item_name.text().strip()
        qty_text = self.ui.damage_quantity.text().strip()
        status = self.ui.damage_status.currentText()

        if not item_name or not qty_text:
            QtWidgets.QMessageBox.warning(self.page, "Error", "All fields are required")
            return

        try:
            quantity = int(qty_text)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self.page, "Error", "Quantity must be a number"
            )
            return

        stock = next(
            (s for s in self.stocks if s["item_name"].lower() == item_name.lower()),
            None,
        )
        if not stock:
            QtWidgets.QMessageBox.warning(self.page, "Error", "Stock item not found")
            return

        if quantity > stock["quantity"]:
            QtWidgets.QMessageBox.warning(
                self.page, "Error", "Not enough stock available"
            )
            return

        resp = DamageAPI.record_damage(
            stock_id=stock["id"], quantity_damaged=quantity, status=status
        )
        if resp.get("success"):
            new_damage = resp["damage"]
            self.damages.append(new_damage)
            self._insert_damage_row(self.ui.table_damage.rowCount(), new_damage)
            self.update_lcds()
            self.update_stock_row(stock["id"], -quantity)
            QtWidgets.QMessageBox.information(
                self.page, "Success", "Damage recorded successfully"
            )
            self.clear_inputs()
        else:
            QtWidgets.QMessageBox.warning(
                self.page, "Error", resp.get("error", "Failed to record damage")
            )

    # ------------------ Delete Damage -------------------
    def delete_damage(self, damage_id, item_name, qty):
        confirm = QtWidgets.QMessageBox.question(
            self.page,
            "Confirm Delete",
            "Are you sure you want to delete this record?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            self.damages = [d for d in self.damages if d["id"] != damage_id]
            for row in range(self.ui.table_damage.rowCount()):
                if self.ui.table_damage.item(row, 0).text() == str(damage_id):
                    self.ui.table_damage.removeRow(row)
                    break
            self.update_lcds()
            self.update_stock_row_by_name(item_name, qty)

    # ------------------ Stock Update -------------------
    def update_stock_row(self, stock_id, change_qty):
        if not hasattr(self, "stock_controller"):
            return
        table = self.stock_controller.ui.table_stock
        for row in range(table.rowCount()):
            cell = table.item(row, 0)
            if cell and cell.text() == str(stock_id):
                qty_item = table.item(row, 2)
                if qty_item:
                    new_qty = max(0, int(qty_item.text()) + change_qty)
                    qty_item.setText(str(new_qty))
                    if new_qty == 0:
                        qty_item.setBackground(QtGui.QColor("red"))
                break

    def update_stock_row_by_name(self, item_name, qty_change):
        if not hasattr(self, "stock_controller"):
            return
        table = self.stock_controller.ui.table_stock
        for row in range(table.rowCount()):
            name_cell = table.item(row, 1)
            if name_cell and name_cell.text().lower() == item_name.lower():
                qty_item = table.item(row, 2)
                if qty_item:
                    new_qty = int(qty_item.text()) + qty_change
                    qty_item.setText(str(new_qty))
                    qty_item.setBackground(QtGui.QColor("white"))
                break

    # ------------------ Filter Damages -------------------
    def filter_damages(self, text):
        text = text.lower()
        filtered = [d for d in self.damages if text in d["item_name"].lower()]
        self.ui.table_damage.setRowCount(0)
        for idx, d in enumerate(filtered):
            self._insert_damage_row(idx, d)
        self.update_lcds()

    # ------------------ Double Click to Edit -------------------
    def fill_inputs_for_edit(self, row, column):
        self.current_item_id = int(self.ui.table_damage.item(row, 0).text())
        self.ui.damage_item_name.setText(self.ui.table_damage.item(row, 1).text())
        self.ui.damage_quantity.setText(self.ui.table_damage.item(row, 2).text())
        self.ui.damage_price.setText(self.ui.table_damage.item(row, 3).text())
        status = self.ui.table_damage.item(row, 4).text()
        idx = self.ui.damage_status.findText(status)
        if idx != -1:
            self.ui.damage_status.setCurrentIndex(idx)

    # ------------------ Clear Inputs -------------------
    def clear_inputs(self):
        self.ui.damage_item_name.clear()
        self.ui.damage_quantity.clear()
        self.ui.damage_price.clear()
        self.ui.damage_status.setCurrentIndex(0)
        self.setup_item_autocomplete()
