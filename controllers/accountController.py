import logging
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import (
    QMessageBox,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt
from backend.apis import AccountAPI

logger = logging.getLogger("AccountController")


class AccountController:
    def __init__(self, ui, page):
        self.ui = ui
        self.page = page
        logger.debug("AccountController __init__ called")

        # Connect signals (only once)
        self.ui.btn_register.clicked.connect(self.handle_register)
        self.ui.btn_edit.clicked.connect(self.handle_edit)
        self.ui.btn_clear.clicked.connect(self.handle_clear)
        self.ui.table_users.cellDoubleClicked.connect(self.handle_row_double_click)

        # Internal state
        self.current_edit_id = None

        # Table style improvements
        self.ui.table_users.setStyleSheet(
            """
            QTableWidget {
                gridline-color: #cccccc; /* softer gridlines */
            }
        """
        )

        logger.debug("Starting background thread to load users")
        self.load_users()
        logger.debug("AccountController instantiated successfully")

    # ------------------- CRUD -------------------

    def handle_register(self):
        logger.debug("handle_register called")

        name = self.ui.input_name.text().strip()
        phone = self.ui.input_phone.text().strip()
        email = self.ui.input_email.text().strip()
        password = self.ui.input_password.text().strip()
        role = self.ui.input_role.currentText().lower().replace(" ", "_")

        if not all([name, phone, email, password, role]):
            QMessageBox.warning(
                self.page, "Validation Error", "All fields are required."
            )
            return

        result = AccountAPI.create_account(name, phone, email, password, role)
        if result["success"]:
            QMessageBox.information(
                self.page, "Success", "Account created successfully"
            )
            self.load_users()
            self.handle_clear()
        else:
            QMessageBox.warning(self.page, "Error", result["error"])

    def handle_edit(self):
        logger.debug("handle_edit called")

        if not self.current_edit_id:
            QMessageBox.warning(self.page, "Error", "No account selected for editing.")
            return

        name = self.ui.input_name.text().strip()
        phone = self.ui.input_phone.text().strip()
        email = self.ui.input_email.text().strip()
        password = self.ui.input_password.text().strip()
        role = self.ui.input_role.currentText().lower().replace(" ", "_")

        result = AccountAPI.update_account(
            self.current_edit_id, name, phone, email, password, role
        )
        if result["success"]:
            QMessageBox.information(
                self.page, "Success", "Account updated successfully"
            )
            self.load_users()
            self.handle_clear()
        else:
            QMessageBox.warning(self.page, "Error", result["error"])

    def handle_clear(self):
        logger.debug("handle_clear called")

        self.ui.input_name.clear()
        self.ui.input_phone.clear()
        self.ui.input_email.clear()
        self.ui.input_password.clear()
        self.ui.input_role.setCurrentIndex(0)
        self.current_edit_id = None

    # ------------------- Table Logic -------------------

    def load_users(self):
        result = AccountAPI.get_all_accounts()
        if not result["success"]:
            QMessageBox.warning(self.page, "Error", result["error"])
            return

        accounts = result["accounts"]
        logger.debug(f"Fetched users: {accounts}")

        table = self.ui.table_users
        table.setRowCount(0)

        for row_idx, acc in enumerate(accounts):
            table.insertRow(row_idx)
            table.setItem(row_idx, 0, self._make_item(str(acc["id"])))
            table.setItem(row_idx, 1, self._make_item(acc["name"]))
            table.setItem(row_idx, 2, self._make_item(acc["phone"]))
            table.setItem(row_idx, 3, self._make_item(acc["email"]))
            table.setItem(row_idx, 4, self._make_item(acc["role"]))

            # --- Action column (edit + delete buttons) ---
            action_widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(action_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(12)

            btn_edit = QtWidgets.QPushButton()
            btn_edit.setIcon(QtGui.QIcon("assets/icons/edit.png"))
            btn_edit.setIconSize(QtCore.QSize(24, 24))
            btn_edit.setFixedSize(32, 32)
            btn_edit.setStyleSheet("border: none; background: transparent;")
            btn_edit.clicked.connect(lambda _, id=acc["id"]: self.fill_edit_form(id))

            btn_delete = QtWidgets.QPushButton()
            btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            btn_delete.setIconSize(QtCore.QSize(24, 24))
            btn_delete.setFixedSize(32, 32)
            btn_delete.setStyleSheet("border: none; background: transparent;")
            btn_delete.clicked.connect(lambda _, id=acc["id"]: self.delete_account(id))

            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)
            layout.setAlignment(Qt.AlignCenter)

            table.setCellWidget(row_idx, 5, action_widget)

    def _make_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return item

    # ------------------- Row Interactions -------------------

    def fill_edit_form(self, account_id):
        result = AccountAPI.get_account_by_id(account_id)
        if not result["success"]:
            QMessageBox.warning(self.page, "Error", result["error"])
            return

        acc = result["account"]
        self.ui.input_name.setText(acc["name"])
        self.ui.input_phone.setText(acc["phone"])
        self.ui.input_email.setText(acc["email"])
        self.ui.input_role.setCurrentText(acc["role"].capitalize())
        self.current_edit_id = acc["id"]

    def handle_row_double_click(self, row, col):
        account_id = int(self.ui.table_users.item(row, 0).text())
        self.fill_edit_form(account_id)

    def delete_account(self, account_id):
        confirm = QMessageBox.question(
            self.page,
            "Confirm Delete",
            "Are you sure you want to delete this account?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirm != QMessageBox.Yes:
            return

        result = AccountAPI.delete_account(account_id)
        if result["success"]:
            QMessageBox.information(self.page, "Deleted", result["message"])
            self.load_users()
        else:
            QMessageBox.warning(self.page, "Error", result["error"])
