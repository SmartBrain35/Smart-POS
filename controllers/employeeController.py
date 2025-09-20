# controllers/employeesController.py
import logging
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QComboBox
from PySide6.QtCore import Qt

from backend.apis import EmployeeAPI

logger = logging.getLogger("EmployeesController")


class EmployeesController:
    def __init__(self, ui, page):
        self.ui = ui
        self.page = page
        self.current_employee_id = None

        logger.debug("EmployeesController initialized")

        # Connect signals
        self.ui.btn_add_employee.clicked.connect(self.handle_add_employee)
        self.ui.btn_clear_employee.clicked.connect(self.handle_clear_form)
        self.ui.filter_input.textChanged.connect(self.handle_filter)

        # Setup table behaviour
        self.ui.table_employees.cellDoubleClicked.connect(self.handle_cell_double_click)

        # Sorting control
        header = self.ui.table_employees.horizontalHeader()
        header.setSectionResizeMode(
            8, QtWidgets.QHeaderView.Fixed
        )  # Action column fixed
        header.resizeSection(8, 70)
        header.sectionClicked.connect(self.handle_sort)

        # Load employees at startup
        self.load_employees()

    # ------------------- CRUD -------------------

    def handle_add_employee(self):
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

        result = EmployeeAPI.create_employee(
            name=name,
            phone=phone,
            ghana_card=ghana_card,
            address=address,
            salary=salary,
            designation=designation,
        )

        if result["success"]:
            QMessageBox.information(self.page, "Success", "Employee added successfully")
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
        if result["success"]:
            self.populate_table(result["employees"])
        else:
            QMessageBox.warning(self.page, "Error", result["error"])

    def populate_table(self, employees: list[dict]):
        table = self.ui.table_employees
        table.clearContents()
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
            # Date Added (read-only)
            item_date = self._make_item(str(emp.get("created_at", "")))
            item_date.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(row_idx, 7, item_date)

            # === Action column (Delete only) ===
            action_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(action_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.setAlignment(QtCore.Qt.AlignCenter)

            btn_delete = QtWidgets.QPushButton()
            btn_delete.setObjectName(f"btnDeleteEmployee_{emp['id']}")
            btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            btn_delete.setIconSize(QtCore.QSize(19, 19))
            btn_delete.setFixedSize(20, 20)
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
            btn_delete.clicked.connect(lambda _, id=emp["id"]: self.delete_employee(id))

            layout.addWidget(btn_delete)
            table.setCellWidget(row_idx, 8, action_widget)

        # Default sort by ID ascending
        table.sortItems(0, Qt.AscendingOrder)

    def _make_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return item

    # ------------------- Row Interactions -------------------

    def handle_cell_double_click(self, row, col):
        """Allow inline editing with API update"""
        # Prevent editing ID (0), Date Added (7), and Action (8)
        if col in (0, 7, 8):
            return

        employee_id = int(self.ui.table_employees.item(row, 0).text())
        column_name = self.ui.table_employees.horizontalHeaderItem(col).text().lower()

        # Special case: designation -> use dropdown
        if column_name == "designation":
            combo = QComboBox()
            combo.addItems(["admin", "manager", "sales_rep"])
            current_val = self.ui.table_employees.item(row, col).text()
            combo.setCurrentText(current_val)

            self.ui.table_employees.setCellWidget(row, col, combo)

            def commit_combo():
                new_value = combo.currentText()
                result = EmployeeAPI.update_employee_field(
                    employee_id, "designation", new_value
                )
                if result["success"]:
                    QMessageBox.information(self.page, "Success", "Designation updated")
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
        if not ok or new_value.strip() == old_value:
            return

        result = EmployeeAPI.update_employee_field(
            employee_id, column_name.replace(" ", "_"), new_value.strip()
        )
        if result["success"]:
            QMessageBox.information(self.page, "Success", f"{column_name} updated")
            self.load_employees()
        else:
            QMessageBox.warning(self.page, "Error", result["error"])

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

    # ------------------- Sorting Control -------------------

    def handle_sort(self, logicalIndex):
        """Disable sorting on ID column"""
        if logicalIndex == 0:  # prevent sorting ID
            return
        self.ui.table_employees.sortItems(logicalIndex, Qt.AscendingOrder)
