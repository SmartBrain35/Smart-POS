from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from backend.apis import ExpenditureAPI


class ExpenditureController:
    def __init__(self, ui):
        self.ui = ui
        self.load_expenditures()

        # Connect buttons
        self.ui.btnAddExpenditure.clicked.connect(self.add_expenditure)
        self.ui.btnRefreshExpenditures.clicked.connect(self.load_expenditures)

    def load_expenditures(self):
        """Load all expenditures into the table."""
        resp = ExpenditureAPI.get_all_expenditures()
        if not resp.get("success"):
            QMessageBox.warning(
                self.ui, "Error", resp.get("error", "Failed to fetch expenditures")
            )
            return

        expenditures = resp["expenditures"]
        self.ui.tableExpenditures.setRowCount(0)

        for row, exp in enumerate(expenditures):
            self.ui.tableExpenditures.insertRow(row)
            self.ui.tableExpenditures.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(exp["id"]))
            )
            self.ui.tableExpenditures.setItem(
                row, 1, QtWidgets.QTableWidgetItem(exp["description"])
            )
            self.ui.tableExpenditures.setItem(
                row, 2, QtWidgets.QTableWidgetItem(f"{exp['amount']:.2f}")
            )
            self.ui.tableExpenditures.setItem(
                row, 3, QtWidgets.QTableWidgetItem(exp["category"])
            )
            self.ui.tableExpenditures.setItem(
                row, 4, QtWidgets.QTableWidgetItem(exp["expense_date"])
            )

    def add_expenditure(self):
        """Add a new expenditure record."""
        description = self.ui.txtDescription.text()
        amount = float(self.ui.spinAmount.value())
        category = self.ui.cboCategory.currentText().lower()
        expense_date = self.ui.dateExpense.date().toString("yyyy-MM-dd")

        resp = ExpenditureAPI.create_expenditure(
            description, amount, category, expense_date
        )
        if not resp.get("success"):
            QMessageBox.warning(
                self.ui, "Error", resp.get("error", "Failed to add expenditure")
            )
            return

        QMessageBox.information(self.ui, "Success", "Expenditure added successfully")
        self.load_expenditures()
