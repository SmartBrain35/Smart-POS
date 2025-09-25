import logging
from datetime import date
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide6.QtGui import QTextDocument
from backend.apis import SaleAPI
from ui.sales_history_ui import Ui_SalesHistory

logger = logging.getLogger("HistoryController")


# -------------------- Custom Delegate for Actions Column --------------------
class ActionsDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.delete_icon = QtGui.QIcon.fromTheme("edit-delete")
        self.print_icon = QtGui.QIcon.fromTheme("document-print")
        self.icon_size = QtCore.QSize(24, 24)

    def paint(self, painter, option, index):
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
        rect = option.rect
        spacing = 5
        delete_rect = QtCore.QRect(
            rect.left() + spacing,
            rect.top() + (rect.height() - self.icon_size.height()) // 2,
            self.icon_size.width(),
            self.icon_size.height(),
        )
        print_rect = QtCore.QRect(
            delete_rect.right() + spacing,
            rect.top() + (rect.height() - self.icon_size.height()) // 2,
            self.icon_size.width(),
            self.icon_size.height(),
        )
        self.delete_icon.paint(painter, delete_rect)
        self.print_icon.paint(painter, print_rect)

    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonRelease:
            pos = event.pos()
            rect = option.rect
            spacing = 5
            delete_rect = QtCore.QRect(
                rect.left() + spacing,
                rect.top() + (rect.height() - self.icon_size.height()) // 2,
                self.icon_size.width(),
                self.icon_size.height(),
            )
            print_rect = QtCore.QRect(
                delete_rect.right() + spacing,
                rect.top() + (rect.height() - self.icon_size.height()) // 2,
                self.icon_size.width(),
                self.icon_size.height(),
            )

            if delete_rect.contains(pos):
                self.controller.delete_sale(index.row())
                return True
            elif print_rect.contains(pos):
                self.controller.print_sale(index.row())
                return True
        return super().editorEvent(event, model, option, index)


# -------------------- Table Model --------------------
class SalesHistoryModel(QtCore.QAbstractTableModel):
    HEADERS = [
        "Invoice",
        "Customer",
        "Date",
        "Amount",
        "Pay Method",
        "Daily Sales",
        "Profit",
        "Items Sold",
        "Actions",
    ]

    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self._data = data or []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        value = self._data[row][col]
        if role == QtCore.Qt.DisplayRole:
            if col == self.columnCount() - 1:
                return ""
            return str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            return (
                self.HEADERS[section]
                if orientation == QtCore.Qt.Horizontal
                else section + 1
            )
        return None

    def set_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()


# -------------------- Proxy Model --------------------
class SalesHistoryProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.date_filter_str = None
        self.search_text = ""

    def set_search_text(self, text: str):
        self.search_text = text.lower()
        self.invalidateFilter()

    def set_date_filter(self, date_str: str | None):
        self.date_filter_str = date_str
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        model = self.sourceModel()
        if self.date_filter_str:
            date_value = model.data(model.index(source_row, 2), QtCore.Qt.DisplayRole)
            if date_value != self.date_filter_str:
                return False

        if self.search_text:
            invoice_value = (
                model.data(model.index(source_row, 0), QtCore.Qt.DisplayRole) or ""
            )
            customer_value = (
                model.data(model.index(source_row, 1), QtCore.Qt.DisplayRole) or ""
            )
            if (
                self.search_text not in invoice_value.lower()
                and self.search_text not in customer_value.lower()
            ):
                return False

        return True


