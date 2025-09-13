# controllers/dashboard.py

from PySide6.QtWidgets import QMessageBox
from ui.home import Ui_AdminDashboard
from ui.login_window import LoginWindow


class DashboardController(Ui_AdminDashboard):
    def __init__(self):
        super().__init__()

        # Connect sidebar buttons
        self.btn_dashboard.clicked.connect(self.show_dashboard)
        self.btn_stock.clicked.connect(self.show_stock)
        self.btn_sales.clicked.connect(self.show_sales)
        self.btn_report.clicked.connect(self.show_report)
        self.btn_employees.clicked.connect(self.show_employees)
        self.btn_return.clicked.connect(self.show_return)
        self.btn_damage.clicked.connect(self.show_damage)
        self.btn_expenditure.clicked.connect(self.show_expenditure)
        self.btn_account.clicked.connect(self.show_account)
        self.btn_logout.clicked.connect(self.logout)

    # ===================== PAGE HANDLERS =====================
    def show_dashboard(self):
        self.pages.setCurrentWidget(self.page_dashboard)

    def show_stock(self):
        self.pages.setCurrentWidget(self.page_stock)

    def show_sales(self):
        self.pages.setCurrentWidget(self.page_sales)

    def show_report(self):
        self.pages.setCurrentWidget(self.page_report)

    def show_employees(self):
        self.pages.setCurrentWidget(self.page_employees)

    def show_return(self):
        self.pages.setCurrentWidget(self.page_return)

    def show_damage(self):
        self.pages.setCurrentWidget(self.page_damage)

    def show_expenditure(self):
        self.pages.setCurrentWidget(self.page_expenditure)

    def show_account(self):
        self.pages.setCurrentWidget(self.page_account)

    # ===================== LOGOUT =====================
    def logout(self):
        confirm = QMessageBox.question(
            self,
            "Logout Confirmation",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.close()  # close dashboard
            self.login_window = LoginWindow()
            self.login_window.show()
