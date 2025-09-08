# ui/login.py
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QFrame,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QGuiApplication
import os
import sys


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Frameless + transparent window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # allow rounded corners
        self.setFixedSize(400, 300)  # fixed size

        # Outer layout (transparent background)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setAlignment(Qt.AlignCenter)

        # Container with rounded corners + shadow
        self.container = QFrame()
        self.container.setObjectName("loginContainer")
        self.container.setFixedSize(400, 300)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 120))  # softer shadow
        self.container.setGraphicsEffect(shadow)

        # Inner layout
        layout = QVBoxLayout(self.container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        self.lbl_title = QLabel("Login to Smart POS")
        self.lbl_title.setObjectName("titleLabel")
        layout.addWidget(self.lbl_title, alignment=Qt.AlignCenter)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("LoginUsernameInput")
        layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setObjectName("LoginPasswordInput")
        layout.addWidget(self.password_input)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setVisible(False)
        layout.addWidget(self.error_label, alignment=Qt.AlignCenter)

        # Buttons
        btn_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("BtnLogin")
        btn_layout.addWidget(self.login_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setObjectName("BtnExit")
        self.exit_button.clicked.connect(sys.exit)
        btn_layout.addWidget(self.exit_button)

        layout.addLayout(btn_layout)

        outer_layout.addWidget(self.container)

        # Center window on screen
        self.center_on_screen()

    def show_error(self, message: str):
        """Show error message inline"""
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def center_on_screen(self):
        """Center window on the screen"""
        screen = QGuiApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
