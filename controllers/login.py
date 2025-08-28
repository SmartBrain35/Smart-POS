# controllers/login.py
from PySide6.QtWidgets import QMessageBox
from ui.admin_dashboard import AdminDashboard


class LoginController:
    def __init__(self, login_view):
        self.login_view = login_view
        self.login_view.login_button.clicked.connect(self.handle_login)

        # keep reference to dashboard so it's not garbage-collected
        self.dashboard = None  

    def handle_login(self):
        username = self.login_view.username_input.text().strip()
        password = self.login_view.password_input.text().strip()

        # Dummy authentication (replace with real DB check later)
        if username == "admin" and password == "1234":
            QMessageBox.information(self.login_view, "Login Success", "Welcome!")

            # Create and show the dashboard
            self.dashboard = AdminDashboard()
            self.dashboard.show()

            # Close the login window
            self.login_view.close()
        else:
            QMessageBox.warning(self.login_view, "Login Failed", "Invalid credentials")
