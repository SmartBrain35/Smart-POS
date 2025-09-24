from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QMessageBox, QPushButton
from backend.apis import StockAPI, SaleAPI
from datetime import date
import os
import random


class SalesController:
    def __init__(self, ui, page):
        self.ui = ui
        self.page = page
        self.items = []
        self.delete_icon_path = os.path.join("assets", "icons", "delete.png")

        # Allow only numbers in amount & discount fields
        validator = QDoubleValidator(0.0, 9999999.99, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.ui.inputAmountPaid.setValidator(validator)
        self.ui.inputDiscount.setValidator(validator)

        # Generate invoice ID
        self.generate_invoice_id()

        # Load stock items
        self.load_items()

        # Live LCD updates
        self.ui.inputSearchItem.textChanged.connect(self.filter_items)
        self.ui.inputDiscount.textChanged.connect(self.update_lcds)
        self.ui.inputAmountPaid.textChanged.connect(self.update_lcds)

        # Button events
        self.ui.btnAddToCart.clicked.connect(self.add_to_cart)
        self.ui.btnSave.clicked.connect(self.save_sale)
        self.ui.btnComplete.clicked.connect(self.complete_sale)
        self.ui.btnPrint.clicked.connect(self.print_receipt)
        self.ui.btnClear.clicked.connect(self.clear_all)

    # ---------- Helpers ----------
    def to_float(self, text):
        try:
            return float(text)
        except ValueError:
            return 0.0

    def generate_invoice_id(self):
        invoice_id = f"INV-{random.randint(1000, 9999)}"
        self.ui.inputInvoiceID.setText(invoice_id)

    # ---------- Load Stock ----------
    def load_items(self):
        resp = StockAPI.get_all()
        if not resp.get("success"):
            QMessageBox.warning(
                self.page, "Error", resp.get("error", "Failed to load stock")
            )
            return

        self.items = resp["items"]
        self.display_items(self.items)
        self.ui.tableItemList.cellClicked.connect(self.display_item_details)

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
        name = self.ui.tableItemList.item(row, 0).text()
        item = next((i for i in self.items if i["item_name"] == name), None)
        if item:
            self.ui.inputQtyInStock.setText(str(item["quantity"]))
            self.ui.inputStockPrice.setText(str(item["selling_price"]))
            self.ui.inputCategory.setText(item["category"])

    # ---------- Add to Cart ----------
    def add_to_cart(self):
        row = self.ui.tableItemList.currentRow()
        if row < 0:
            QMessageBox.warning(self.page, "Error", "Select an item first")
            return

        name = self.ui.tableItemList.item(row, 0).text()
        item = next((i for i in self.items if i["item_name"] == name), None)
        if not item:
            QMessageBox.warning(self.page, "Error", "Item not found")
            return

        # Prevent duplicates
        for r in range(self.ui.tableCheckoutCart.rowCount()):
            if self.ui.tableCheckoutCart.item(r, 0).text() == name:
                QMessageBox.warning(
                    self.page, "Error", "This item is already in the cart"
                )
                return

        qty = self.ui.inputQtySold.value()
        if qty > item["quantity"]:
            QMessageBox.warning(self.page, "Error", "Insufficient stock")
            return

        price = float(item["selling_price"])
        total = qty * price

        r = self.ui.tableCheckoutCart.rowCount()
        self.ui.tableCheckoutCart.insertRow(r)
        self.ui.tableCheckoutCart.setItem(
            r, 0, QtWidgets.QTableWidgetItem(item["item_name"])
        )
        self.ui.tableCheckoutCart.setItem(
            r, 1, QtWidgets.QTableWidgetItem(item["category"])
        )
        self.ui.tableCheckoutCart.setItem(r, 2, QtWidgets.QTableWidgetItem(str(qty)))
        self.ui.tableCheckoutCart.setItem(
            r, 3, QtWidgets.QTableWidgetItem(f"{price:.2f}")
        )
        self.ui.tableCheckoutCart.setItem(
            r, 4, QtWidgets.QTableWidgetItem(f"{total:.2f}")
        )

        # Delete button only, no stock ID
        btn_delete = QPushButton()
        btn_delete.setObjectName("btnDeleteRow")

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

        if os.path.exists(self.delete_icon_path):
            btn_delete.setIcon(QtGui.QIcon(self.delete_icon_path))
        else:
            btn_delete.setIcon(QtGui.QIcon.fromTheme("edit-delete"))
        btn_delete.setToolTip("Delete this item")
        btn_delete.clicked.connect(lambda _, row=r: self.delete_cart_row(row))
        self.ui.tableCheckoutCart.setCellWidget(r, 5, btn_delete)

        self.update_lcds()
        self.reset_inputs()

    def delete_cart_row(self, row):
        self.ui.tableCheckoutCart.removeRow(row)
        self.update_lcds()

    # ---------- LCD Updates ----------
    def update_lcds(self):
        gross, items_sold = 0, 0
        for r in range(self.ui.tableCheckoutCart.rowCount()):
            qty = int(self.ui.tableCheckoutCart.item(r, 2).text())
            total = float(self.ui.tableCheckoutCart.item(r, 4).text())
            gross += total
            items_sold += qty

        discount = self.to_float(self.ui.inputDiscount.text())
        total = gross - discount
        amount_paid = self.to_float(self.ui.inputAmountPaid.text())
        change = amount_paid - total if amount_paid >= total else 0

        self.ui.lcdGross.display(gross)
        self.ui.lcdDiscount.display(discount)
        self.ui.lcdTotal.display(total)
        self.ui.lcdItemsSold.display(items_sold)
        self.ui.lcdDailySales.display(gross)
        self.ui.lcdDailyProfit.display(gross * 0.3)
        self.ui.inputChange.setText(f"{change:.2f}")

    def reset_inputs(self):
        self.ui.inputQtyInStock.clear()
        self.ui.inputStockPrice.clear()
        self.ui.inputCategory.clear()
        self.ui.inputQtySold.setValue(1)

    # ---------- Save / Complete / Print / Clear ----------
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
        self.update_lcds()
        self.generate_invoice_id()

    def create_sale(self, print_receipt=False):
        sale_items = []
        for r in range(self.ui.tableCheckoutCart.rowCount()):
            name = self.ui.tableCheckoutCart.item(r, 0).text()
            qty = int(self.ui.tableCheckoutCart.item(r, 2).text())
            stock_id = next(
                (i["id"] for i in self.items if i["item_name"] == name), None
            )
            if stock_id:
                sale_items.append({"stock_id": stock_id, "quantity_sold": qty})

        amount_paid = self.to_float(self.ui.inputAmountPaid.text())
        discount = self.to_float(self.ui.inputDiscount.text())
        payment_method = self.ui.comboPaymentMethod.currentText().lower()
        sale_date = (
            self.ui.dateInvoice.date().toString("yyyy-MM-dd")
            if self.ui.checkIncludeDate.isChecked()
            else date.today().strftime("%Y-%m-%d")
        )

        # Call Sale API
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

        # 🔹 Deduct sold quantities in-memory
        for s in sale_items:
            stock_item = next((i for i in self.items if i["id"] == s["stock_id"]), None)
            if stock_item:
                stock_item["quantity"] -= s["quantity_sold"]

        # 🔹 Refresh stock page after sale
        self.load_items()

        # Update LCDs, show message
        self.update_lcds()
        msg = (
            "Sale completed & receipt printed"
            if print_receipt
            else "Sale saved successfully"
        )
        QMessageBox.information(self.page, "Success", msg)

        # Clear cart & regenerate invoice
        self.clear_all()
