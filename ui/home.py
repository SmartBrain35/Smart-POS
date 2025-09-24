from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMessageBox
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
from controllers.accountController import AccountController
from controllers.employeeController import EmployeesController
from controllers.stockController import StockController
from controllers.salesController import SalesController
from controllers.damageController import DamageController
import logging

home_logger = logging.getLogger("HomePage")
home_logger.setLevel(logging.DEBUG)
if not home_logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    home_logger.addHandler(ch)


class HomePage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.page_configs = [
            (Ui_Dashboard, "page_dashboard"),
            (Ui_Stock, "page_stock"),
            (Ui_Sales, "page_sales"),
            (Ui_Report, "page_report"),
            (Ui_Employees, "page_employees"),
            (Ui_Return, "page_return"),
            (Ui_Damage, "page_damage"),
            (Ui_Expenditure, "page_expenditure"),
            (Ui_Account, "page_account"),
            (Ui_Settings, "page_settings"),
        ]
        self.page_loaded = [False] * len(self.page_configs)
        self.pages = {}

        self.current_button = None
        self.account_controller = None
        self.employees_controller = None
        self.stock_controller = None
        self.sales_controller = None
        self.damage_controller = None

        self.setupUi(self)
        self.setup_connections()
        home_logger.debug("HomePage initialized, switching to Dashboard")
        self.switch_page(0, "Dashboard")

    def setupUi(self, Home):
        Home.setObjectName("home")
        Home.setMinimumSize(1200, 800)
        Home.showMaximized()

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(Home)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        # Sidebar
        self.setup_sidebar()
        self.horizontalLayout.addWidget(self.sidebar, stretch=1)

        # Main Content
        self.mainContent = QtWidgets.QFrame(self.centralwidget)
        self.mainContent.setObjectName("mainContent")
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainContent)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Header
        self.setup_header()
        self.mainLayout.addWidget(self.header)

        # Stacked Pages
        self.stackedWidget = QtWidgets.QStackedWidget(self.mainContent)
        self.stackedWidget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setup_placeholder_pages()
        self.mainLayout.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.mainContent, stretch=4)

        Home.setCentralWidget(self.centralwidget)
        self.retranslateUi(Home)
        QtCore.QMetaObject.connectSlotsByName(Home)

    def setup_sidebar(self):
        self.sidebar = QtWidgets.QFrame(self.centralwidget)
        self.sidebar.setMinimumWidth(220)
        self.sidebar.setMaximumWidth(300)
        self.sidebar.setStyleSheet("background-color: #1e1e2f; color: white;")
        self.sidebar.setObjectName("sidebar")

        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(15, 15, 15, 15)
        self.sidebarLayout.setSpacing(8)
        self.sidebarLayout.setAlignment(QtCore.Qt.AlignTop)

        # Sidebar Title
        self.logo = QtWidgets.QLabel("SMART-POS")
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold)
        self.logo.setFont(font)
        self.logo.setStyleSheet("color: #ecf0f1; font-weight: 700; color: #00aaff")
        self.sidebarLayout.addWidget(self.logo)

        # --- Normal Button Style ---
        button_style = """
            QPushButton {
                background: transparent;
                color: white;
                border: none;
                text-align: left;
                font-size: 17px;
                padding: 10px 8px 10px 15px;
                border-radius: 6px;
            }
            QPushButton::menu-indicator { width: 0px; }
            QPushButton:hover { background-color: #00aaff; color: white; }
            QPushButton[active="true"] {
                background: #00aaff;
                color: white;
                font-weight: bold;
            }
            QPushButton[active="true"]:hover {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(41,128,185,1),
                    stop:1 rgba(31,97,141,1)
                );
            }
        """

        # --- Logout Button Style ---
        logout_style = """
            QPushButton {
                background: transparent;
                color: #ff4d4d;
                border: none;
                text-align: left;
                padding: 10px 8px 10px 15px;
                font-size: 17px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: rgba(255, 77, 77, 0.2);
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(255, 77, 77, 0.4);
            }
        """

        button_configs = [
            ("Dashboard", 0, "assets/icons/dashboard.png"),
            ("Stock", 1, "assets/icons/stock.png"),
            ("Sales", 2, "assets/icons/sales.png"),
            ("Report", 3, "assets/icons/report.png"),
            ("Employees", 4, "assets/icons/employees.png"),
            ("Return", 5, "assets/icons/return.png"),
            ("Damage", 6, "assets/icons/damage.png"),
            ("Expenditure", 7, "assets/icons/expenditure.png"),
            ("Account", 8, "assets/icons/account.png"),
            ("Settings", 9, "assets/icons/settings.png"),
        ]

        self.buttons = {}
        for name, index, icon_path in button_configs:
            btn = QtWidgets.QPushButton(f"  {name}")
            btn.setIcon(QtGui.QIcon(icon_path))
            btn.setIconSize(QtCore.QSize(22, 22))
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.setStyleSheet(button_style)
            btn.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            btn.setProperty("active", False)
            btn.setProperty("index", index)
            self.sidebarLayout.addWidget(btn)
            self.buttons[name] = btn

        self.sidebarLayout.addStretch()

        # Logout button
        logout_btn = QtWidgets.QPushButton("  Logout")
        logout_btn.setIcon(QtGui.QIcon("assets/icons/logout.png"))
        logout_btn.setIconSize(QtCore.QSize(22, 22))
        logout_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        logout_btn.setStyleSheet(logout_style)
        logout_btn.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.sidebarLayout.addWidget(logout_btn)
        self.buttons["Logout"] = logout_btn

    def setup_header(self):
        self.header = QtWidgets.QFrame(self.mainContent)
        self.header.setMinimumHeight(60)
        self.header.setStyleSheet("background-color: #2e4053;")
        self.headerLayout = QtWidgets.QHBoxLayout(self.header)
        self.headerLayout.setContentsMargins(20, 0, 20, 0)

        self.lbl_title = QtWidgets.QLabel("Dashboard")
        font = QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold)
        self.lbl_title.setFont(font)
        self.lbl_title.setStyleSheet("color: white;")
        self.headerLayout.addWidget(self.lbl_title)
        self.headerLayout.addStretch()

        self.userLabel = QtWidgets.QLabel("Welcome, Admin")
        self.userLabel.setStyleSheet("color: #ecf0f1; font-size: 13px;")
        self.headerLayout.addWidget(self.userLabel)

    def setup_placeholder_pages(self):
        for _ in self.page_configs:
            self.stackedWidget.addWidget(QtWidgets.QWidget())

    def load_page(self, index):
        if self.page_loaded[index]:
            return
        ui_class, attr_name = self.page_configs[index]
        page = self.stackedWidget.widget(index)
        ui_instance = ui_class()
        ui_instance.setupUi(page)
        self.pages[attr_name] = page
        setattr(self, attr_name, page)
        setattr(self, f"ui_{attr_name.split('_')[1]}", ui_instance)
        self.page_loaded[index] = True

    def setup_connections(self):
        for name, btn in self.buttons.items():
            if name == "Logout":
                btn.clicked.connect(self.logout)
            else:
                btn.clicked.connect(
                    lambda checked, idx=btn.property(
                        "index"
                    ), ttl=name, b=btn: self.switch_page(idx, ttl, b)
                )
            btn.setFocusPolicy(QtCore.Qt.StrongFocus)
            btn.installEventFilter(self)

    def switch_page(self, index, title, button=None):
        home_logger.debug(f"Switching to page {index} ({title})")

        if index is not None:
            self.load_page(index)
            self.stackedWidget.setCurrentIndex(index)
            self.lbl_title.setText(title)

            # === Controllers ===
            attr_name = self.page_configs[index][1]
            ui_instance = getattr(self, f"ui_{attr_name.split('_')[1]}", None)
            page = getattr(self, attr_name, None)

            # account controller
            if attr_name == "page_account":
                if self.account_controller is None:
                    self.account_controller = AccountController(ui_instance, page)
                    home_logger.debug("AccountController instantiated")
                else:
                    if hasattr(self.account_controller, "refresh_table"):
                        self.account_controller.refresh_table()
                        home_logger.debug("AccountController refreshed")

            # Employess controller
            if attr_name == "page_employees":
                if self.employees_controller is None:
                    self.employees_controller = EmployeesController(ui_instance, page)
                    home_logger.debug("EmployeesController instantiated")
                else:
                    if hasattr(self.employees_controller, "refresh_table"):
                        self.employees_controller.refresh_table()
                        home_logger.debug("EmployeesController refreshed")

            # Stock controller
            if attr_name == "page_stock":
                if self.stock_controller is None:
                    self.stock_controller = StockController(ui_instance, page)
                    home_logger.debug("StockController instantiated")
                else:
                    if hasattr(self.stock_controller, "refresh_table"):
                        self.stock_controller.refresh_table()
                        home_logger.debug("StockController refreshed")

            # Sales controller
            if attr_name == "page_sales":
                if self.sales_controller is None:
                    self.sales_controller = SalesController(ui_instance, page)
                    home_logger.debug("SalesController instantiated")
                else:
                    if hasattr(self.sales_controller, "refresh_table"):
                        self.sales_controller.refresh_table()
                        home_logger.debug("SalesController refreshed")

            # Damage controller
            if attr_name == "page_damage":
                if self.damage_controller is None:
                    self.damage_controller = DamageController(ui_instance, page)
                    home_logger.debug("DamageController instantiated")
                else:
                    if hasattr(self.damage_controller, "refresh_table"):
                        self.damage_controller.refresh_table()
                        home_logger.debug("DamageController refreshed")

            # Highlight buttons
            if self.current_button:
                self.current_button.setProperty("active", False)
                self.current_button.style().unpolish(self.current_button)
                self.current_button.style().polish(self.current_button)

            if button:
                self.current_button = button
                button.setProperty("active", True)
                button.style().unpolish(button)
                button.style().polish(button)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and isinstance(
            obj, QtWidgets.QPushButton
        ):
            if event.key() in (
                QtCore.Qt.Key_Return,
                QtCore.Qt.Key_Enter,
                QtCore.Qt.Key_Space,
            ):
                home_logger.debug(f"Button {obj.text()} triggered via key press")
                obj.click()
                return True
        return super().eventFilter(obj, event)

    def logout(self):
        from controllers.login import LoginController

        confirm = QMessageBox.question(
            self,
            "Logout Confirmation",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.close()
            self.login_controller = LoginController()
            self.login_controller.login_view.show()

    def retranslateUi(self, Home):
        _translate = QtCore.QCoreApplication.translate
        Home.setWindowTitle(_translate("Home", "SMART-POS Dashboard"))