# -------------------- Main Controller --------------------
class HistoryController(QtWidgets.QDialog, Ui_SalesHistory):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Sales History")
        self.setModal(False)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)

        # Map UI elements
        self.search_box = self.searchBox
        self.date_filter = self.dateFilter
        self.refresh_btn = self.refreshButton
        self.export_btn = self.exportButton
        self.table_view = self.tableSalesHistory
        self.status_label = self.labelStatus

        # --- Model ---
        self.model = SalesHistoryModel([])
        self.proxy_model = SalesHistoryProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.table_view.setModel(self.proxy_model)

        # --- Actions column ---
        actions_col = self.model.columnCount() - 1
        self.table_view.setItemDelegateForColumn(
            actions_col, ActionsDelegate(controller=self, parent=self.table_view)
        )

        # --- Signals ---
        self.refresh_btn.clicked.connect(self.load_sales)
        self.export_btn.clicked.connect(self.export_csv)
        self.search_box.textChanged.connect(self.proxy_model.set_search_text)
        self.date_filter.dateChanged.connect(
            lambda qdate: self.proxy_model.set_date_filter(qdate.toString("yyyy-MM-dd"))
        )
        self.table_view.doubleClicked.connect(self.show_sale_items)

        self.load_sales()

    # -------------------- Load Sales --------------------
    def load_sales(self):
        try:
            result = SaleAPI.get_all_sales()
            if not result["success"]:
                raise ValueError(result.get("error", "Unknown error"))

            formatted = []
            for s in result["sales"]:
                totals = SaleAPI.get_totals_by_date(s["sale_date"])
                formatted.append(
                    [
                        f"INV-{s['id']:05d}",
                        s.get("customer_name", "N/A"),
                        (
                            s["sale_date"].strftime("%Y-%m-%d")
                            if isinstance(s["sale_date"], date)
                            else s["sale_date"]
                        ),
                        f"{s['amount_paid']:.2f}",
                        s.get("payment_method", "N/A"),
                        f"{totals.get('gross', 0):.2f}",
                        f"{totals.get('profit', 0):.2f}",
                        str(totals.get("items_sold", 0)),
                        "",
                    ]
                )

            self.model.set_data(formatted)
            self.status_label.setText(f"Loaded {len(formatted)} records.")
        except Exception as e:
            logger.error("Error loading sales: %s", e)
            self.status_label.setText("Error loading sales!")

    # -------------------- Export CSV --------------------
    def export_csv(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save CSV", "", "CSV Files (*.csv)"
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(",".join(SalesHistoryModel.HEADERS) + "\n")
                for row in range(self.proxy_model.rowCount()):
                    row_data = [
                        self.proxy_model.data(self.proxy_model.index(row, col))
                        for col in range(self.proxy_model.columnCount())
                    ]
                    f.write(",".join(row_data) + "\n")
            self.status_label.setText(f"Exported to {path}")
        except Exception as e:
            logger.error("Export failed: %s", e)
            self.status_label.setText("Export failed!")

    # -------------------- Delete Action --------------------
    def delete_sale(self, row: int):
        invoice = self.proxy_model.data(self.proxy_model.index(row, 0))
        sale_id = int(invoice.replace("INV-", ""))  # FIXED: correct ID
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete {invoice}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                result = SaleAPI.delete_sale(sale_id)
                if result.get("success"):
                    QtWidgets.QMessageBox.information(
                        self, "Deleted", f"{invoice} deleted successfully!"
                    )
                    self.load_sales()
                else:
                    QtWidgets.QMessageBox.warning(
                        self, "Error", result.get("error", "Delete failed")
                    )
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Delete failed: {e}")

    # -------------------- Print Action --------------------
    def print_sale(self, row: int):
        invoice = self.proxy_model.data(self.proxy_model.index(row, 0))
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirm Print",
            f"Do you want to print {invoice}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                printer = QPrinter(QPrinter.HighResolution)
                preview = QPrintPreviewDialog(printer, self)

                def render_preview(p):
                    doc = QTextDocument()
                    doc.setHtml(f"<h2>{invoice}</h2><p>Invoice print preview</p>")
                    doc.print_(p)

                preview.paintRequested.connect(render_preview)
                preview.exec()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Print failed: {e}")

    # -------------------- Show Items Dialog --------------------
    def show_sale_items(self, index: QtCore.QModelIndex):
        try:
            row = index.row()
            invoice = self.proxy_model.data(self.proxy_model.index(row, 0))
            sale_id = int(invoice.replace("INV-", ""))

            # Fetch sale details and items
            result = SaleAPI.get_sale_by_id(sale_id)
            if not result.get("success"):
                QtWidgets.QMessageBox.warning(
                    self, "Error", result.get("error", "Failed to fetch sale details")
                )
                return

            sale = result["sale"]
            items = result["items"]

            # --- Create Frameless Dialog ---
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog)
            dialog.resize(300, 450)  # Small, receipt-like size
            dialog.setFixedSize(dialog.size())
            layout = QtWidgets.QVBoxLayout(dialog)

            # --- Monospace font for receipt style ---
            receipt_font = QtGui.QFont("Courier New", 10)
            receipt_font.setStyleHint(QtGui.QFont.Monospace)

            # --- Receipt Header ---
            header = QtWidgets.QLabel(
                f"<div style='text-align:center;'>"
                f"<h3>STORE NAME</h3>"
                f"Invoice: {invoice}<br>"
                f"Date: {sale.get('sale_date', 'N/A')}<br>"
                f"Customer: {sale.get('customer_name', 'N/A')}<br>"
                f"</div>"
            )
            header.setFont(receipt_font)
            layout.addWidget(header)

            # --- Separator ---
            layout.addWidget(QtWidgets.QLabel("-" * 40))

            # --- Items Table ---
            table = QtWidgets.QTableWidget(dialog)
            table.setStyleSheet("color: black; font-weight: bold")
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Item", "Qty", "Price"])
            table.setRowCount(len(items))
            table.horizontalHeader().setStretchLastSection(False)
            table.verticalHeader().setVisible(False)
            table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            table.setShowGrid(False)
            table.setAlternatingRowColors(False)
            table.setFont(receipt_font)
            table.setFixedHeight(200)

            total = 0
            for row_idx, item in enumerate(items):
                name = item.get("item_name", "N/A")
                qty = item.get("quantity_sold", 0)
                price = item.get("price", 0.0)
                total += price * qty
                table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(name)))
                table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(qty)))
                table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(f"{price:.2f}"))

            layout.addWidget(table)

            # --- Separator ---
            layout.addWidget(QtWidgets.QLabel("-" * 40))

            # --- Total Section ---
            total_label = QtWidgets.QLabel(
                f"<div style='text-align:right;'><b>Total: {total:.2f}</b></div>"
            )
            total_label.setFont(receipt_font)
            layout.addWidget(total_label)

            # --- Buttons at the bottom ---
            btn_layout = QtWidgets.QHBoxLayout()
            btn_print = QtWidgets.QPushButton("Print")
            btn_print.clicked.connect(
                lambda: QtWidgets.QMessageBox.information(
                    dialog, "Print", "Printing coming soon..."
                )
            )
            btn_close = QtWidgets.QPushButton("Close")
            btn_close.clicked.connect(dialog.close)
            btn_layout.addWidget(btn_print)
            btn_layout.addWidget(btn_close)

            layout.addLayout(btn_layout)

            dialog.exec()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not load items: {e}")


