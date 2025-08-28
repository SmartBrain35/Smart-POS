# ui/login.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS System - Login")
        self.resize(400, 250)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        main_layout.addWidget(title)

        # Username
        username_layout = QHBoxLayout()
        lbl_username = QLabel("Username:")
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Enter username")
        username_layout.addWidget(lbl_username)
        username_layout.addWidget(self.txt_username)
        main_layout.addLayout(username_layout)

        # Password
        password_layout = QHBoxLayout()
        lbl_password = QLabel("Password:")
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText("Enter password")
        password_layout.addWidget(lbl_password)
        password_layout.addWidget(self.txt_password)
        main_layout.addLayout(password_layout)

        # Login Button
        self.btn_login = QPushButton("Login")
        self.btn_login.setFixedHeight(40)
        main_layout.addWidget(self.btn_login)

        # Message label (for errors or info)
        self.lbl_message = QLabel("")
        self.lbl_message.setAlignment(Qt.AlignCenter)
        self.lbl_message.setStyleSheet("color: red; font-size: 12px;")
        main_layout.addWidget(self.lbl_message)
