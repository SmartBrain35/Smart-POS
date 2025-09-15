from PySide6.QtWidgets import QMessageBox, QMainWindow
from ui.login_window import LoginWindow
from ui.home import HomePage
from backend.apis import AccountAPI


class LoginController:
    def __init__(self):
        # Create login view
        self.login_view = LoginWindow()
        self.login_view.login_button.clicked.connect(self.handle_login)

        self.dashboard_window = None

    def handle_login(self):
        username = self.login_view.username_input.text().strip()
        password = self.login_view.password_input.text().strip()

        if not username or not password:
            self.login_view.show_error("username/password invalid")
            return

        ## call API authentication method
        result = AccountAPI.authenticate(username, password)

        if result["success"]:
            # Create dashboard window properly
            self.dashboard_window = QMainWindow()
            self.ui = HomePage()
            self.ui.setupUi(self.dashboard_window)

            self.dashboard_window.show()
            self.login_view.close()
        else:
            QMessageBox.warning(self.login_view, "Login Failed", result["error"])