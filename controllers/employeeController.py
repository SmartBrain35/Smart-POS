from PySide6.QtWidgets import QtCore, QtGui, QtWidgets, QMessageBox, QMainWindow
from ui.employees_ui import Ui_Employees
from backend.apis import EmployeeAPI
from datetime import datetime

class EmployeeController:
    def __init__(self, parent=None):
        self.parent = parent
        self.employee_window = QMainWindow()
        self.ui = Ui_Employees()
        self.ui.setupUi(self.employee_window)

        # Connect UI signals to controller methods
        self.ui.btn_add_employee.clicked.connect(self.handle_add_employee)
        self.ui.btn_clear_employee.clicked.connect(self.handle_clear)
        self.ui.filter_input.textChanged.connect(self.filter_employees)
        self.ui.table_employees.doubleClicked.connect(self.handle_table_edit)

        # Load initial data
        self.load_employees()

    def load_employees(self):
        # Clear existing rows
        self.ui.table_employees.setRowCount(0)

        # Fetch employees from API
        result = EmployeeAPI.get_all_employees()
        if result["success"]:
            self.ui.table_employees.setRowCount(len(result["employees"]))
            for row, emp in enumerate(result["employees"]):
                self.ui.table_employees.setItem(row, 0, QtWidgets.QTableWidgetItem(str(emp.get("id", ""))))
                self.ui.table_employees.setItem(row, 1, QtWidgets.QTableWidgetItem(emp.get("name", "")))
                self.ui.table_employees.setItem(row, 2, QtWidgets.QTableWidgetItem(emp.get("phone", "")))
                self.ui.table_employees.setItem(row, 3, QtWidgets.QTableWidgetItem(emp.get("ghana_card", "")))
                self.ui.table_employees.setItem(row, 4, QtWidgets.QTableWidgetItem(emp.get("address", "")))
                self.ui.table_employees.setItem(row, 5, QtWidgets.QTableWidgetItem(emp.get("designation", "")))
                self.ui.table_employees.setItem(row, 6, QtWidgets.QTableWidgetItem(str(emp.get("salary", ""))))
                self.ui.table_employees.setItem(row, 7, QtWidgets.QTableWidgetItem(emp.get("created_at", "").split("T")[0] if emp.get("created_at") else ""))
                # No delete button as per requirement
        else:
            QMessageBox.warning(self.employee_window, "Error", result["error"])

    def handle_add_employee(self):
        name = self.ui.emp_name.text().strip()
        phone = self.ui.emp_phone.text().strip()
        ghana_card = self.ui.emp_card.text().strip()
        address = self.ui.emp_address.text().strip() if self.ui.emp_address.text().strip() else None
        salary = self.ui.emp_salary.text().strip() if self.ui.emp_salary.text().strip() else None
        designation = self.ui.emp_designation.currentText()

        # Validate compulsory fields
        if not all([name, phone, ghana_card]):
            QMessageBox.warning(self.employee_window, "Input Error", "Name, Phone, and Ghana Card ID are compulsory.")
            return

        # Basic input validation
        if not self.is_valid_phone(phone):
            QMessageBox.warning(self.employee_window, "Input Error", "Please enter a valid phone number (e.g., 10 digits).")
            return
        if not self.is_valid_ghana_card(ghana_card):
            QMessageBox.warning(self.employee_window, "Input Error", "Please enter a valid Ghana Card ID (e.g., GHA-XXXXXXXXX).")
            return
        if salary and not self.is_valid_salary(salary):
            QMessageBox.warning(self.employee_window, "Input Error", "Please enter a valid salary (numeric value).")
            return

        result = EmployeeAPI.create_employee(name, phone, ghana_card, address, float(salary) if salary else None, designation)
        if result["success"]:
            QMessageBox.information(self.employee_window, "Success", "Employee added successfully.")
            self.handle_clear()
            self.load_employees()
        else:
            QMessageBox.warning(self.employee_window, "Error", result["error"])

    def handle_clear(self):
        self.ui.emp_name.clear()
        self.ui.emp_phone.clear()
        self.ui.emp_card.clear()
        self.ui.emp_address.clear()
        self.ui.emp_salary.clear()
        self.ui.emp_designation.setCurrentIndex(0)

    def filter_employees(self, search_term):
        result = EmployeeAPI.filter_employees(search_term)
        if result["success"]:
            self.ui.table_employees.setRowCount(0)
            for row, emp in enumerate(result["employees"]):
                self.ui.table_employees.setRowCount(self.ui.table_employees.rowCount() + 1)
                self.ui.table_employees.setItem(row, 0, QtWidgets.QTableWidgetItem(str(emp.get("id", ""))))
                self.ui.table_employees.setItem(row, 1, QtWidgets.QTableWidgetItem(emp.get("name", "")))
                self.ui.table_employees.setItem(row, 2, QtWidgets.QTableWidgetItem(emp.get("phone", "")))
                self.ui.table_employees.setItem(row, 3, QtWidgets.QTableWidgetItem(emp.get("ghana_card", "")))
                self.ui.table_employees.setItem(row, 4, QtWidgets.QTableWidgetItem(emp.get("address", "")))
                self.ui.table_employees.setItem(row, 5, QtWidgets.QTableWidgetItem(emp.get("designation", "")))
                self.ui.table_employees.setItem(row, 6, QtWidgets.QTableWidgetItem(str(emp.get("salary", ""))))
                self.ui.table_employees.setItem(row, 7, QtWidgets.QTableWidgetItem(emp.get("created_at", "").split("T")[0] if emp.get("created_at") else ""))
                # No action column
        else:
            QMessageBox.warning(self.employee_window, "Error", result["error"])

    def handle_table_edit(self, index):
        row = index.row()
        col = index.column()
        if 0 <= col < 8:  # Exclude Action column if it existed
            current_value = self.ui.table_employees.item(row, col).text()
            field_map = ["id", "name", "phone", "ghana_card", "address", "designation", "salary", "date_added"]
            field = field_map[col]

            # Open a dialog for editing
            text, ok = QtWidgets.QInputDialog.getText(
                self.employee_window,
                f"Edit {field.replace('_', ' ').title()}",
                f"Enter new {field.replace('_', ' ').title()}:",
                QtWidgets.QLineEdit.Normal,
                current_value
            )
            if ok and text:
                employee_id = int(self.ui.table_employees.item(row, 0).text())
                result = EmployeeAPI.update_employee_field(employee_id, field, text)
                if result["success"]:
                    self.load_employees()
                else:
                    QMessageBox.warning(self.employee_window, "Error", result["error"])

    def is_valid_phone(self, phone):
        # Simple validation for Ghana phone numbers (e.g., 10 digits starting with 0 or +233)
        import re
        phone_pattern = r'^\+?233\d{9}$|^0\d{9}$'
        return re.match(phone_pattern, phone) is not None

    def is_valid_ghana_card(self, ghana_card):
        # Simple validation for Ghana Card ID (e.g., GHA- followed by 9 digits)
        import re
        ghana_card_pattern = r'^GHA-\d{9}$'
        return re.match(ghana_card_pattern, ghana_card) is not None

    def is_valid_salary(self, salary):
        try:
            float(salary)
            return True
        except ValueError:
            return False

    def show(self):
        self.employee_window.show()