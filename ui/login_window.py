# ui/login.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Smart POS")
        self.setGeometry(500, 200, 400, 250)

        layout = QVBoxLayout(self)

        self.lbl_title = QLabel("Login to Smart POS")
        self.lbl_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.lbl_title)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)
