from PySide6 import QMessageBox, QMainWindow, QtGui, QtCore, QtWidgets
from ui.account_ui import Ui_Account
from backend.apis import AccountAPI

class AccountController:
    def __init__(self, parent=None):
        self.parent = parent
        self.account_window = QMainWindow()
        self.ui = Ui_Account()
        self.ui.setupUi(self.account_window)
        
        # Connect UI signals to controller methods
        self.ui.btn_register.clicked.connect(self.handle_register)
        self.ui.btn_edit.clicked.connect(self.handle_edit)
        self.ui.btn_clear.clicked.connect(self.handle_clear)
        
        # Connect table action buttons
        self.connect_table_buttons()

        # Load initial data
        self.load_users()

    def connect_table_buttons(self):
        for row in range(self.ui.table_users.rowCount()):
            action_widget = self.ui.table_users.cellWidget(row, 5)
            if action_widget:
                for btn in action_widget.findChildren(QtWidgets.QPushButton):
                    if btn.objectName() == "tableBtnEdit":
                        btn.clicked.connect(lambda checked, r=row: self.handle_table_edit(r))
                    elif btn.objectName() == "tableBtnDelete":
                        btn.clicked.connect(lambda checked, r=row: self.handle_table_delete(r))

    def load_users(self):
        # Clear existing rows
        self.ui.table_users.setRowCount(0)
        
        # Fetch users from API
        users = AccountAPI.get_all_users()
        if users:
            self.ui.table_users.setRowCount(len(users))
            for row, user in enumerate(users):
                self.ui.table_users.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user.get("id", ""))))
                self.ui.table_users.setItem(row, 1, QtWidgets.QTableWidgetItem(user.get("name", "")))
                self.ui.table_users.setItem(row, 2, QtWidgets.QTableWidgetItem(user.get("phone", "")))
                self.ui.table_users.setItem(row, 3, QtWidgets.QTableWidgetItem(user.get("email", "")))
                self.ui.table_users.setItem(row, 4, QtWidgets.QTableWidgetItem(user.get("role", "")))

                # Action cell
                action_widget = QtWidgets.QWidget()
                action_layout = QtWidgets.QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 0, 0, 0)
                action_layout.setSpacing(15)

                btn_edit = QtWidgets.QPushButton()
                btn_edit.setObjectName("tableBtnEdit")
                btn_edit.setIcon(QtGui.QIcon("assets/icons/edit.png"))
                btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                btn_edit.setToolTip("Edit User")
                btn_edit.setFixedSize(30, 30)

                btn_delete = QtWidgets.QPushButton()
                btn_delete.setObjectName("tableBtnDelete")
                btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
                btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                btn_delete.setToolTip("Delete User")
                btn_delete.setFixedSize(30, 30)

                action_layout.addStretch()
                action_layout.addWidget(btn_edit)
                action_layout.addWidget(btn_delete)
                action_layout.addStretch()

                self.ui.table_users.setCellWidget(row, 5, action_widget)
                self.connect_table_buttons()  # Reconnect signals for new rows

    def handle_register(self):
        name = self.ui.input_name.text().strip()
        phone = self.ui.input_phone.text().strip()
        email = self.ui.input_email.text().strip()
        password = self.ui.input_password.text().strip()
        role = self.ui.input_role.currentText()

        if not all([name, phone, email, password, role]):
            QMessageBox.warning(self.account_window, "Input Error", "All fields are required.")
            return

        result = AccountAPI.create_user(name, phone, email, password, role)
        if result["success"]:
            QMessageBox.information(self.account_window, "Success", "User registered successfully.")
            self.clear_fields()
            self.load_users()
        else:
            QMessageBox.warning(self.account_window, "Error", result["error"])

    def handle_edit(self):
        selected_row = self.ui.table_users.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self.account_window, "Selection Error", "Please select a user to edit.")
            return

        name = self.ui.input_name.text().strip()
        phone = self.ui.input_phone.text().strip()
        email = self.ui.input_email.text().strip()
        password = self.ui.input_password.text().strip()
        role = self.ui.input_role.currentText()
        user_id = int(self.ui.table_users.item(selected_row, 0).text())

        if not all([name, phone, email, role]):
            QMessageBox.warning(self.account_window, "Input Error", "All fields except password are required.")
            return

        result = AccountAPI.update_user(user_id, name, phone, email, password if password else None, role)
        if result["success"]:
            QMessageBox.information(self.account_window, "Success", "User updated successfully.")
            self.clear_fields()
            self.load_users()
        else:
            QMessageBox.warning(self.account_window, "Error", result["error"])

    def handle_clear(self):
        self.clear_fields()

    def handle_table_edit(self, row):
        user_id = int(self.ui.table_users.item(row, 0).text())
        user = AccountAPI.get_user_by_id(user_id)
        if user:
            self.ui.input_name.setText(user.get("name", ""))
            self.ui.input_phone.setText(user.get("phone", ""))
            self.ui.input_email.setText(user.get("email", ""))
            self.ui.input_password.clear()
            self.ui.input_role.setCurrentText(user.get("role", "Admin"))

    def handle_table_delete(self, row):
        user_id = int(self.ui.table_users.item(row, 0).text())
        reply = QMessageBox.question(self.account_window, "Confirm Delete", "Are you sure you want to delete this user?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            result = AccountAPI.delete_user(user_id)
            if result["success"]:
                self.load_users()
            else:
                QMessageBox.warning(self.account_window, "Error", result["error"])

    def clear_fields(self):
        self.ui.input_name.clear()
        self.ui.input_phone.clear()
        self.ui.input_email.clear()
        self.ui.input_password.clear()
        self.ui.input_role.setCurrentIndex(0)

    def show(self):
        self.account_window.show()
