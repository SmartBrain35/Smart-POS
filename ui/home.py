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
        self.setupUi(self)
        self.setup_connections()
        self.switch_page(0, "Dashboard")  # Load and show dashboard initially

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
        font = QtGui.QFont("Segoe UI", 20, QtGui.QFont.Bold)
        self.logo.setFont(font)
        self.logo.setStyleSheet("color: #00c2ff; margin-bottom: 25px;")
        self.sidebarLayout.addWidget(self.logo)

        # Sidebar Buttons
        button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                padding: 12px 15px;
                padding-left: 40px; /* Increased padding to add space after icon */
                text-align: left;
                border: none;
                font-size: 15px;
                font-weight: bold;
                border-radius: 5px;
                margin: 2px 0;
            }
            QPushButton:hover {
                background-color: #00c2ff;
                color: black;
            }
            QPushButton:pressed {
                background-color: #0086b3;
                color: white;
            }
            QPushButton[active=true] {
                background-color: #00c2ff;
                color: black;
                border-left: 4px solid #ffffff; /* Fixed typo from #a190b */
            }
            QPushButton > QIcon {
                color: white; /* Default icon color */
                margin-right: 10px; /* Additional spacing between icon and text */
            }
            QPushButton:hover > QIcon {
                color: black; /* Icon color on hover */
            }
            QPushButton:pressed > QIcon {
                color: white; /* Icon color when pressed */
            }
            QPushButton[active=true] > QIcon {
                color: black; /* Icon color when active */
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
            ("Logout", None, "assets/icons/logout.png"),
        ]

        screen = QtWidgets.QApplication.primaryScreen()
        dpi = screen.logicalDotsPerInch()
        icon_size = QtCore.QSize(24, 24) if dpi < 120 else QtCore.QSize(32, 32)

        self.buttons = {}
        for name, index, icon_path in button_configs:
            btn = QtWidgets.QPushButton(name)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.setStyleSheet(button_style)
            btn.setIcon(QtGui.QIcon(icon_path))
            btn.setIconSize(icon_size)
            btn.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            btn.setMinimumHeight(45)
            btn.setProperty("index", index)
            btn.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.sidebarLayout.addWidget(btn)
            self.buttons[name.lower()] = btn
        self.sidebarLayout.addStretch()

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
            if name == "logout":
                btn.clicked.connect(self.logout)
            else:
                btn.clicked.connect(
                    lambda checked, idx=btn.property(
                        "index"
                    ), ttl=name.capitalize(), b=btn: self.switch_page(idx, ttl, b)
                )
            btn.setFocusPolicy(QtCore.Qt.StrongFocus)
            btn.installEventFilter(self)

    def switch_page(self, index, title, button=None):
        if index is not None:
            self.load_page(index)
            self.stackedWidget.setCurrentIndex(index)
            self.lbl_title.setText(title)
            # Update active button state
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