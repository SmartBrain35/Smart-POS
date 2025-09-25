import os
from typing import Optional
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QMessageBox, QPushButton
from PySide6.QtGui import QIntValidator, QIcon
from backend.apis import StockAPI, DamageAPI
from controllers.stockController import stock_events

DELETE_ICON_PATH = os.path.join("assets", "icons", "delete.png")


class DamageController:
    def __init__(self, ui: object, page: QtWidgets.QWidget):
        self.ui = ui
        self.page = page
        self.selected_damage_id: Optional[int] = None
        self._completer = None
        self._stock_items = []  # latest active stock items

        self.setup_validators()
        self.setup_connections()
        self.load_stock_items()
        self.load_damage_table()

        # set default UI state
        self.ui.btn_edit_damage.setEnabled(False)  # disable Edit until row selected
        self.ui.btn_save_damage.setEnabled(True)  # Add enabled by default

    # ---------------- Validators ----------------
    def setup_validators(self):
        int_validator = QIntValidator(1, 999999)
        self.ui.damage_quantity.setValidator(int_validator)

    # ---------------- Connections ----------------
    def setup_connections(self):
        # Buttons
        self.ui.btn_save_damage.clicked.connect(self.save_damage)  # always new
        self.ui.btn_edit_damage.clicked.connect(self.update_damage)  # always update
        self.ui.btn_delete_damage.clicked.connect(self.delete_selected_damage)
        self.ui.btn_clear_damage.clicked.connect(self.clear_inputs)

        # Filter
        try:
            self.ui.filter_input_damage.textChanged.connect(self.filter_damage_table)
        except Exception:
            try:
                self.ui.filterInputDamage.textChanged.connect(self.filter_damage_table)
            except Exception:
                pass

        # Table interactions
        self.ui.table_damage.cellDoubleClicked.connect(self.table_row_double_clicked)

        # Stock changes
        stock_events.stock_changed.connect(self.load_stock_items)

        # Auto price on item name typing
        self.ui.damage_item_name.textChanged.connect(self.on_item_name_typed)

    # ---------------- Stock items ----------------
    def load_stock_items(self):
        resp = StockAPI.get_all()
        if not resp.get("success"):
            QMessageBox.warning(
                self.page, "Error", resp.get("error", "Failed to load stock")
            )
            return

        self._stock_items = [s for s in resp["items"] if s.get("is_active", True)]
        names = [s["item_name"] for s in self._stock_items]

        self._completer = QtWidgets.QCompleter(names, self.ui.damage_item_name)
        self._completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._completer.setFilterMode(QtCore.Qt.MatchContains)
        self.ui.damage_item_name.setCompleter(self._completer)

    def find_stock_by_name(self, name: str):
        return next(
            (s for s in self._stock_items if s["item_name"].lower() == name.lower()),
            None,
        )

    # ---------------- Damage table ----------------
    def load_damage_table(self):
        resp = DamageAPI.get_all_damages()
        if not resp.get("success"):
            QMessageBox.warning(
                self.page, "Error", resp.get("error", "Failed to load damages")
            )
            return
        self.populate_table(resp["damages"])

    def populate_table(self, damages):
        table = self.ui.table_damage
        table.setRowCount(0)

        for r, d in enumerate(damages):
            table.insertRow(r)

            # ID
            id_item = QtWidgets.QTableWidgetItem(str(d["id"]))
            id_item.setFlags(id_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 0, id_item)

            # Item name
            name_item = QtWidgets.QTableWidgetItem(d["item_name"])
            name_item.setFlags(name_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 1, name_item)

            # Quantity
            qty_item = QtWidgets.QTableWidgetItem(str(d["quantity_damaged"]))
            qty_item.setFlags(qty_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 2, qty_item)

            # Price
            price_item = QtWidgets.QTableWidgetItem(f"{float(d['price']):.2f}")
            price_item.setFlags(price_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 3, price_item)

            # Status
            status_item = QtWidgets.QTableWidgetItem(str(d["damage_status"]))
            status_item.setFlags(status_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 4, status_item)

            # Date
            date_item = QtWidgets.QTableWidgetItem(d.get("created_at", ""))
            date_item.setFlags(date_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 5, date_item)

            # Delete button
            btn = QPushButton()
            btn.setStyleSheet("border: none; background: transparent;")
            btn.setFlat(True)
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            (
                btn.setIcon(QIcon(DELETE_ICON_PATH))
                if os.path.exists(DELETE_ICON_PATH)
                else btn.setText("Del")
            )
            btn.clicked.connect(
                lambda _, did=d["id"], row=r: self.delete_damage_dialog(did, row)
            )
            table.setCellWidget(r, 6, btn)

        # resize
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(True)

        # update LCDs
        QtCore.QTimer.singleShot(0, self.update_lcds)

    # ---------------- Filter ----------------
    def filter_damage_table(self, text: str):
        text = text.strip().lower()
        resp = DamageAPI.get_all_damages()
        if not resp.get("success"):
            return
        filtered = [d for d in resp["damages"] if text in d["item_name"].lower()]
        self.populate_table(filtered)

    # ---------------- Input helpers ----------------
    def on_item_name_typed(self, text: str):
        name = text.strip()
        if not name:
            self.ui.damage_price.clear()
            return
        stock = self.find_stock_by_name(name)
        if stock:
            self.ui.damage_price.setText(
                f"{float(stock.get('selling_price', 0.0)):.2f}"
            )
        else:
            self.ui.damage_price.clear()

    # ---------------- Save (Add) ----------------
    def save_damage(self):
        """Always save a new damage record."""
        self._save_or_update(is_update=False)

    # ---------------- Update (Edit) ----------------
    def update_damage(self):
        """Always update selected record."""
        if not self.selected_damage_id:
            QMessageBox.information(
                self.page, "Info", "No damage record selected for update."
            )
            return
        self._save_or_update(is_update=True)

    # ---------------- Shared Save/Update ----------------
    def _save_or_update(self, is_update: bool):
        name = self.ui.damage_item_name.text().strip()
        qty_text = self.ui.damage_quantity.text().strip()
        price_text = self.ui.damage_price.text().strip()
        status = (
            self.ui.damage_status.currentText()
            if hasattr(self.ui.damage_status, "currentText")
            else str(self.ui.damage_status.text()).strip()
        )

        # validation
        if not name or not qty_text or not price_text or not status:
            QMessageBox.critical(
                self.page, "Validation Error", "All fields are required."
            )
            return

        try:
            qty = int(qty_text)
        except Exception:
            QMessageBox.critical(
                self.page, "Validation Error", "Quantity must be an integer."
            )
            return

        stock = self.find_stock_by_name(name)
        if not stock:
            QMessageBox.critical(
                self.page, "Error", "Selected item not found in stock."
            )
            return

        if is_update:
            resp = DamageAPI.update_damage(self.selected_damage_id, qty, status)
            if not resp.get("success"):
                QMessageBox.critical(
                    self.page,
                    "Update Failed",
                    resp.get("error", "Failed to update damage"),
                )
                return
            QMessageBox.information(self.page, "Success", "Damage updated successfully")
        else:
            resp = DamageAPI.record_damage(
                stock_id=stock["id"], quantity_damaged=qty, status=status
            )
            if not resp.get("success"):
                QMessageBox.critical(
                    self.page, "Save Failed", resp.get("error", "Failed to save damage")
                )
                return
            QMessageBox.information(self.page, "Success", "Damage saved successfully")

        # refresh UI and auto-clear back to Add mode
        self.load_damage_table()
        stock_events.stock_changed.emit()
        self.clear_inputs()

    # ---------------- Delete ----------------
    def delete_damage_dialog(self, damage_id: int, row: int):
        reply = QMessageBox.question(
            self.page,
            "Confirm Delete",
            "Delete this damage record? This will restore the damaged quantity back to stock.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._perform_delete(damage_id)

    def delete_selected_damage(self):
        sel = self.ui.table_damage.currentRow()
        if sel < 0:
            QMessageBox.information(
                self.page, "Info", "Select a damage record to delete."
            )
            return
        item = self.ui.table_damage.item(sel, 0)
        if not item:
            QMessageBox.information(
                self.page, "Error", "Unable to get selected damage id."
            )
            return
        try:
            damage_id = int(item.text())
        except Exception:
            QMessageBox.information(self.page, "Error", "Invalid damage id.")
            return

        reply = QMessageBox.question(
            self.page,
            "Confirm Delete",
            "Delete selected damage record? This will restore quantity to stock.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self._perform_delete(damage_id)

    def _perform_delete(self, damage_id: int):
        resp = DamageAPI.delete_damage(damage_id)
        if not resp.get("success"):
            QMessageBox.critical(
                self.page, "Delete Failed", resp.get("error", "Failed to delete damage")
            )
            return
        QMessageBox.information(self.page, "Deleted", resp.get("message", "Deleted"))
        self.load_damage_table()
        stock_events.stock_changed.emit()

    # ---------------- Double-click to edit ----------------
    def table_row_double_clicked(self, row: int, column: int):
        try:
            item_id_item = self.ui.table_damage.item(row, 0)
            if not item_id_item:
                return
            did = int(item_id_item.text())
            name = self.ui.table_damage.item(row, 1).text()
            qty = self.ui.table_damage.item(row, 2).text()
            price = self.ui.table_damage.item(row, 3).text()
            status = self.ui.table_damage.item(row, 4).text()
        except Exception:
            return

        self.selected_damage_id = did
        self.ui.damage_item_name.setText(name)
        self.ui.damage_quantity.setText(qty)
        self.ui.damage_price.setText(price)

        try:
            self.ui.damage_status.setCurrentText(status)
        except Exception:
            idx = self.ui.damage_status.findText(status)
            if idx >= 0:
                self.ui.damage_status.setCurrentIndex(idx)

        self.ui.damage_item_name.setReadOnly(True)
        self.ui.damage_price.setReadOnly(True)

        # switch to edit mode
        self.ui.btn_save_damage.setEnabled(False)
        self.ui.btn_edit_damage.setEnabled(True)

    # ---------------- Clear inputs ----------------
    def clear_inputs(self):
        self.selected_damage_id = None
        self.ui.damage_item_name.clear()
        self.ui.damage_quantity.clear()
        self.ui.damage_price.clear()
        try:
            self.ui.damage_status.setCurrentIndex(0)
        except Exception:
            pass

        self.ui.damage_item_name.setReadOnly(False)
        self.ui.damage_price.setReadOnly(False)

        # back to add mode
        self.ui.btn_save_damage.setEnabled(True)
        self.ui.btn_edit_damage.setEnabled(False)

    # ---------------- LCD updates ----------------
    def update_lcds(self):
        total_items = 0
        total_price = 0.0
        total_profit = 0.0

        tbl = self.ui.table_damage
        for r in range(tbl.rowCount()):
            try:
                name = tbl.item(r, 1).text()
                qty = int(tbl.item(r, 2).text())
                price = float(tbl.item(r, 3).text())
            except Exception:
                continue
            total_items += qty
            total_price += price * qty

            stock = self.find_stock_by_name(name)
            cost = float(stock.get("cost_price", 0.0)) if stock else 0.0
            total_profit += (price - cost) * qty

        try:
            self.ui.lcdTotalItems.display(total_items)
            self.ui.lcdTotalPrice.display(total_price)
            self.ui.lcdTotalProfit.display(total_profit)
        except Exception:
            pass
