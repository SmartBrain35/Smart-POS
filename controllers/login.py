###Login controller
import logging
from PySide6.QtWidgets import QMessageBox, QMainWindow
from ui.login_window import LoginWindow
from ui.home import HomePage
from backend.apis import AccountAPI

# Configure logging for debugging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


class LoginController:
    def __init__(self):
        # Initialize login view
        self.login_view = LoginWindow()
        self.login_view.login_button.clicked.connect(self.handle_login)
        self.dashboard_window = None
        logging.info("LoginController initialized")

    def handle_login(self):
        """Handle login button click, authenticate user, and transition to dashboard."""
        username = self.login_view.username_input.text().strip()
        password = self.login_view.password_input.text().strip()

        if not username or not password:
            self.show_error("Please enter both username and password.")
            logging.warning("Login attempt with empty username or password")
            return

        try:
            # Call API authentication method
            result = AccountAPI.authenticate(username, password)
            logging.debug(f"Authentication result: {result}")
        except Exception as e:
            self.show_error(f"Authentication failed: {str(e)}")
            logging.error(f"Authentication error: {str(e)}")
            return

        if result["success"]:
            # Create and show dashboard
            self.dashboard_window = HomePage()
            self.dashboard_window.show()
            self.login_view.close()
            logging.info(f"Login successful for user: {username}, dashboard shown")
        else:
            self.show_error(result["error"])
            logging.warning(
                f"Login failed for user: {username}, error: {result['error']}"
            )

    def show_error(self, message):
        """Display an error message in a QMessageBox."""
        QMessageBox.warning(self.login_view, "Login Failed", message, QMessageBox.Ok)