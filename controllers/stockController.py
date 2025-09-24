from PySide6 import QtCore, QtGui, QtWidgets
from backend.apis import StockAPI
from datetime import datetime, date


class StockEvents(QtCore.QObject):
    stock_changed = QtCore.Signal()  # global signal for stock updates


stock_events = StockEvents()


class StockController:
    def __init__(self, ui, page):
        self.ui = ui
        self.page = page
        self.selected_stock_id = None
        self.setup_validators()
        self.setup_connections()
        self.load_stocks()

    # ------------------ VALIDATORS ------------------
    def setup_validators(self):
        int_validator = QtGui.QIntValidator(0, 999999)
        double_validator = QtGui.QDoubleValidator(0.0, 999999.99, 2)
        double_validator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        self.ui.inputRetailQty.setValidator(int_validator)
        self.ui.inputRetailCost.setValidator(double_validator)
        self.ui.inputRetailSelling.setValidator(double_validator)

    # ------------------ CONNECTIONS ------------------
    def setup_connections(self):
        self.ui.btnRetailAdd.clicked.connect(self.add_stock)
        self.ui.btnRetailEdit.clicked.connect(self.update_stock)
        self.ui.btnRetailDelete.clicked.connect(self.delete_stock)
        self.ui.btnRetailClear.clicked.connect(self.clear_inputs)
        self.ui.btnRetailFilter.clicked.connect(self.filter_stocks)
        self.ui.inputRetailFilter.textChanged.connect(self.filter_stocks)
        self.ui.table_stock.doubleClicked.connect(self.load_row_to_inputs)
        # Connect to global stock changed signal to refresh table on external changes
        stock_events.stock_changed.connect(self.load_stocks)

    # ------------------ LOAD STOCKS ------------------
    def load_stocks(self):
        result = StockAPI.get_all()
        if result["success"]:
            active_items = [s for s in result["items"] if s.get("is_active", True)]
            self.populate_stock_table(active_items)
            self.update_lcds(active_items)
        else:
            self.show_error(result["error"])

    # ------------------ POPULATE TABLE ------------------
    def populate_stock_table(self, stocks):
        model = QtGui.QStandardItemModel()
        headers = [
            "ID",
            "Item Name",
            "Quantity",
            "Cost Price",
            "Selling Price",
            "Category",
            "Expiry Date",
        ]
        model.setHorizontalHeaderLabels(headers)

        for stock in stocks:
            expiry_date = stock.get("expiry_date")
            if expiry_date:
                expiry = (
                    expiry_date.strftime("%Y-%m-%d")
                    if hasattr(expiry_date, "strftime")
                    else str(expiry_date)
                )
            else:
                expiry = "N/A"

            row = [
                QtGui.QStandardItem(str(stock["id"])),
                QtGui.QStandardItem(stock["item_name"]),
                QtGui.QStandardItem(str(stock["quantity"])),
                QtGui.QStandardItem(f"{stock['cost_price']:.2f}"),
                QtGui.QStandardItem(f"{stock['selling_price']:.2f}"),
                QtGui.QStandardItem(stock["category"]),
                QtGui.QStandardItem(expiry),
            ]
            model.appendRow(row)

        self.ui.table_stock.setModel(model)
        self.ui.table_stock.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

    # ------------------ FILTER ------------------
    def filter_stocks(self):
        text = self.ui.inputRetailFilter.text().strip().lower()
        result = StockAPI.get_all()
        if result["success"]:
            active_items = [s for s in result["items"] if s.get("is_active", True)]
            filtered = [s for s in active_items if text in s["item_name"].lower()]
            self.populate_stock_table(filtered)
            self.update_lcds(filtered)

    # ------------------ ADD STOCK ------------------
    def add_stock(self):
        name = self.ui.inputRetailName.text().strip()
        qty = self.ui.inputRetailQty.text().strip()
        cost = self.ui.inputRetailCost.text().strip()
        selling = self.ui.inputRetailSelling.text().strip()
        category = self.ui.inputRetailCategory.currentText()
        expiry = (
            self.ui.dateRetailExpiry.date().toString("yyyy-MM-dd")
            if self.ui.checkRetailExpiry.isChecked()
            else None
        )

        if not name or not qty or not cost or not selling:
            self.show_error("All fields are required!")
            return

        result = StockAPI.create_stock(
            name, int(qty), float(cost), float(selling), category, expiry
        )
        if result["success"]:
            self.load_stocks()
            self.clear_inputs()
            stock_events.stock_changed.emit()
        else:
            self.show_error(result["error"])

    # ------------------ UPDATE STOCK ------------------
    def update_stock(self):
        if not self.selected_stock_id:
            self.show_error("Select a stock to update")
            return

        name = self.ui.inputRetailName.text().strip()
        qty = self.ui.inputRetailQty.text().strip()
        cost = self.ui.inputRetailCost.text().strip()
        selling = self.ui.inputRetailSelling.text().strip()
        category = self.ui.inputRetailCategory.currentText()
        expiry = (
            self.ui.dateRetailExpiry.date().toString("yyyy-MM-dd")
            if self.ui.checkRetailExpiry.isChecked()
            else None
        )

        result = StockAPI.update_stock(
            self.selected_stock_id,
            name,
            int(qty),
            float(cost),
            float(selling),
            category,
            expiry,
        )
        if result["success"]:
            self.load_stocks()
            self.clear_inputs()
            stock_events.stock_changed.emit()
        else:
            self.show_error(result["error"])

    # ------------------ DELETE STOCK ------------------
    def delete_stock(self):
        if not self.selected_stock_id:
            self.show_error("Select a stock to delete")
            return

        confirm = QtWidgets.QMessageBox.warning(
            self.page,
            "Confirm Delete",
            "Are you sure you want to delete/archive this stock?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            result = StockAPI.delete_stock(self.selected_stock_id)
            if result["success"]:
                self.load_stocks()
                self.clear_inputs()
                stock_events.stock_changed.emit()
            else:
                self.show_error(result["error"])

    # ------------------ ROW TO INPUTS ------------------
    def load_row_to_inputs(self, index):
        row = index.row()
        model = self.ui.table_stock.model()
        self.selected_stock_id = int(model.item(row, 0).text())
        self.ui.inputRetailName.setText(model.item(row, 1).text())
        self.ui.inputRetailQty.setText(model.item(row, 2).text())
        self.ui.inputRetailCost.setText(model.item(row, 3).text())
        self.ui.inputRetailSelling.setText(model.item(row, 4).text())
        self.ui.inputRetailCategory.setCurrentText(model.item(row, 5).text())
        expiry = model.item(row, 6).text()
        if expiry != "N/A":
            self.ui.checkRetailExpiry.setChecked(True)
            self.ui.dateRetailExpiry.setDate(
                QtCore.QDate.fromString(expiry, "yyyy-MM-dd")
            )
        else:
            self.ui.checkRetailExpiry.setChecked(False)

    # ------------------ CLEAR INPUTS ------------------
    def clear_inputs(self):
        self.selected_stock_id = None
        self.ui.inputRetailName.clear()
        self.ui.inputRetailQty.clear()
        self.ui.inputRetailCost.clear()
        self.ui.inputRetailSelling.clear()
        self.ui.checkRetailExpiry.setChecked(False)
        self.ui.inputRetailFilter.clear()

    # ------------------ LCD UPDATES ------------------
    def update_lcds(self, stocks):
        retail_items = sum(
            s["quantity"] for s in stocks if s["category"].lower() == "retail"
        )
        wholesale_items = sum(
            s["quantity"] for s in stocks if s["category"].lower() == "wholesale"
        )

        retail_cost = sum(
            s["cost_price"] * s["quantity"]
            for s in stocks
            if s["category"].lower() == "retail"
        )
        wholesale_cost = sum(
            s["cost_price"] * s["quantity"]
            for s in stocks
            if s["category"].lower() == "wholesale"
        )

        retail_value = sum(
            s["selling_price"] * s["quantity"]
            for s in stocks
            if s["category"].lower() == "retail"
        )
        wholesale_value = sum(
            s["selling_price"] * s["quantity"]
            for s in stocks
            if s["category"].lower() == "wholesale"
        )

        retail_profit = retail_value - retail_cost
        wholesale_profit = wholesale_value - wholesale_cost

        self.ui.lcdRetailItems.display(retail_items)
        self.ui.lcdsWholesaleItems.display(wholesale_items)
        self.ui.lcdRetailCosts.display(retail_cost)
        self.ui.lcdsWholesaleCosts.display(wholesale_cost)
        self.ui.lcdRetailValues.display(retail_value)
        self.ui.lcdsWholesaleValues.display(wholesale_value)
        self.ui.lcdRetailProfits.display(retail_profit)
        self.ui.lcdsWholesaleProfits.display(wholesale_profit)

    # ------------------ ERROR POPUP ------------------
    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self.page, "Error", message)
