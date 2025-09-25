# controllers/employeesController.py
import logging
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QComboBox
from PySide6.QtCore import Qt, QSize

from backend.apis import EmployeeAPI

logger = logging.getLogger("EmployeesController")


class EmployeesController:
    HEADERS = [
        "ID",
        "Name",
        "Phone",
        "Ghana Card",
        "Address",
        "Designation",
        "Salary",
        "Created At",
        "Action",
    ]

    def __init__(self, ui, page):
        self.ui = ui
        self.page = page
        self.current_employee_id = None

        logger.debug("EmployeesController initialized")

        # Configure table
        self.setup_table()

        # Connect signals
        self.ui.btn_add_employee.clicked.connect(self.handle_add_or_update)
        self.ui.btn_clear_employee.clicked.connect(self.handle_clear_form)
        self.ui.filter_input.textChanged.connect(self.handle_filter)
        self.ui.table_employees.cellDoubleClicked.connect(self.handle_cell_double_click)

        # Load employees
        self.load_employees()

    # ------------------- Table Setup -------------------

    def setup_table(self):
        table = self.ui.table_employees
        table.setColumnCount(len(self.HEADERS))
        table.setHorizontalHeaderLabels(self.HEADERS)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        table.verticalHeader().setVisible(False)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(len(self.HEADERS) - 1, QtWidgets.QHeaderView.Fixed)
        header.resizeSection(len(self.HEADERS) - 1, 70)

    # ------------------- CRUD -------------------

    def handle_add_or_update(self):
        name = self.ui.emp_name.text().strip()
        phone = self.ui.emp_phone.text().strip()
        ghana_card = self.ui.emp_card.text().strip()
        address = self.ui.emp_address.text().strip()
        designation = self.ui.emp_designation.currentText().lower().replace(" ", "_")
        salary_text = self.ui.emp_salary.text().strip()
        salary = float(salary_text) if salary_text else None

        if not all([name, phone, ghana_card]):
            QMessageBox.warning(
                self.page,
                "Validation Error",
                "Name, Phone and Ghana Card ID are required.",
            )
            return

        if self.current_employee_id:  # Update existing
            result = EmployeeAPI.update_employee(
                self.current_employee_id,
                name=name,
                phone=phone,
                ghana_card=ghana_card,
                address=address,
                salary=salary,
                designation=designation,
            )
            if result["success"]:
                QMessageBox.information(
                    self.page, "Updated", "Employee updated successfully"
                )
                self.load_employees()
                self.handle_clear_form()
            else:
                QMessageBox.warning(self.page, "Error", result["error"])
        else:  # Create new
            result = EmployeeAPI.create_employee(
                name=name,
                phone=phone,
                ghana_card=ghana_card,
                address=address,
                salary=salary,
                designation=designation,
            )
            if result["success"]:
                QMessageBox.information(
                    self.page, "Success", "Employee added successfully"
                )
                self.load_employees()
                self.handle_clear_form()
            else:
                QMessageBox.warning(self.page, "Error", result["error"])

    def handle_clear_form(self):
        self.ui.emp_name.clear()
        self.ui.emp_phone.clear()
        self.ui.emp_card.clear()
        self.ui.emp_address.clear()
        self.ui.emp_salary.clear()
        self.ui.emp_designation.setCurrentIndex(0)
        self.current_employee_id = None
        self.ui.btn_add_employee.setText("Add Employee")

    def handle_filter(self, text: str):
        text = text.strip()
        if not text:
            self.load_employees()
            return

        result = EmployeeAPI.filter_employees(text)
        if result["success"]:
            self.populate_table(result["employees"])
        else:
            QMessageBox.warning(self.page, "Error", result["error"])

    # ------------------- Table Logic -------------------

    def load_employees(self):
        result = EmployeeAPI.get_all_employees()
        logger.debug(f"Employees API result: {result}")
        if result["success"]:
            self.populate_table(result["employees"])
        else:
            QMessageBox.warning(self.page, "Error", result["error"])

    def populate_table(self, employees: list[dict]):
        table = self.ui.table_employees
        table.setRowCount(0)

        for row_idx, emp in enumerate(employees):
            table.insertRow(row_idx)
            table.setItem(row_idx, 0, self._make_item(str(emp["id"])))
            table.setItem(row_idx, 1, self._make_item(emp["name"]))
            table.setItem(row_idx, 2, self._make_item(emp["phone"]))
            table.setItem(row_idx, 3, self._make_item(emp["ghana_card"]))
            table.setItem(row_idx, 4, self._make_item(emp.get("address") or ""))
            table.setItem(row_idx, 5, self._make_item(emp["designation"]))
            table.setItem(row_idx, 6, self._make_item(str(emp.get("salary") or "")))
            table.setItem(row_idx, 7, self._make_item(str(emp.get("created_at", ""))))

            # Action column (Delete button)
            btn_delete = QtWidgets.QPushButton()
            btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            btn_delete.setIconSize(QSize(18, 18))
            btn_delete.setFixedSize(24, 24)
            btn_delete.setStyleSheet(
                "QPushButton { border: none; background: transparent; }"
            )
            btn_delete.clicked.connect(lambda _, id=emp["id"]: self.delete_employee(id))
            action_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(action_widget)
            layout.addWidget(btn_delete, alignment=Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(row_idx, 8, action_widget)

        table.resizeRowsToContents()

    def _make_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return item

    # ------------------- Row Interactions -------------------

    def handle_cell_double_click(self, row, col):
        """Dual behavior:
        - If clicking ID/Created/Action → ignore
        - If clicking editable cell → inline edit
        - If clicking row (col 1–6) → load form for editing
        """
        if col in (0, 7, 8):  # non-editable columns
            return

        employee_id = int(self.ui.table_employees.item(row, 0).text())
        column_name = (
            self.ui.table_employees.horizontalHeaderItem(col)
            .text()
            .lower()
            .replace(" ", "_")
        )

        # === Option 1: Inline edit in table ===
        if column_name == "designation":  # dropdown
            combo = QComboBox()
            combo.addItems(["admin", "manager", "sales_rep"])
            current_val = self.ui.table_employees.item(row, col).text()
            combo.setCurrentText(current_val)
            self.ui.table_employees.setCellWidget(row, col, combo)

            def commit_combo():
                new_val = combo.currentText()
                result = EmployeeAPI.update_employee_field(
                    employee_id, "designation", new_val
                )
                if result["success"]:
                    QMessageBox.information(
                        self.page, "Updated", "Designation updated successfully"
                    )
                    self.load_employees()
                else:
                    QMessageBox.warning(self.page, "Error", result["error"])

            combo.currentIndexChanged.connect(commit_combo)
            return

        old_value = self.ui.table_employees.item(row, col).text()
        new_value, ok = QtWidgets.QInputDialog.getText(
            self.page,
            "Edit Field",
            f"Enter new value for {column_name}:",
            text=old_value,
        )
        if ok and new_value.strip() != old_value:
            result = EmployeeAPI.update_employee_field(
                employee_id, column_name, new_value.strip()
            )
            if result["success"]:
                QMessageBox.information(self.page, "Updated", f"{column_name} updated")
                self.load_employees()
            else:
                QMessageBox.warning(self.page, "Error", result["error"])
            return

        # === Option 2: Load full row into form for editing ===
        self.current_employee_id = employee_id
        self.ui.btn_add_employee.setText("Update Employee")
        self.ui.emp_name.setText(self.ui.table_employees.item(row, 1).text())
        self.ui.emp_phone.setText(self.ui.table_employees.item(row, 2).text())
        self.ui.emp_card.setText(self.ui.table_employees.item(row, 3).text())
        self.ui.emp_address.setText(self.ui.table_employees.item(row, 4).text())
        self.ui.emp_designation.setCurrentText(
            self.ui.table_employees.item(row, 5).text()
        )
        self.ui.emp_salary.setText(self.ui.table_employees.item(row, 6).text())

    def delete_employee(self, employee_id):
        confirm = QMessageBox.question(
            self.page,
            "Delete Employee",
            "Are you sure you want to delete this employee?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        result = EmployeeAPI.delete_employee(employee_id)
        if result["success"]:
            QMessageBox.information(self.page, "Deleted", result["message"])
            self.load_employees()
        else:
            QMessageBox.warning(self.page, "Error", result["error"])
