from PySide6 import QtCore, QtGui, QtWidgets

from ui.dashboard_ui import Ui_Dashboard
from ui.stock_ui import Ui_Stock
from ui.sales_ui import Ui_Sales
from ui.report_ui import Ui_Report
from ui.employees_ui import Ui_Employees
from ui.return_ui import Ui_Return
from ui.damage_ui import Ui_Damage
from ui.expenditure_ui import Ui_Expenditure
from ui.account_ui import Ui_Account
from ui.settings_ui import Ui_Settings
from ui.simple_page_ui import Ui_SimplePage
from ui.report_ui import Ui_Report

# from controllers.report import ReportController


class HomePage(object):
    def setupUi(self, Home):
        Home.setObjectName("home")
        Home.setMinimumSize(1200, 800)
        Home.showMaximized()

        # ===== Central Widget =====
        self.centralwidget = QtWidgets.QWidget(Home)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        # ===== Sidebar =====
        self.sidebar = QtWidgets.QFrame(self.centralwidget)
        self.sidebar.setFixedWidth(220)
        self.sidebar.setStyleSheet("background-color: #1e1e2f; color: white;")
        self.sidebar.setObjectName("sidebar")

        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(10, 10, 10, 10)
        self.sidebarLayout.setSpacing(10)
        self.sidebarLayout.setAlignment(QtCore.Qt.AlignTop)

        # Sidebar Title
        self.logo = QtWidgets.QLabel("SMART-POS")
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.logo.setFont(font)
        self.logo.setStyleSheet("color: #00c2ff; margin-bottom: 20px; font-size: 20px;")
        self.sidebarLayout.addWidget(self.logo)

        # Sidebar Buttons
        self.buttons = {}
        button_names = [
            "Dashboard",
            "Stock",
            "Sales",
            "Report",
            "Employees",
            "Return",
            "Damage",
            "Expenditure",
            "Account",
            "Settings",
            "Logout",
        ]

        for name in button_names:
            btn = QtWidgets.QPushButton(name)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    border: none;
                    font-size: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #00c2ff;
                    color: black;
                    border-radius: 5px;
                }
                """
            )
            btn.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            self.sidebarLayout.addWidget(btn)
            self.buttons[name] = btn

        self.sidebarLayout.addStretch()
        self.horizontalLayout.addWidget(self.sidebar)

        # ===== Main Content =====
        self.mainContent = QtWidgets.QFrame(self.centralwidget)
        self.mainContent.setObjectName("mainContent")
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainContent)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Header
        self.header = QtWidgets.QFrame(self.mainContent)
        self.header.setFixedHeight(60)
        self.header.setStyleSheet("background-color: #2e4053;")
        self.headerLayout = QtWidgets.QHBoxLayout(self.header)
        self.headerLayout.setContentsMargins(20, 0, 20, 0)

        self.lbl_title = QtWidgets.QLabel("Dashboard")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.lbl_title.setFont(font)
        self.lbl_title.setStyleSheet("color: white;")
        self.headerLayout.addWidget(self.lbl_title)

        self.headerLayout.addStretch()

        self.userLabel = QtWidgets.QLabel("Welcome, Admin")
        self.userLabel.setStyleSheet("color: #ecf0f1; font-size: 13px;")
        self.headerLayout.addWidget(self.userLabel)

        self.mainLayout.addWidget(self.header)

        # Stacked Pages
        self.stackedWidget = QtWidgets.QStackedWidget(self.mainContent)

        # Dashboard Page (simple)
        self.page_dashboard = QtWidgets.QWidget()
        self.ui_dashboard = Ui_Dashboard()
        self.ui_dashboard.setupUi(self.page_dashboard)

        # Stock Page
        self.page_stock = QtWidgets.QWidget()
        self.ui_stock = Ui_Stock()
        self.ui_stock.setupUi(self.page_stock)

        # Sales Page
        self.page_sales = QtWidgets.QWidget()
        self.ui_sales = Ui_Sales()
        self.ui_sales.setupUi(self.page_sales)

        # Report Page
        self.page_report = QtWidgets.QWidget()
        self.ui_report = Ui_Report()
        self.ui_report.setupUi(self.page_report)
        # Report Controller
        # self.report_controller = ReportController(self.ui_report)

        # Employees Page
        self.page_employees = QtWidgets.QWidget()
        self.ui_employees = Ui_Employees()
        self.ui_employees.setupUi(self.page_employees)

        # Return Page
        self.page_return = QtWidgets.QWidget()
        self.ui_return = Ui_Return()
        self.ui_return.setupUi(self.page_return)

        # Damage Page
        self.page_damage = QtWidgets.QWidget()
        self.ui_damage = Ui_Damage()
        self.ui_damage.setupUi(self.page_damage)

        # Expenditure Page
        self.page_expenditure = QtWidgets.QWidget()
        self.ui_expenditure = Ui_Expenditure()
        self.ui_expenditure.setupUi(self.page_expenditure)

        # Account Page
        self.page_account = QtWidgets.QWidget()
        self.ui_account = Ui_Account()
        self.ui_account.setupUi(self.page_account)

        # Settings Page (simple)
        self.page_settings = QtWidgets.QWidget()
        self.ui_settings = Ui_Settings()
        self.ui_settings.setupUi(self.page_settings)

        # Add pages to stacked widget
        self.stackedWidget.addWidget(self.page_dashboard)  # index 0
        self.stackedWidget.addWidget(self.page_stock)  # index 1
        self.stackedWidget.addWidget(self.page_sales)  # index 2
        self.stackedWidget.addWidget(self.page_report)  # index 3
        self.stackedWidget.addWidget(self.page_employees)  # index 4
        self.stackedWidget.addWidget(self.page_return)  # index 5
        self.stackedWidget.addWidget(self.page_damage)  # index 6
        self.stackedWidget.addWidget(self.page_expenditure)  # index 7
        self.stackedWidget.addWidget(self.page_account)  # index 8
        self.stackedWidget.addWidget(self.page_settings)  # index 9

        self.mainLayout.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.mainContent)

        Home.setCentralWidget(self.centralwidget)
        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

        # ===== Page Switching Connections =====
        self.buttons["Dashboard"].clicked.connect(
            lambda: self.switch_page(0, "Dashboard")
        )
        self.buttons["Stock"].clicked.connect(lambda: self.switch_page(1, "Stock"))
        self.buttons["Sales"].clicked.connect(lambda: self.switch_page(2, "Sales"))
        self.buttons["Report"].clicked.connect(lambda: self.switch_page(3, "Report"))
        self.buttons["Employees"].clicked.connect(
            lambda: self.switch_page(4, "Employees")
        )
        self.buttons["Return"].clicked.connect(lambda: self.switch_page(5, "Return"))
        self.buttons["Damage"].clicked.connect(lambda: self.switch_page(6, "Damage"))
        self.buttons["Expenditure"].clicked.connect(
            lambda: self.switch_page(7, "Expenditure")
        )
        self.buttons["Account"].clicked.connect(lambda: self.switch_page(8, "Account"))
        self.buttons["Settings"].clicked.connect(
            lambda: self.switch_page(9, "Settings")
        )
        self.buttons["Logout"].clicked.connect(self.logout)

    # add this method inside Home class
    def logout(self):
        from controllers.login import LoginController

        # Close the parent window (the QMainWindow that loaded this UI)
        self.centralwidget.window().close()

        # Show login window again
        self.login_controller = LoginController()
        self.login_controller.login_view.show()

    def switch_page(self, index, title):
        """Switch stacked page and update header title"""
        self.stackedWidget.setCurrentIndex(index)
        self.lbl_title.setText(title)

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "Dashboard"))
