import os
import random
from datetime import date
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QMessageBox, QPushButton, QInputDialog
from backend.apis import StockAPI, SaleAPI

# Import the global stock_events from stockController to listen for changes
from controllers.stockController import stock_events


class SalesController:
    def __init__(self, ui, page):
        self.ui = ui
        self.page = page

        self.items = []  # loaded stock items (active)
        self.delete_icon_path = os.path.join("assets", "icons", "delete.png")

        # validators: allow numeric typing but not arbitrary text in amount/discount
        self.setup_validators()

        # Generate invoice ID
        self.generate_invoice_id()

        # Load stock items into the left item table
        self.load_items()

        # Live connections
        self.ui.inputSearchItem.textChanged.connect(self.filter_items)
        self.ui.inputDiscount.textChanged.connect(self.update_lcds)
        self.ui.inputAmountPaid.textChanged.connect(self.update_lcds)

        # Buttons
        self.ui.btnAddToCart.clicked.connect(self.add_to_cart)
        self.ui.btnSave.clicked.connect(self.save_sale)
        self.ui.btnComplete.clicked.connect(self.complete_sale)
        self.ui.btnPrint.clicked.connect(self.print_receipt)
        self.ui.btnClear.clicked.connect(self.clear_all)

        # cart interactions
        self.ui.tableCheckoutCart.itemDoubleClicked.connect(
            self.handle_cart_item_double_click
        )

        # Update items live when stock changes
        stock_events.stock_changed.connect(self.load_items)

        self.ui.tableCheckoutCart.cellChanged.connect(self.on_cart_cell_changed)

        # --- DAILY LCDS: load today's accumulated totals from DB on startup ---
        # This will show 0 if no invoices have been saved today, or the DB totals if they exist.
        self.load_today_totals()

    # ------------------ Validators ------------------
    def setup_validators(self):
        double_validator = QDoubleValidator(0.0, 99999999.99, 2)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        self.ui.inputAmountPaid.setValidator(double_validator)
        self.ui.inputDiscount.setValidator(double_validator)

    # ------------------ Helpers ------------------
    def to_float(self, text):
        try:
            return float(text)
        except Exception:
            return 0.0

    def generate_invoice_id(self):
        invoice_id = f"INV-{random.randint(1000, 9999)}"
        self.ui.inputInvoiceID.setText(invoice_id)

    # ------------------ Load Stock Items ------------------
    def load_items(self):
        resp = StockAPI.get_all()
        if not resp.get("success"):
            QMessageBox.warning(
                self.page, "Error", resp.get("error", "Failed to load stock")
            )
            return

        self.items = [i for i in resp["items"] if i.get("is_active", True)]
        self.display_items(self.items)

        try:
            try:
                self.ui.tableItemList.cellClicked.disconnect()
            except Exception:
                pass
            self.ui.tableItemList.cellClicked.connect(self.display_item_details)
        except Exception:
            try:
                self.ui.tableItemList.itemClicked.disconnect()
            except Exception:
                pass
            self.ui.tableItemList.itemClicked.connect(
                lambda it: self.display_item_details(it.row(), 0)
            )

    def display_items(self, items):
        self.ui.tableItemList.setRowCount(0)
        for row, item in enumerate(items):
            self.ui.tableItemList.insertRow(row)
            self.ui.tableItemList.setItem(
                row, 0, QtWidgets.QTableWidgetItem(item["item_name"])
            )

    def filter_items(self, text):
        filtered = [i for i in self.items if text.lower() in i["item_name"].lower()]
        self.display_items(filtered)

    def display_item_details(self, row, column):
        if row < 0:
            return
        name_item = self.ui.tableItemList.item(row, 0)
        if not name_item:
            return
        name = name_item.text()
        item = next((i for i in self.items if i["item_name"] == name), None)
        if item:
            self.ui.inputQtyInStock.setText(str(item["quantity"]))
            self.ui.inputStockPrice.setText(str(item["selling_price"]))
            try:
                self.ui.inputCategory.setText(item["category"])
            except Exception:
                try:
                    self.ui.inputCategory.setCurrentText(item["category"])
                except Exception:
                    pass

    # ------------------ Add to Cart ------------------
    def add_to_cart(self):
        row = self.ui.tableItemList.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Error", "Select an item first")
            return

        name_item = self.ui.tableItemList.item(row, 0)
        if not name_item:
            QMessageBox.warning(self.page, "Error", "Select an item first")
            return

        name = name_item.text()
        item = next((i for i in self.items if i["item_name"] == name), None)
        if not item:
            QMessageBox.warning(self.page, "Error", "Item not found")
            return

        qty_to_add = int(self.ui.inputQtySold.value())
        if qty_to_add <= 0:
            QMessageBox.warning(self.page, "Error", "Quantity must be at least 1")
            return

        for r in range(self.ui.tableCheckoutCart.rowCount()):
            cell_item = self.ui.tableCheckoutCart.item(r, 0)
            if cell_item and cell_item.text() == name:
                existing_qty = int(self.ui.tableCheckoutCart.item(r, 2).text())
                new_qty = existing_qty + qty_to_add
                if new_qty > item["quantity"]:
                    QMessageBox.warning(
                        self.page, "Error", "Insufficient stock for requested increase"
                    )
                    return
                self.ui.tableCheckoutCart.item(r, 2).setText(str(new_qty))
                price = float(self.ui.tableCheckoutCart.item(r, 3).text())
                new_total = new_qty * price
                self.ui.tableCheckoutCart.item(r, 4).setText(f"{new_total:.2f}")
                QtCore.QTimer.singleShot(0, self.update_lcds)
                self.reset_inputs()
                return

        if qty_to_add > item["quantity"]:
            QMessageBox.warning(self.page, "Error", "Insufficient stock")
            return

        price = float(item["selling_price"])
        total = qty_to_add * price

        r = self.ui.tableCheckoutCart.rowCount()
        self.ui.tableCheckoutCart.insertRow(r)
        self.ui.tableCheckoutCart.setItem(
            r, 0, QtWidgets.QTableWidgetItem(item["item_name"])
        )
        self.ui.tableCheckoutCart.setItem(
            r, 1, QtWidgets.QTableWidgetItem(item["category"])
        )
        self.ui.tableCheckoutCart.setItem(
            r, 2, QtWidgets.QTableWidgetItem(str(qty_to_add))
        )
        self.ui.tableCheckoutCart.setItem(
            r, 3, QtWidgets.QTableWidgetItem(f"{price:.2f}")
        )
        self.ui.tableCheckoutCart.setItem(
            r, 4, QtWidgets.QTableWidgetItem(f"{total:.2f}")
        )

        btn_delete = QPushButton()
        btn_delete.setStyleSheet("border: none; background: transparent;")
        if os.path.exists(self.delete_icon_path):
            btn_delete.setIcon(QtGui.QIcon(self.delete_icon_path))
        else:
            btn_delete.setIcon(QtGui.QIcon.fromTheme("edit-delete"))
        btn_delete.setToolTip("Delete this item")
        btn_delete.clicked.connect(lambda _, b=btn_delete: self.delete_cart_row(b))

        self.ui.tableCheckoutCart.setCellWidget(r, 5, btn_delete)

        QtCore.QTimer.singleShot(0, self.update_lcds)
        self.reset_inputs()

    def delete_cart_row(self, btn):
        index = self.ui.tableCheckoutCart.indexAt(btn.pos())
        row = index.row()
        if row >= 0:
            self.ui.tableCheckoutCart.removeRow(row)
            QtCore.QTimer.singleShot(0, self.update_lcds)

    # ------------------ Cart quantity edit (double click) ------------------
    def handle_cart_item_double_click(self, item: QtWidgets.QTableWidgetItem):
        if item.column() != 2:
            return

        row = item.row()
        name = self.ui.tableCheckoutCart.item(row, 0).text()
        current_qty = int(item.text())
        stock_item = next((i for i in self.items if i["item_name"] == name), None)
        max_allowed = stock_item["quantity"] if stock_item else 999999

        new_qty, ok = QInputDialog.getInt(
            self.page,
            "Edit Quantity",
            f"Set quantity for {name}:",
            current_qty,
            1,
            max_allowed,
        )
        if not ok:
            return

        if stock_item and new_qty > stock_item["quantity"]:
            QMessageBox.warning(
                self.page, "Error", "Insufficient stock for requested quantity"
            )
            return

        item.setText(str(new_qty))
        price = float(self.ui.tableCheckoutCart.item(row, 3).text())
        new_total = new_qty * price
        self.ui.tableCheckoutCart.item(row, 4).setText(f"{new_total:.2f}")
        QtCore.QTimer.singleShot(0, self.update_lcds)

    # ------------------ LCD Updates ------------------
    def load_today_totals(self):
        """Fetch today's cumulative totals from DB and update daily LCDs."""
        resp = SaleAPI.get_today_totals()  # includes gross, profit, items_sold
        if resp.get("success"):
            gross = resp.get("gross", 0.0)
            profit = resp.get("profit", 0.0)
            items_sold = resp.get("items_sold", 0)  # now DB-based
        else:
            gross = 0.0
            profit = 0.0
            items_sold = 0

        try:
            self.ui.lcdDailySales.display(gross)
            self.ui.lcdDailyProfit.display(profit)
            self.ui.lcdItemsSold.display(items_sold)
        except Exception:
            pass

    def update_lcds(self):
        """Update cart totals (gross, discount, total, change) only."""
        gross = 0.0

        for r in range(self.ui.tableCheckoutCart.rowCount()):
            try:
                total = float(self.ui.tableCheckoutCart.item(r, 4).text())
            except Exception:
                total = 0.0
            gross += total

        discount = self.to_float(self.ui.inputDiscount.text())
        total_after_discount = max(0.0, gross - discount)
        amount_paid = self.to_float(self.ui.inputAmountPaid.text())
        change = max(0.0, amount_paid - total_after_discount)

        try:
            self.ui.lcdGross.display(gross)
            self.ui.lcdDiscount.display(discount)
            self.ui.lcdTotal.display(total_after_discount)
            self.ui.inputChange.setText(f"{change:.2f}")
        except Exception:
            pass

    # ------------------ Reset inputs ------------------
    def reset_inputs(self):
        try:
            self.ui.inputQtyInStock.clear()
            self.ui.inputStockPrice.clear()
            try:
                self.ui.inputCategory.clear()
            except Exception:
                try:
                    self.ui.inputCategory.setCurrentIndex(0)
                except Exception:
                    pass
            self.ui.inputQtySold.setValue(1)
        except Exception:
            pass

    # ------------------ Save / Complete / Print / Clear ------------------
    def save_sale(self):
        confirm = QMessageBox.question(
            self.page,
            "Confirm Save",
            "Are you sure you want to save this sale?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.create_sale(print_receipt=False)

    def complete_sale(self):
        self.create_sale(print_receipt=True)

    def print_receipt(self):
        QMessageBox.information(self.page, "Print", "Printing receipt...")

    def clear_all(self):
        self.ui.tableCheckoutCart.setRowCount(0)
        self.reset_inputs()
        self.ui.inputAmountPaid.clear()
        self.ui.inputChange.clear()
        self.ui.inputDiscount.clear()
        QtCore.QTimer.singleShot(0, self.update_lcds)
        self.generate_invoice_id()

    def create_sale(self, print_receipt=False):
        sale_items = []
        for r in range(self.ui.tableCheckoutCart.rowCount()):
            name = self.ui.tableCheckoutCart.item(r, 0).text()
            qty = int(self.ui.tableCheckoutCart.item(r, 2).text())
            stock_id = next((i["id"] for i in self.items if i["item_name"] == name), None)
            if stock_id:
                sale_items.append({"stock_id": stock_id, "quantity_sold": qty})

        amount_paid = self.to_float(self.ui.inputAmountPaid.text())
        discount = self.to_float(self.ui.inputDiscount.text())
        payment_method = self.ui.comboPaymentMethod.currentText().lower()
        sale_date = (
            self.ui.dateInvoice.date().toString("yyyy-MM-dd")
            if getattr(self.ui, "checkIncludeDate", None)
            and self.ui.checkIncludeDate.isChecked()
            else date.today().strftime("%Y-%m-%d")
        )

        resp = SaleAPI.create_sale(
            cashier_id=1,
            sale_items=sale_items,
            amount_paid=amount_paid,
            discount_amount=discount,
            payment_method=payment_method,
            sale_date=sale_date,
        )

        if not resp.get("success"):
            QMessageBox.warning(self.page, "Error", resp.get("error", "Sale failed"))
            return

        # --- REFRESH DAILY TOTALS FROM DATABASE ---
        self.load_today_totals()  # now lcdItemsSold, lcdDailySales, lcdDailyProfit are all DB-based

        stock_events.stock_changed.emit()

        msg = (
            "Sale completed & receipt printed"
            if print_receipt
            else "Sale saved successfully"
        )
        QMessageBox.information(self.page, "Success", msg)

        self.clear_all()
        self.load_items()

    def on_cart_cell_changed(self, row, column):
        if column in (2, 3):
            QtCore.QTimer.singleShot(0, self.update_lcds)