"""     def show_sale_items(self, index: QtCore.QModelIndex):
        try:
            # Get row index and invoice number
            row = index.row()
            invoice = self.proxy_model.data(self.proxy_model.index(row, 0))
            sale_id = int(invoice.replace("INV-", ""))  # Extract sale_id from INV-00001

            # Fetch sale details and items from database
            result = SaleAPI.get_sale_by_id(sale_id)
            if not result.get("success"):
                QtWidgets.QMessageBox.warning(
                    self, "Error", result.get("error", "Failed to fetch sale details")
                )
                return

            sale = result["sale"]
            items = result["items"]

            # --- Frameless QDialog ---
            dialog = QtWidgets.QDialog(
                self, QtCore.Qt.FramelessWindowHint | QtCore.Qt.Dialog
            )
            dialog.setWindowTitle(f"Invoice - {invoice}")
            dialog.resize(300, 600)

            layout = QtWidgets.QVBoxLayout(dialog)

            # --- Table for invoice items ---
            table = QtWidgets.QTableWidget(dialog)
            table.setStyleSheet("color: black; font-weight: bold")
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Price"])
            table.setRowCount(len(items))
            table.horizontalHeader().setStretchLastSection(False)
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            table.verticalHeader().setVisible(False)
            table.setShowGrid(False)

            total_amount = 0.0
            for row_idx, item in enumerate(items):
                table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(item["item_name"]))
                table.setItem(
                    row_idx, 1, QtWidgets.QTableWidgetItem(str(item["quantity_sold"]))
                )
                price = item["price"]
                table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(f"{price:.2f}"))
                total_amount += price * item["quantity_sold"]

            layout.addWidget(table)

            # --- Total label ---
            total_label = QtWidgets.QLabel(f"<b>Total: {total_amount:.2f}</b>")
            total_label.setAlignment(QtCore.Qt.AlignRight)
            layout.addWidget(total_label)

            # --- Buttons (Print & Close) ---
            btn_layout = QtWidgets.QHBoxLayout()
            btn_print = QtWidgets.QPushButton("Print Invoice")
            btn_close = QtWidgets.QPushButton("Close")

            btn_layout.addWidget(btn_print)
            btn_layout.addStretch()
            btn_layout.addWidget(btn_close)

            layout.addLayout(btn_layout)

            # --- Print action ---
            def print_invoice():
                printer = QPrinter(QPrinter.HighResolution)
                preview = QPrintPreviewDialog(printer, self)

                def render_preview(p):
                    html_content = f"<h2>Invoice {invoice}</h2><table border='1' width='100%' cellspacing='0' cellpadding='3'>"
                    html_content += (
                        "<tr><th>Item Name</th><th>Quantity</th><th>Price</th></tr>"
                    )
                    for item in items:
                        html_content += f"<tr><td>{item['item_name']}</td><td>{item['quantity_sold']}</td><td>{item['price']:.2f}</td></tr>"
                    html_content += f"</table><h3>Total: {total_amount:.2f}</h3>"

                    doc = QTextDocument()
                    doc.setHtml(html_content)
                    doc.print_(p)

                preview.paintRequested.connect(render_preview)
                preview.exec()

            btn_print.clicked.connect(print_invoice)
            btn_close.clicked.connect(dialog.close)

            # --- Show dialog ---
            dialog.exec()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not load items: {e}")
 """
