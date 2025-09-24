import logging
from PySide6 import QtCore
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from backend.apis import StockAPI  # use the real backend
from datetime import date as DateType
from PySide6.QtWidgets import QMessageBox


logger = logging.getLogger("StockController")


# ------------------ Stock Table Model ------------------
class StockTableModel(QAbstractTableModel):
    def __init__(self, items: list[dict], parent=None):
        super().__init__(parent)
        self._items = items
        self._headers = ["ID", "Name", "Qty", "Cost", "Sell", "Category", "Expiry"]

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self._items[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return item["id"]
            if col == 1:
                return item["item_name"]
            if col == 2:
                return item["quantity"]
            if col == 3:
                return f"{item['cost_price']:.2f}"
            if col == 4:
                return f"{item['selling_price']:.2f}"
            if col == 5:
                return item["category"]
            if col == 6:
                expiry = item.get("expiry_date")
                if expiry:
                    if isinstance(expiry, DateType):
                        return expiry.isoformat()
                    else:
                        return str(expiry)
                else:
                    return "N/A"
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None

    def get_item(self, row):
        return self._items[row] if 0 <= row < len(self._items) else None

    def update_items(self, items):
        self.beginResetModel()
        self._items = items
        self.endResetModel()


# ------------------ Controller ------------------
class StockController:
    def __init__(self, ui, page):
        self.ui = ui
        self.page = page
        self.current_item_id = None

        # Connect buttons
        self.ui.btnRetailAdd.clicked.connect(self.handle_add)
        self.ui.btnRetailEdit.clicked.connect(self.handle_edit)
        self.ui.btnRetailDelete.clicked.connect(self.handle_delete)
        self.ui.btnRetailClear.clicked.connect(self.handle_clear)

        # Filter
        self.ui.inputRetailFilter.textChanged.connect(self.handle_filter)
        self.ui.btnRetailFilter.clicked.connect(self.handle_filter_btn)

        # Table model
        self.model = StockTableModel([])
        self.ui.RetailTable.setModel(self.model)
        self.ui.RetailTable.doubleClicked.connect(self.handle_row_double_click)

        # Initial load
        self.refresh_table()

    # ---------------- Validation (unchanged) ----------------
    def clear_validation_styles(self):
        for field in [
            self.ui.inputRetailName,
            self.ui.inputRetailQty,
            self.ui.inputRetailCost,
            self.ui.inputRetailSelling,
        ]:
            field.setStyleSheet("")

    def validate_inputs(self):
        self.clear_validation_styles()
        valid = True

        name = self.ui.inputRetailName.text().strip()
        qty = self.ui.inputRetailQty.text().strip()
        cost = self.ui.inputRetailCost.text().strip()
        sell = self.ui.inputRetailSelling.text().strip()

        def mark_invalid(widget):
            widget.setStyleSheet("border: 2px solid red;")

        if not name:
            mark_invalid(self.ui.inputRetailName)
            valid = False
        if not qty.isdigit():
            mark_invalid(self.ui.inputRetailQty)
            valid = False
        try:
            cost_val = float(cost)
        except ValueError:
            mark_invalid(self.ui.inputRetailCost)
            valid = False
            cost_val = 0
        try:
            sell_val = float(sell)
        except ValueError:
            mark_invalid(self.ui.inputRetailSelling)
            valid = False
            sell_val = 0

        if valid and sell_val < cost_val:
            mark_invalid(self.ui.inputRetailSelling)
            valid = False

        return valid

    def get_form_data(self):
        name = self.ui.inputRetailName.text().strip()
        qty = int(self.ui.inputRetailQty.text().strip())
        cost = float(self.ui.inputRetailCost.text().strip())
        sell = float(self.ui.inputRetailSelling.text().strip())
        category = self.ui.inputRetailCategory.currentText().strip().lower()

        expiry = (
            self.ui.dateRetailExpiry.date().toString("yyyy-MM-dd")
            if self.ui.checkRetailExpiry.isChecked()
            else None
        )
        return name, qty, cost, sell, category, expiry

    # ---------------- Handlers ----------------
    def handle_add(self):
        if not self.validate_inputs():
            return
        name, qty, cost, sell, category, expiry = self.get_form_data()
        result = StockAPI.create_stock(name, qty, cost, sell, category, expiry)
        if not result["success"]:
            QMessageBox.warning(
                self.page, "Add Failed", result.get("error", "Unknown error")
            )
            logger.error(result["error"])
            return
        self.refresh_table()
        self.handle_clear()

    def handle_edit(self):
        if self.current_item_id is None or not self.validate_inputs():
            return
        name, qty, cost, sell, category, expiry = self.get_form_data()
        result = StockAPI.update_stock(
            self.current_item_id, name, qty, cost, sell, category, expiry
        )
        if not result["success"]:
            QMessageBox.warning(
                self.page, "Edit Failed", result.get("error", "Unknown error")
            )
            logger.error(result["error"])
            return
        self.refresh_table()
        self.handle_clear()

    def handle_delete(self):
        if self.current_item_id is None:
            return

        result = StockAPI.delete_stock(self.current_item_id)

        if result["success"]:
            if result.get("archived", False):
                title = "Stock Archived"
            else:
                title = "Stock Deleted"
            msg = result["message"]
            QMessageBox.information(self.page, title, msg)
        else:
            msg = result.get("error", "Unknown error")
            QMessageBox.warning(self.page, "Operation Failed", msg)

        self.refresh_table()
        self.handle_clear()

    def handle_clear(self):
        self.ui.inputRetailId.clear()
        self.ui.inputRetailName.clear()
        self.ui.inputRetailQty.clear()
        self.ui.inputRetailCost.clear()
        self.ui.inputRetailSelling.clear()
        self.ui.checkRetailExpiry.setChecked(False)
        self.ui.inputRetailCategory.setCurrentIndex(0)
        self.clear_validation_styles()
        self.current_item_id = None

    def handle_filter(self, text):
        text = text.strip()
        if not text:
            self.refresh_table()
        else:
            items = self.model._items
            filtered = [i for i in items if text.lower() in i["item_name"].lower()]
            self.populate_table(filtered)

    def handle_filter_btn(self):
        self.handle_filter(self.ui.inputRetailFilter.text().strip())

    def handle_row_double_click(self, index):
        item = self.model.get_item(index.row())
        if not item:
            return

        self.current_item_id = item["id"]
        self.ui.inputRetailId.setText(str(item["id"]))
        self.ui.inputRetailName.setText(item["item_name"])
        self.ui.inputRetailQty.setText(str(item["quantity"]))
        self.ui.inputRetailCost.setText(str(item["cost_price"]))
        self.ui.inputRetailSelling.setText(str(item["selling_price"]))
        self.ui.inputRetailCategory.setCurrentText(item["category"].capitalize())

        expiry = item.get("expiry_date")
        if expiry:
            self.ui.checkRetailExpiry.setChecked(True)
            if isinstance(expiry, DateType):  # real date object
                qdate = QtCore.QDate(expiry.year, expiry.month, expiry.day)
            else:  # fallback if string
                qdate = QtCore.QDate.fromString(str(expiry), "yyyy-MM-dd")
            self.ui.dateRetailExpiry.setDate(qdate)
        else:
            self.ui.checkRetailExpiry.setChecked(False)

    # ---------------- Refresh ----------------
    def refresh_table(self):
        result = StockAPI.get_all()
        if not result.get("success", True):
            logger.error(result.get("error", "Failed to refresh stock"))
            return
        self.populate_table(result["items"])
        logger.debug("StockController refreshed")

    def populate_table(self, items):
        self.model.update_items(items)

        total = {
            "retail": {"count": 0, "cost": 0.0, "sell": 0.0, "profit": 0.0},
            "wholesale": {"count": 0, "cost": 0.0, "sell": 0.0, "profit": 0.0},
        }

        for item in items:
            cat = item["category"].lower()
            if cat in total:
                q = item["quantity"]
                c = item["cost_price"]
                s = item["selling_price"]
                total[cat]["count"] += q
                total[cat]["cost"] += c * q
                total[cat]["sell"] += s * q
                total[cat]["profit"] += (s - c) * q

        def display_lcd(lcd, value):
            lcd.display(f"{value:.2f}")

        display_lcd(self.ui.lcdRetailItems, total["retail"]["count"])
        display_lcd(self.ui.lcdRetailCosts, total["retail"]["cost"])
        display_lcd(self.ui.lcdRetailValues, total["retail"]["sell"])
        display_lcd(self.ui.lcdRetailProfits, total["retail"]["profit"])

        display_lcd(self.ui.lcdsWholesaleItems, total["wholesale"]["count"])
        display_lcd(self.ui.lcdsWholesaleCosts, total["wholesale"]["cost"])
        display_lcd(self.ui.lcdsWholesaleValues, total["wholesale"]["sell"])
        display_lcd(self.ui.lcdsWholesaleProfits, total["wholesale"]["profit"])
