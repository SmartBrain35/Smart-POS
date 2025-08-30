# controllers/login.py
from PySide6.QtWidgets import QMessageBox, QMainWindow
from ui.login_window import LoginWindow
from ui.dashboard import Ui_AdminDashboard


class LoginController:
    def __init__(self):
        # Create login view
        self.login_view = LoginWindow()
        self.login_view.login_button.clicked.connect(self.handle_login)

        self.dashboard_window = None

    def handle_login(self):
        username = self.login_view.username_input.text().strip()
        password = self.login_view.password_input.text().strip()

        if username == "admin" and password == "1234":
            QMessageBox.information(self.login_view, "Login Success", "Welcome!")

            # Create dashboard window properly
            self.dashboard_window = QMainWindow()
            self.ui = Ui_AdminDashboard()
            self.ui.setupUi(self.dashboard_window)

            self.dashboard_window.show()
            self.login_view.close()
        else:
            QMessageBox.warning(self.login_view, "Login Failed", "Invalid credentials")



