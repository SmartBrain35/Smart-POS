import logging
import re
import threading
import functools

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

from ui.account_ui import Ui_Account
from backend.apis import AccountAPI

# Configure module logger
logger = logging.getLogger("AccountController")
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(ch)


class AccountController:
    def __init__(self, parent=None):
        self.parent = parent
        self.account_window = QtWidgets.QMainWindow()
        self.ui = Ui_Account()
        self.ui.setupUi(self.account_window)

        # Connect UI signals
        self.ui.btn_register.clicked.connect(self.handle_register)
        self.ui.btn_edit.clicked.connect(self.handle_edit)
        self.ui.btn_clear.clicked.connect(self.handle_clear)

        # Improve table behavior
        self.ui.table_users.setSortingEnabled(False)
        self.ui.table_users.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.ui.table_users.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.table_users.cellDoubleClicked.connect(self._on_table_double_clicked)

        # Load users asynchronously
        self.load_users_async()

    def normalize_user(self, user):
        """
        Normalize a user row to a dict with keys: id, name, phone, email, role.
        """
        if user is None:
            return {"id": "", "name": "", "phone": "", "email": "", "role": ""}

        try:
            if isinstance(user, dict):
                return {
                    "id": user.get("id", ""),
                    "name": user.get("name", ""),
                    "phone": user.get("phone", ""),
                    "email": user.get("email", ""),
                    "role": user.get("role", "").capitalize(),
                }
        except Exception:
            pass

        for attr in ("id", "pk", "user_id"):
            if hasattr(user, attr):
                return {
                    "id": getattr(user, attr),
                    "name": getattr(user, "name", getattr(user, "full_name", "")),
                    "phone": getattr(user, "phone", ""),
                    "email": getattr(user, "email", ""),
                    "role": getattr(user, "role", "").capitalize(),
                }

        try:
            if isinstance(user, (list, tuple)):
                u0 = user + ("",) * (5 - len(user))
                return {
                    "id": u0[0],
                    "name": u0[1],
                    "phone": u0[2],
                    "email": u0[3],
                    "role": u0[4].capitalize(),
                }
        except Exception:
            pass

        return {
            "id": str(user),
            "name": str(user),
            "phone": "",
            "email": "",
            "role": "",
        }

    def load_users_async(self):
        """Start background thread to fetch users and populate table on completion."""
        logger.debug("Starting background thread to load users")
        t = threading.Thread(target=self._fetch_users_worker, daemon=True)
        t.start()

    def _fetch_users_worker(self):
        """Runs in background thread: call API and then schedule UI update."""
        try:
            result = AccountAPI.get_all_accounts()
            logger.debug("Fetched accounts: %s", result)
            accounts = result.get("accounts", []) if result.get("success") else []
        except Exception as e:
            logger.exception("Error fetching accounts: %s", e)
            accounts = []
        QtCore.QTimer.singleShot(
            0, functools.partial(self.populate_users_table, accounts)
        )

    def populate_users_table(self, accounts):
        """
        Populate the QTableWidget. This runs on the main GUI thread.
        """
        try:
            self.ui.table_users.setUpdatesEnabled(False)
            self.ui.table_users.blockSignals(True)

            self.ui.table_users.setRowCount(0)
            if not accounts:
                logger.debug("No accounts to populate")
                return

            normalized = [self.normalize_user(acc) for acc in accounts]
            self.ui.table_users.setRowCount(len(normalized))

            for row, user in enumerate(normalized):
                uid = str(user.get("id", ""))
                name = user.get("name", "") or ""
                phone = user.get("phone", "") or ""
                email = user.get("email", "") or ""
                role = user.get("role", "") or ""

                self.ui.table_users.setItem(row, 0, QtWidgets.QTableWidgetItem(uid))
                self.ui.table_users.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
                self.ui.table_users.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
                self.ui.table_users.setItem(row, 3, QtWidgets.QTableWidgetItem(email))
                self.ui.table_users.setItem(row, 4, QtWidgets.QTableWidgetItem(role))

                action_widget = QtWidgets.QWidget()
                action_layout = QtWidgets.QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(8)

                btn_edit = QtWidgets.QPushButton()
                btn_edit.setObjectName("tableBtnEdit")
                btn_edit.setFixedSize(28, 28)
                try:
                    btn_edit.setIcon(QtGui.QIcon("assets/icons/edit.png"))
                except Exception as e:
                    logger.warning("Failed to load edit icon: %s", e)

                btn_delete = QtWidgets.QPushButton()
                btn_delete.setObjectName("tableBtnDelete")
                btn_delete.setFixedSize(28, 28)
                try:
                    btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                except Exception as e:
                    logger.warning("Failed to load delete icon: %s", e)

                btn_edit.clicked.connect(
                    functools.partial(self.handle_table_edit_by_id, uid)
                )
                btn_delete.clicked.connect(
                    functools.partial(self.handle_table_delete_by_id, uid)
                )

                action_layout.addStretch()
                action_layout.addWidget(btn_edit)
                action_layout.addWidget(btn_delete)
                action_layout.addStretch()

                self.ui.table_users.setCellWidget(row, 5, action_widget)

            self.ui.table_users.resizeColumnsToContents()
            logger.debug("Populated table with %d rows", len(normalized))

        except Exception as e:
            logger.exception("Error populating users table: %s", e)
            QtWidgets.QMessageBox.warning(
                self.account_window, "Error", f"Failed to load users: {e}"
            )
        finally:
            self.ui.table_users.blockSignals(False)
            self.ui.table_users.setUpdatesEnabled(True)

    def handle_register(self):
        logger.debug("Register button clicked")
        name = self.ui.input_name.text().strip()
        phone = self.ui.input_phone.text().strip()
        email = self.ui.input_email.text().strip()
        password = self.ui.input_password.text().strip()
        role = self.ui.input_role.currentText()

        if not all([name, phone, email, password, role]):
            QtWidgets.QMessageBox.warning(
                self.account_window,
                "Input Error",
                "All fields (Name, Phone, Email, Password, Role) are required.",
            )
            return

        if not self.is_valid_email(email):
            QtWidgets.QMessageBox.warning(
                self.account_window,
                "Input Error",
                "Please enter a valid email address.",
            )
            return

        if not self.is_valid_phone(phone):
            QtWidgets.QMessageBox.warning(
                self.account_window, "Input Error", "Please enter a valid phone number."
            )
            return

        def _create():
            try:
                result = AccountAPI.create_account(
                    name, phone, email, password, role.lower()
                )
                logger.debug("Create account result: %s", result)
            except Exception as e:
                logger.exception("Create account failed: %s", e)
                result = {"success": False, "error": str(e)}
            QtCore.QTimer.singleShot(
                0, functools.partial(self._after_create_account, result)
            )

        threading.Thread(target=_create, daemon=True).start()

    def _after_create_account(self, result):
        if result.get("success"):
            QtWidgets.QMessageBox.information(
                self.account_window, "Success", "User registered successfully."
            )
            self.clear_fields()
            self.load_users_async()
        else:
            err = result.get("error", "Unknown error")
            QtWidgets.QMessageBox.warning(self.account_window, "Error", str(err))

    def handle_edit(self):
        logger.debug("Edit button clicked")
        selected_row = self.ui.table_users.currentRow()
        if selected_row == -1:
            QtWidgets.QMessageBox.warning(
                self.account_window, "Selection Error", "Please select a user to edit."
            )
            return

        try:
            user_id_item = self.ui.table_users.item(selected_row, 0)
            if user_id_item is None:
                raise ValueError("Selected row has no ID")
            user_id = int(user_id_item.text())
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self.account_window, "Error", f"Invalid selection: {e}"
            )
            return

        name = self.ui.input_name.text().strip()
        phone = self.ui.input_phone.text().strip()
        email = self.ui.input_email.text().strip()
        password = self.ui.input_password.text().strip()
        role = self.ui.input_role.currentText()

        if not all([name, phone, email, role]):
            QtWidgets.QMessageBox.warning(
                self.account_window,
                "Input Error",
                "All fields (Name, Phone, Email, Role) are required.",
            )
            return

        if not self.is_valid_email(email):
            QtWidgets.QMessageBox.warning(
                self.account_window,
                "Input Error",
                "Please enter a valid email address.",
            )
            return

        if not self.is_valid_phone(phone):
            QtWidgets.QMessageBox.warning(
                self.account_window, "Input Error", "Please enter a valid phone number."
            )
            return

        def _update():
            try:
                result = AccountAPI.update_account(
                    user_id,
                    name,
                    phone,
                    email,
                    password if password else None,
                    role.lower(),
                )
                logger.debug("Update account result: %s", result)
            except Exception as e:
                logger.exception("Update account failed: %s", e)
                result = {"success": False, "error": str(e)}
            QtCore.QTimer.singleShot(
                0, functools.partial(self._after_update_account, result)
            )

        threading.Thread(target=_update, daemon=True).start()

    def _after_update_account(self, result):
        if result.get("success"):
            QtWidgets.QMessageBox.information(
                self.account_window, "Success", "User updated successfully."
            )
            self.clear_fields()
            self.load_users_async()
        else:
            QtWidgets.QMessageBox.warning(
                self.account_window, "Error", result.get("error", "Unknown error")
            )

    def handle_clear(self):
        logger.debug("Clear button clicked")
        self.clear_fields()

    def handle_table_edit_by_id(self, user_id):
        logger.debug("Table edit button clicked for user_id: %s", user_id)
        try:
            result = AccountAPI.get_user_by_id(user_id)
            logger.debug("Get user by ID result: %s", result)
            if not result.get("success"):
                raise ValueError(result.get("error", "Failed to load user"))
            user = self.normalize_user(result.get("account"))
            self.ui.input_name.setText(user.get("name", ""))
            self.ui.input_phone.setText(user.get("phone", ""))
            self.ui.input_email.setText(user.get("email", ""))
            self.ui.input_password.clear()
            role = user.get("role", "") or ""
            idx = self.ui.input_role.findText(role)
            if idx >= 0:
                self.ui.input_role.setCurrentIndex(idx)
            else:
                self.ui.input_role.setCurrentIndex(0)
            self._select_row_by_user_id(user_id)
        except Exception as e:
            logger.exception("Error loading user for edit: %s", e)
            QtWidgets.QMessageBox.warning(
                self.account_window, "Error", f"Failed to load user: {e}"
            )

    def handle_table_delete_by_id(self, user_id):
        logger.debug("Table delete button clicked for user_id: %s", user_id)
        reply = QtWidgets.QMessageBox.question(
            self.account_window,
            "Confirm Delete",
            "Are you sure you want to delete this user?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return

        def _delete():
            try:
                result = AccountAPI.delete_account(user_id)
                logger.debug("Delete account result: %s", result)
            except Exception as e:
                logger.exception("Delete account failed: %s", e)
                result = {"success": False, "error": str(e)}
            QtCore.QTimer.singleShot(
                0, functools.partial(self._after_delete_account, result)
            )

        threading.Thread(target=_delete, daemon=True).start()

    def _after_delete_account(self, result):
        if result.get("success"):
            QtWidgets.QMessageBox.information(
                self.account_window, "Success", "User deleted successfully."
            )
            self.load_users_async()
        else:
            QtWidgets.QMessageBox.warning(
                self.account_window, "Error", result.get("error", "Unknown error")
            )

    def clear_fields(self):
        self.ui.input_name.clear()
        self.ui.input_phone.clear()
        self.ui.input_email.clear()
        self.ui.input_password.clear()
        self.ui.input_role.setCurrentIndex(0)

    def _select_row_by_user_id(self, user_id):
        for r in range(self.ui.table_users.rowCount()):
            item = self.ui.table_users.item(r, 0)
            if item and str(item.text()) == str(user_id):
                self.ui.table_users.selectRow(r)
                return

    def _on_table_double_clicked(self, row, col):
        try:
            item = self.ui.table_users.item(row, 0)
            if not item:
                return
            uid = item.text()
            try:
                uid_val = int(uid)
            except Exception:
                uid_val = uid
            self.handle_table_edit_by_id(uid_val)
        except Exception as e:
            logger.exception("Error on table double click: %s", e)

    def is_valid_email(self, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email) is not None

    def is_valid_phone(self, phone):
        phone_pattern = r"^\+?\d{7,15}$"
        return re.match(phone_pattern, phone) is not None

    def show(self):
        self.account_window.show()
