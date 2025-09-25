import os
import logging
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QMessageBox, QPushButton
from backend.apis import ExpenditureAPI

logger = logging.getLogger("ExpenditureController")

# UI-friendly ↔ enum-safe mapping
CATEGORY_MAP = {
    "Utilities": "utilities",
    "Supplies": "supplies",
    "Salaries": "salaries",
    "Other": "other",
}
REVERSE_CATEGORY_MAP = {v: k for k, v in CATEGORY_MAP.items()}


class ExpenditureController:
    def __init__(self, ui, page):
        """
        ui: the generated Ui_Expenditure object (with widget attributes)
        page: the actual QWidget that acts as parent for dialogs (e.g., page container)
        """
        self.ui = ui
        self.page = page
        self.delete_icon_path = os.path.join("assets", "icons", "delete.png")
        self.selected_row_id = None

        # Connect buttons
        self.ui.btn_save_expenditure.clicked.connect(self.add_expenditure)
        self.ui.btn_edit_expenditure.clicked.connect(self.update_expenditure)
        self.ui.btn_delete_expenditure.clicked.connect(self.delete_selected)
        self.ui.btn_clear_expenditure.clicked.connect(self.clear_inputs)

        # Connect table click to populate inputs for editing
        self.ui.table_expenditure.cellClicked.connect(self.populate_inputs)

        # Connect search filter
        self.ui.filter_input_expenditure.textChanged.connect(self.filter_expenditures)

        # Initial load
        self.load_expenditures()
        self.load_lcd_totals()
        logger.debug("ExpenditureController initialized")

    # ------------------ Load Expenditures ------------------
    def load_expenditures(self):
        resp = ExpenditureAPI.get_all_expenditures()
        if not resp.get("success"):
            logger.error("Failed to load expenditures: %s", resp.get("error"))
            QMessageBox.warning(self.page, "Error", resp.get("error", "Failed to load"))
            return

        expenditures = resp["expenditures"]
        self.ui.table_expenditure.setRowCount(0)

        for row, exp in enumerate(expenditures):
            self.ui.table_expenditure.insertRow(row)
            self.ui.table_expenditure.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(exp["id"]))
            )
            self.ui.table_expenditure.setItem(
                row, 1, QtWidgets.QTableWidgetItem(exp["expense_date"])
            )
            self.ui.table_expenditure.setItem(
                row, 2, QtWidgets.QTableWidgetItem(exp["description"])
            )
            self.ui.table_expenditure.setItem(
                row, 3, QtWidgets.QTableWidgetItem(f"{exp['amount']:.2f}")
            )

            pretty_category = REVERSE_CATEGORY_MAP.get(
                exp["category"].lower(), exp["category"]
            )
            self.ui.table_expenditure.setItem(
                row, 4, QtWidgets.QTableWidgetItem(pretty_category)
            )

            # Delete button widget
            btn_delete = QPushButton()
            btn_delete.setStyleSheet("border:none; background:transparent;")
            if os.path.exists(self.delete_icon_path):
                btn_delete.setIcon(QtGui.QIcon(self.delete_icon_path))
            else:
                btn_delete.setIcon(QtGui.QIcon.fromTheme("edit-delete"))
            btn_delete.setToolTip("Delete this expenditure")
            btn_delete.clicked.connect(
                lambda _, r_id=exp["id"]: self.delete_expenditure(r_id)
            )
            self.ui.table_expenditure.setCellWidget(row, 5, btn_delete)

        logger.debug("Loaded %d expenditures", len(expenditures))

    # ------------------ Filter ------------------
    def filter_expenditures(self, text: str):
        text = text.strip().lower()
        for r in range(self.ui.table_expenditure.rowCount()):
            desc_item = self.ui.table_expenditure.item(r, 2)
            cat_item = self.ui.table_expenditure.item(r, 4)
            row_text = (
                (desc_item.text() if desc_item else "")
                + " "
                + (cat_item.text() if cat_item else "")
            ).lower()
            self.ui.table_expenditure.setRowHidden(r, text not in row_text)

    # ------------------ Populate Inputs -----------------
    def populate_inputs(self, row: int, column: int):
        try:
            self.selected_row_id = int(self.ui.table_expenditure.item(row, 0).text())
        except Exception:
            self.selected_row_id = None
            return

        # Fill fields
        date_str = self.ui.table_expenditure.item(row, 1).text()
        self.ui.expenditure_date.setDate(
            QtCore.QDate.fromString(date_str, "yyyy-MM-dd")
        )
        self.ui.expenditure_description.setText(
            self.ui.table_expenditure.item(row, 2).text()
        )
        self.ui.expenditure_amount.setText(
            self.ui.table_expenditure.item(row, 3).text()
        )

        category_label = self.ui.table_expenditure.item(row, 4).text()
        index = self.ui.expenditure_category.findText(
            category_label, QtCore.Qt.MatchFixedString
        )
        if index >= 0:
            self.ui.expenditure_category.setCurrentIndex(index)

        # 🔹 Disable Add while editing
        self.ui.btn_save_expenditure.setEnabled(False)

    # ------------------ Add Expenditure ------------------
    def add_expenditure(self):
        self._save_or_update(is_update=False)

    # ------------------ Update Expenditure ------------------
    def update_expenditure(self):
        if not self.selected_row_id:
            QMessageBox.warning(self.page, "Error", "Select a row to update first")
            return
        self._save_or_update(is_update=True)
        # 🔹 Re-enable Add button
        self.ui.btn_save_expenditure.setEnabled(True)

    # ------------------ Core Save / Update ------------------
    def _save_or_update(self, is_update: bool):
        description = self.ui.expenditure_description.text().strip()
        amount_text = self.ui.expenditure_amount.text().strip()
        pretty_category = self.ui.expenditure_category.currentText().strip()
        category = CATEGORY_MAP.get(pretty_category, pretty_category).lower()
        expense_date = self.ui.expenditure_date.date().toString("yyyy-MM-dd")

        if not description or not amount_text or not category:
            QMessageBox.warning(self.page, "Error", "All fields are required")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except Exception:
            QMessageBox.warning(self.page, "Error", "Amount must be a positive number")
            return

        if is_update:
            resp = ExpenditureAPI.update_expenditure(
                self.selected_row_id, description, amount, category, expense_date
            )
            msg = "Expenditure updated successfully"
        else:
            resp = ExpenditureAPI.create_expenditure(
                description, amount, category, expense_date
            )
            msg = "Expenditure added successfully"

        if not resp.get("success"):
            logger.error("Save operation failed: %s", resp.get("error"))
            QMessageBox.warning(
                self.page, "Error", resp.get("error", "Operation failed")
            )
            return

        QMessageBox.information(self.page, "Success", msg)
        self.clear_inputs()
        self.load_expenditures()
        self.load_lcd_totals()

    # ------------------ Delete (row button) ------------------
    def delete_expenditure(self, exp_id: int):
        confirm = QMessageBox.question(
            self.page,
            "Confirm Delete",
            "Are you sure you want to delete this record?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        resp = ExpenditureAPI.delete_expenditure(exp_id)
        if not resp.get("success"):
            logger.error("Delete failed: %s", resp.get("error"))
            QMessageBox.warning(self.page, "Error", resp.get("error", "Delete failed"))
            return

        QMessageBox.information(
            self.page, "Success", "Expenditure deleted successfully"
        )
        self.clear_inputs()
        self.load_expenditures()
        self.load_lcd_totals()

    # ------------------ Delete (main delete button) ------------------
    def delete_selected(self):
        if not self.selected_row_id:
            QMessageBox.warning(
                self.page, "Error", "No expenditure selected for deletion"
            )
            return
        self.delete_expenditure(self.selected_row_id)

    # ------------------ Clear Inputs ------------------
    def clear_inputs(self):
        self.selected_row_id = None
        self.ui.expenditure_date.setDate(QtCore.QDate.currentDate())
        self.ui.expenditure_description.clear()
        self.ui.expenditure_amount.clear()
        self.ui.expenditure_category.setCurrentIndex(0)

    # ------------------ LCD Totals ------------------
    def load_lcd_totals(self):
        totals = ExpenditureAPI.get_lcd_totals()
        if not totals.get("success"):
            logger.error("Failed to load totals: %s", totals.get("error"))
        self.ui.lcdWeeklyExpenditures.display(totals.get("weekly", 0.0))
        self.ui.lcdMonthlyExpenditures.display(totals.get("monthly", 0.0))
        self.ui.lcdYearlyExpenditures.display(totals.get("yearly", 0.0))
        logger.debug(
            "LCD totals loaded: weekly=%s monthly=%s yearly=%s",
            totals.get("weekly"),
            totals.get("monthly"),
            totals.get("yearly"),
        )
