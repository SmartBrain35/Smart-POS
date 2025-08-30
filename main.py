# main.py
import sys
from PySide6.QtWidgets import QApplication
from controllers.login import LoginController


def main():
    app = QApplication(sys.argv)

    controller = LoginController()
    controller.login_view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
