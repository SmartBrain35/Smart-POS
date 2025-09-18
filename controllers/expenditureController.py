from PySide6.QtWidgets import QtCore, QtGui, QtWidgets, QMessageBox, QMainWindow
from ui.expenditure_ui import Ui_Expenditure
from backend.apis import ExpenditureAPI
from datetime import datetime


class ExpenditureController:
    def __init__(self, parent=None):
        self.parent = parent
        self.expenditure_window = QMainWindow()
        self.ui = Ui_Expenditure()
        self.ui.setupUi(self.expenditure_window)

        # Connect UI signals to controller methods
        self.ui.btn_save_expenditure.clicked.connect(self.handle_save_expenditure)
        self.ui.btn_edit_expenditure.clicked.connect(self.handle_edit_expenditure)
        self.ui.btn_delete_expenditure.clicked.connect(self.handle_delete_expenditure)
        self.ui.btn_clear_expenditure.clicked.connect(self.handle_clear)
        self.ui.filter_input_expenditure.textChanged.connect(self.filter_expenditures)
        self.ui.table_expenditure.clicked.connect(self.fill_form_from_selection)

        # Load initial data and update LCDs
        self.load_expenditures()
        self.update_lcds()

    def load_expenditures(self):
        # Clear existing rows
        self.ui.table_expenditure.setRowCount(0)

        # Fetch expenditures from API
        result = ExpenditureAPI.get_all_expenditures()
        if result["success"]:
            self.ui.table_expenditure.setRowCount(len(result["expenditures"]))
            for row, exp in enumerate(result["expenditures"]):
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
                self.ui.table_expenditure.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(exp["category"])
                )

                # Action column with delete button
                delete_btn = QtWidgets.QPushButton()
                delete_btn.setObjectName("ExpenditureTableBtnDelete")
                delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                delete_btn.setToolTip("Delete")
                delete_btn.setFixedSize(30, 30)
                delete_btn.clicked.connect(
                    lambda checked, r=row: self.handle_table_delete(r)
                )
                self.ui.table_expenditure.setCellWidget(row, 5, delete_btn)
        else:
            QMessageBox.warning(self.expenditure_window, "Error", result["error"])

    def handle_save_expenditure(self):
        date = self.ui.expenditure_date.date().toString("yyyy-MM-dd")
        description = self.ui.expenditure_description.text().strip()
        amount = self.ui.expenditure_amount.text().strip()
        category = self.ui.expenditure_category.currentText()

        # Validate all fields are mandatory
        if not all([date, description, amount, category]):
            QMessageBox.warning(
                self.expenditure_window, "Input Error", "All fields are mandatory."
            )
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self.expenditure_window,
                "Input Error",
                "Amount must be a positive number.",
            )
            return

        result = ExpenditureAPI.create_expenditure(description, amount, category, date)
        if result["success"]:
            QMessageBox.information(
                self.expenditure_window, "Success", result["message"]
            )
            self.handle_clear()
            self.load_expenditures()
            self.update_lcds()
        else:
            QMessageBox.warning(self.expenditure_window, "Error", result["error"])

    def handle_edit_expenditure(self):
        selected_row = self.ui.table_expenditure.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self.expenditure_window,
                "Selection Error",
                "Please select an expenditure to edit.",
            )
            return

        expenditure_id = int(self.ui.table_expenditure.item(selected_row, 0).text())
        date = self.ui.expenditure_date.date().toString("yyyy-MM-dd")
        description = self.ui.expenditure_description.text().strip()
        amount = self.ui.expenditure_amount.text().strip()
        category = self.ui.expenditure_category.currentText()

        if not all([date, description, amount, category]):
            QMessageBox.warning(
                self.expenditure_window, "Input Error", "All fields are mandatory."
            )
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(
                self.expenditure_window,
                "Input Error",
                "Amount must be a positive number.",
            )
            return

        result = ExpenditureAPI.update_expenditure(
            expenditure_id, description, amount, category, date
        )
        if result["success"]:
            QMessageBox.information(
                self.expenditure_window, "Success", result["message"]
            )
            self.handle_clear()
            self.load_expenditures()
            self.update_lcds()
        else:
            QMessageBox.warning(self.expenditure_window, "Error", result["error"])

    def handle_delete_expenditure(self):
        selected_row = self.ui.table_expenditure.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self.expenditure_window,
                "Selection Error",
                "Please select an expenditure to delete.",
            )
            return

        expenditure_id = int(self.ui.table_expenditure.item(selected_row, 0).text())
        reply = QMessageBox.question(
            self.expenditure_window,
            "Confirm Delete",
            "Are you sure you want to delete this expenditure?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            result = ExpenditureAPI.delete_expenditure(expenditure_id)
            if result["success"]:
                self.load_expenditures()
                self.update_lcds()
            else:
                QMessageBox.warning(self.expenditure_window, "Error", result["error"])

    def handle_clear(self):
        self.ui.expenditure_date.setDate(QtCore.QDate.currentDate())
        self.ui.expenditure_description.clear()
        self.ui.expenditure_amount.clear()
        self.ui.expenditure_category.setCurrentIndex(0)

    def filter_expenditures(self, search_term):
        result = ExpenditureAPI.filter_expenditures(search_term)
        if result["success"]:
            self.ui.table_expenditure.setRowCount(0)
            for row, exp in enumerate(result["expenditures"]):
                self.ui.table_expenditure.setRowCount(
                    self.ui.table_expenditure.rowCount() + 1
                )
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
                self.ui.table_expenditure.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(exp["category"])
                )

                delete_btn = QtWidgets.QPushButton()
                delete_btn.setObjectName("ExpenditureTableBtnDelete")
                delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                delete_btn.setToolTip("Delete")
                delete_btn.setFixedSize(30, 30)
                delete_btn.clicked.connect(
                    lambda checked, r=row: self.handle_table_delete(r)
                )
                self.ui.table_expenditure.setCellWidget(row, 5, delete_btn)
        else:
            QMessageBox.warning(self.expenditure_window, "Error", result["error"])

    def fill_form_from_selection(self):
        selected_row = self.ui.table_expenditure.currentRow()
        if selected_row != -1:
            self.ui.expenditure_date.setDate(
                QtCore.QDate.fromString(
                    self.ui.table_expenditure.item(selected_row, 1).text(), "yyyy-MM-dd"
                )
            )
            self.ui.expenditure_description.setText(
                self.ui.table_expenditure.item(selected_row, 2).text()
            )
            self.ui.expenditure_amount.setText(
                self.ui.table_expenditure.item(selected_row, 3).text()
            )
            self.ui.expenditure_category.setCurrentText(
                self.ui.table_expenditure.item(selected_row, 4).text()
            )

    def handle_table_delete(self, row):
        expenditure_id = int(self.ui.table_expenditure.item(row, 0).text())
        reply = QMessageBox.question(
            self.expenditure_window,
            "Confirm Delete",
            "Are you sure you want to delete this expenditure?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            result = ExpenditureAPI.delete_expenditure(expenditure_id)
            if result["success"]:
                self.load_expenditures()
                self.update_lcds()
            else:
                QMessageBox.warning(self.expenditure_window, "Error", result["error"])

    def update_lcds(self):
        result = ExpenditureAPI.get_all_expenditures()
        if result["success"]:
            summary = result["summary"]
            self.ui.lcdWeeklyExpenditures.display(summary["weekly_total"])
            self.ui.lcdMonthlyExpenditures.display(summary["monthly_total"])
            self.ui.lcdYearlyExpenditures.display(summary["yearly_total"])

    def show(self):
        self.expenditure_window.show()
