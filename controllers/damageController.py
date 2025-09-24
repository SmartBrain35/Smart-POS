import os
from typing import Optional
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMessageBox, QPushButton
from PySide6.QtGui import QIntValidator, QIcon
from backend.apis import StockAPI  # keep your existing StockAPI import path
from backend.apis import DamageAPI  # adjust path if needed
from controllers.stockController import stock_events

DELETE_ICON_PATH = os.path.join("assets", "icons", "delete.png")


class DamageController:
    def __init__(self, ui: object, page: QtWidgets.QWidget):
        self.ui = ui
        self.page = page
        self.selected_damage_id: Optional[int] = None
        self._completer = None
        self._stock_items = []  # latest active stock items (list of dicts)

        self.setup_validators()
        self.setup_connections()
        self.load_stock_items()
        self.load_damage_table()

    # ---------------- Validators ----------------
    def setup_validators(self):
        int_validator = QIntValidator(1, 999999)
        # quantity is integer only and > 0
        self.ui.damage_quantity.setValidator(int_validator)

    # ---------------- Connections ----------------
    def setup_connections(self):
        # Buttons
        self.ui.btn_save_damage.clicked.connect(self.save_or_update_damage)
        self.ui.btn_edit_damage.clicked.connect(self.prepare_edit_selected)
        self.ui.btn_delete_damage.clicked.connect(self.delete_selected_damage)
        self.ui.btn_clear_damage.clicked.connect(self.clear_inputs)

        # Filter
        try:
            # ui uses filter_input_damage attribute name
            self.ui.filter_input_damage.textChanged.connect(self.filter_damage_table)
        except Exception:
            # fallback to older name if exists
            try:
                self.ui.filterInputDamage.textChanged.connect(self.filter_damage_table)
            except Exception:
                pass

        # Table interactions
        self.ui.table_damage.cellDoubleClicked.connect(self.table_row_double_clicked)

        # Make sure we update when stock changes elsewhere
        stock_events.stock_changed.connect(self.load_stock_items)

        # When user types item name -> auto pull price using completer selection or text change
        self.ui.damage_item_name.textChanged.connect(self.on_item_name_typed)

    # ---------------- Stock items & completer ----------------
    def load_stock_items(self):
        """Load active stock items for the item-name completer and pricing lookup."""
        resp = StockAPI.get_all()
        if not resp.get("success"):
            QMessageBox.warning(
                self.page, "Error", resp.get("error", "Failed to load stock")
            )
            return

        # keep only active items
        self._stock_items = [s for s in resp["items"] if s.get("is_active", True)]

        names = [s["item_name"] for s in self._stock_items]

        # Setup QCompleter for item name input (auto-filter drop-down as you type)
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

        damages = resp["damages"]
        self.populate_table(damages)

    def populate_table(self, damages):
        table = self.ui.table_damage
        table.setRowCount(0)

        for r, d in enumerate(damages):
            table.insertRow(r)
            # ID (hidden by user if needed)
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

            # Damage status
            status_item = QtWidgets.QTableWidgetItem(str(d["damage_status"]))
            status_item.setFlags(status_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 4, status_item)

            # Date added
            date_item = QtWidgets.QTableWidgetItem(d.get("created_at", ""))
            date_item.setFlags(date_item.flags() & ~QtCore.Qt.ItemIsEditable)
            table.setItem(r, 5, date_item)

            # Action (delete icon)
            btn = QPushButton()
            btn.setStyleSheet("border: none; background: transparent;")
            btn.setFlat(True)
            btn.setCursor(QtCore.Qt.PointingHandCursor)

            if os.path.exists(DELETE_ICON_PATH):
                btn.setIcon(QIcon(DELETE_ICON_PATH))
            else:
                btn.setText("Del")
            # bind with lambda capturing damage id and row
            btn.clicked.connect(
                lambda _, did=d["id"], row=r: self.delete_damage_dialog(did, row)
            )
            table.setCellWidget(r, 6, btn)

        # enforce stretch mode (sometimes needs re-applying after first load)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(True)

        # update LCDs after loading table
        QtCore.QTimer.singleShot(0, self.update_lcds)

    # ---------------- Filter ----------------
    def filter_damage_table(self, text: str):
        text = text.strip().lower()
        resp = DamageAPI.get_all_damages()
        if not resp.get("success"):
            return
        damages = resp["damages"]
        filtered = [d for d in damages if text in d["item_name"].lower()]
        self.populate_table(filtered)

    # ---------------- Input helpers ----------------
    def on_item_name_typed(self, text: str):
        """When user types/selects an item name, auto-pull price from stock if available."""
        name = text.strip()
        if not name:
            self.ui.damage_price.clear()
            return
        stock = self.find_stock_by_name(name)
        if stock:
            # show selling price in price input (read-only)
            self.ui.damage_price.setText(
                f"{float(stock.get('selling_price', 0.0)):.2f}"
            )
        else:
            # clear if no exact match yet
            self.ui.damage_price.clear()

    # ---------------- Save / Update ----------------
    def save_or_update_damage(self):
        """
        Saves a new damage record or updates the selected one.
        All inputs mandatory. Stock adjustments are handled in DamageAPI and only on DB success.
        """
        name = self.ui.damage_item_name.text().strip()
        qty_text = self.ui.damage_quantity.text().strip()
        price_text = self.ui.damage_price.text().strip()
        status = (
            self.ui.damage_status.currentText()
            if hasattr(self.ui.damage_status, "currentText")
            else str(self.ui.damage_status.text()).strip()
        )

        # validation: all inputs mandatory
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

        # If updating an existing damage record
        if self.selected_damage_id:
            resp = DamageAPI.update_damage(self.selected_damage_id, qty, status)
            if not resp.get("success"):
                QMessageBox.critical(
                    self.page,
                    "Update Failed",
                    resp.get("error", "Failed to update damage"),
                )
                return

            QMessageBox.information(self.page, "Success", "Damage updated successfully")
            # refresh table & stock
            self.load_damage_table()
            stock_events.stock_changed.emit()
            self.clear_inputs()
            return

        # Otherwise create a new damage record
        resp = DamageAPI.record_damage(
            stock_id=stock["id"], quantity_damaged=qty, status=status
        )
        if not resp.get("success"):
            QMessageBox.critical(
                self.page, "Save Failed", resp.get("error", "Failed to save damage")
            )
            return

        QMessageBox.information(self.page, "Success", "Damage saved successfully")
        # refresh damage table and stock list
        self.load_damage_table()
        # notify rest of app that stock changed
        stock_events.stock_changed.emit()
        self.clear_inputs()

    # ---------------- Delete helpers ----------------
    def delete_damage_dialog(self, damage_id: int, row: int):
        """Confirm deletion for a row's delete button (used from action column widgets)."""
        reply = QMessageBox.question(
            self.page,
            "Confirm Delete",
            "Delete this damage record? This will restore the damaged quantity back to stock.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        self._perform_delete(damage_id)

    def delete_selected_damage(self):
        """Delete currently selected damage record from table selection (Delete button)."""
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
        if reply != QMessageBox.Yes:
            return
        self._perform_delete(damage_id)

    def _perform_delete(self, damage_id: int):
        resp = DamageAPI.delete_damage(damage_id)
        if not resp.get("success"):
            QMessageBox.critical(
                self.page, "Delete Failed", resp.get("error", "Failed to delete damage")
            )
            return
        QMessageBox.information(self.page, "Deleted", resp.get("message", "Deleted"))
        # reload and broadcast stock update
        self.load_damage_table()
        stock_events.stock_changed.emit()

    # ---------------- Double-click to edit ----------------
    def table_row_double_clicked(self, row: int, column: int):
        """Fill inputs from table on double click (edit friendly)."""
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

        # fill inputs
        self.selected_damage_id = did
        self.ui.damage_item_name.setText(name)
        self.ui.damage_quantity.setText(qty)
        self.ui.damage_price.setText(price)
        # set status in combobox safely
        try:
            self.ui.damage_status.setCurrentText(status)
        except Exception:
            # fallback: iterate items
            idx = self.ui.damage_status.findText(status)
            if idx >= 0:
                self.ui.damage_status.setCurrentIndex(idx)

        # Make item name and price read-only during edit to prevent inconsistencies
        self.ui.damage_item_name.setReadOnly(True)
        self.ui.damage_price.setReadOnly(True)

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
        # Restore editability for new entries
        self.ui.damage_item_name.setReadOnly(False)
        self.ui.damage_price.setReadOnly(False)

    # ---------------- LCD updates ----------------
    def update_lcds(self):
        """
        Update Total Items (sum quantity), Total Price (sum price*qty),
        Total Profit (sum (selling_price - cost_price) * qty) — using stock cost.
        """
        total_items = 0
        total_price = 0.0
        total_profit = 0.0

        # read rows from table (current view)
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

            # compute profit (price - cost) * qty using current stock cost lookup
            stock = self.find_stock_by_name(name)
            cost = float(stock.get("cost_price", 0.0)) if stock else 0.0
            total_profit += (price - cost) * qty

        # update LCDs
        try:
            self.ui.lcdTotalItems.display(total_items)
            self.ui.lcdTotalPrice.display(total_price)
            self.ui.lcdTotalProfit.display(total_profit)
        except Exception:
            # silently ignore UI failures (should not happen in normal usage)
            pass

    # ---------------- Utility: prepare edit ----------------
    def prepare_edit_selected(self):
        """Helper to prepare editing selected damage record (fills inputs)."""
        row = self.ui.table_damage.currentRow()
        if row < 0:
            QMessageBox.information(self.page, "Info", "Select a damage row to edit.")
            return
        self.table_row_double_clicked(row, 0)
