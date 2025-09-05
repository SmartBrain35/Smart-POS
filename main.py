from PySide6.QtWidgets import QApplication
from controllers.login import LoginController
import os, sys


def main():

    app = QApplication(sys.argv)

    # Load QSS globally so ALL windows (dashboard, account page, etc.) use it
    qss_path = os.path.join(os.path.dirname(__file__), "assets/styles/style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    controller = LoginController()
    controller.login_view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
