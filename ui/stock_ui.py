from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from stock_controller import StockController
import csv

LOW_STOCK_THRESHOLD = 5  # Items below this quantity will be highlighted

class StockWindow(QtWidgets.QWidget):
    def __init__(self, db_session):
        super().__init__()
        self.setWindowTitle("Stock Management")
        self.setGeometry(100, 100, 1000, 550)
        self.controller = StockController(db_session)

        # Main layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Search bar and export button
        search_layout = QtWidgets.QHBoxLayout()
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search by name, category, or unit type...")
        search_layout.addWidget(self.search_input)

        self.export_btn = QtWidgets.QPushButton("Export to CSV")
        search_layout.addWidget(self.export_btn)
        layout.addLayout(search_layout)

        # Stock table
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Unit Type", "Category",
            "Cost Price", "Selling Price", "Quantity", "Profit"
        ])
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.add_btn = QtWidgets.QPushButton("Add Item")
        self.update_btn = QtWidgets.QPushButton("Update Item")
        self.delete_btn = QtWidgets.QPushButton("Delete Item")
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        # Total profit label
        self.total_profit_label = QtWidgets.QLabel("Total Profit: 0.00")
        layout.addWidget(self.total_profit_label)

        # Connections
        self.add_btn.clicked.connect(self.add_item_dialog)
        self.update_btn.clicked.connect(self.update_item_dialog)
        self.delete_btn.clicked.connect(self.delete_item)
        self.search_input.textChanged.connect(self.filter_table)
        self.export_btn.clicked.connect(self.export_csv)
        self.table.cellDoubleClicked.connect(self.double_click_edit)

        self.load_stock()

    def load_stock(self):
        self.table.setRowCount(0)
        items = self.controller.get_all_items()
        self.all_items = items  # Keep full list for filtering
        total_profit = 0.0

        for row_idx, item in enumerate(items):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(item.id)))
            self.table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(item.name))
            self.table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(item.unit_type))
            self.table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(str(item.category)))
            self.table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(f"{item.cost_price:.2f}"))
            self.table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(f"{item.selling_price:.2f}"))
            self.table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(str(item.quantity)))

            profit = item.selling_price - item.cost_price
            profit_item = QtWidgets.QTableWidgetItem(f"{profit:.2f}")
            profit_item.setForeground(QColor('green') if profit >= 0 else QColor('red'))
            self.table.setItem(row_idx, 7, profit_item)

            # Highlight low stock
            if item.quantity <= LOW_STOCK_THRESHOLD:
                for col in range(8):
                    self.table.item(row_idx, col).setBackground(QColor('#FFF3CD'))

            total_profit += profit * item.quantity

        self.total_profit_label.setText(f"Total Profit: {total_profit:.2f}")

    def add_item_dialog(self):
        dialog = StockDialog(self.controller)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_stock()

    def update_item_dialog(self):
        selected = self.table.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(self, "No selection", "Select an item to update.")
            return
        item_id = int(self.table.item(selected, 0).text())
        dialog = StockDialog(self.controller, item_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_stock()

    def delete_item(self):
        selected = self.table.currentRow()
        if selected < 0:
            QtWidgets.QMessageBox.warning(self, "No selection", "Select an item to delete.")
            return
        item_id = int(self.table.item(selected, 0).text())
        confirm = QtWidgets.QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this item?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if confirm == QtWidgets.QMessageBox.Yes:
            self.controller.delete_stock(item_id)
            self.load_stock()

    def filter_table(self):
        text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 1).text().lower()
            unit = self.table.item(row, 2).text().lower()
            category = self.table.item(row, 3).text().lower()
            self.table.setRowHidden(row, text not in name and text not in unit and text not in category)

    def export_csv(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export CSV", "", "CSV Files (*.csv)")
        if path:
            with open(path, 'w', newline='') as f:
                writer = csv.writer(f)
                headers = [self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())]
                writer.writerow(headers)
                for row in range(self.table.rowCount()):
                    if self.table.isRowHidden(row):
                        continue
                    row_data = [self.table.item(row, col).text() for col in range(self.table.columnCount())]
                    writer.writerow(row_data)
            QtWidgets.QMessageBox.information(self, "Exported", f"Stock exported to {path}")

    def double_click_edit(self, row, column):
        item_id = int(self.table.item(row, 0).text())
        dialog = StockDialog(self.controller, item_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_stock()


class StockDialog(QtWidgets.QDialog):
    def __init__(self, controller, item_id=None):
        super().__init__()
        self.controller = controller
        self.item_id = item_id
        self.setWindowTitle("Add / Update Stock Item")
        self.setGeometry(150, 150, 400, 300)

        layout = QtWidgets.QFormLayout()
        self.setLayout(layout)

        self.name_input = QtWidgets.QLineEdit()
        self.unit_input = QtWidgets.QLineEdit()
        self.category_input = QtWidgets.QLineEdit()
        self.cost_input = QtWidgets.QDoubleSpinBox()
        self.cost_input.setMaximum(1_000_000)
        self.selling_input = QtWidgets.QDoubleSpinBox()
        self.selling_input.setMaximum(1_000_000)
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setMaximum(1_000_000)

        layout.addRow("Name:", self.name_input)
        layout.addRow("Unit Type:", self.unit_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow("Cost Price:", self.cost_input)
        layout.addRow("Selling Price:", self.selling_input)
        layout.addRow("Quantity:", self.quantity_input)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.save_item)
        layout.addRow(self.save_btn)

        if item_id:
            self.load_item(item_id)

    def load_item(self, item_id):
        item = self.controller.get_item(item_id)
        if item:
            self.name_input.setText(item.name)
            self.unit_input.setText(item.unit_type)
            self.category_input.setText(str(item.category))
            self.cost_input.setValue(item.cost_price)
            self.selling_input.setValue(item.selling_price)
            self.quantity_input.setValue(item.quantity)

    def save_item(self):
        data = {
            "name": self.name_input.text(),
            "unit_type": self.unit_input.text(),
            "category": self.category_input.text(),
            "cost_price": self.cost_input.value(),
            "selling_price": self.selling_input.value(),
            "quantity": self.quantity_input.value()
        }
        if self.item_id:
            self.controller.update_item(self.item_id, **data)
        else:
            self.controller.add_item(**data)
        self.accept()
