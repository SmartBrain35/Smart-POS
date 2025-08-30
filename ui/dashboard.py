from PySide6 import QtCore, QtGui, QtWidgets

class Ui_AdminDashboard(object):
    def setupUi(self, AdminDashboard):
        AdminDashboard.setObjectName("AdminDashboard")
        AdminDashboard.resize(1200, 800)

        # ===== Central Widget =====
        self.centralwidget = QtWidgets.QWidget(AdminDashboard)
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
        self.sidebarLayout.setContentsMargins(10, 20, 10, 20)
        self.sidebarLayout.setSpacing(10)
        self.sidebarLayout.setAlignment(QtCore.Qt.AlignTop)

        # Sidebar Title
        self.logo = QtWidgets.QLabel("SMART POS")
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.logo.setFont(font)
        self.logo.setStyleSheet("color: #00c2ff; margin-bottom: 20px;")
        self.sidebarLayout.addWidget(self.logo)

        # Sidebar Buttons
        self.buttons = {}
        button_names = [
            "Dashboard", "Stock", "Sales", "Report", "Employees",
            "Return", "Damage", "Expenditure", "Account", "Settings", "Logout"
        ]

        for name in button_names:
            btn = QtWidgets.QPushButton(name)
            btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    border: none;
                    font-size: 15px;
                }
                QPushButton:hover {
                    background-color: #00c2ff;
                    color: black;
                    border-radius: 5px;
                }
            """)
            btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
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

        self.page_dashboard = QtWidgets.QLabel("Welcome to Smart POS Dashboard", alignment=QtCore.Qt.AlignCenter)
        self.page_dashboard.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.page_stock = QtWidgets.QLabel("📦 Stock Page", alignment=QtCore.Qt.AlignCenter)
        self.page_sales = QtWidgets.QLabel("🛒 Sales Page", alignment=QtCore.Qt.AlignCenter)
        self.page_report = QtWidgets.QLabel("📊 Report Page", alignment=QtCore.Qt.AlignCenter)
        self.page_employees = QtWidgets.QLabel("👥 Employees Page", alignment=QtCore.Qt.AlignCenter)
        self.page_return = QtWidgets.QLabel("↩ Return Page", alignment=QtCore.Qt.AlignCenter)
        self.page_damage = QtWidgets.QLabel("💥 Damage Page", alignment=QtCore.Qt.AlignCenter)
        self.page_expenditure = QtWidgets.QLabel("💵 Expenditure Page", alignment=QtCore.Qt.AlignCenter)
        self.page_account = QtWidgets.QLabel("⚙ Account Page", alignment=QtCore.Qt.AlignCenter)
        self.page_settings = QtWidgets.QLabel("🔧 Settings Page", alignment=QtCore.Qt.AlignCenter)

        # Add pages to stacked widget
        self.stackedWidget.addWidget(self.page_dashboard)    # index 0
        self.stackedWidget.addWidget(self.page_stock)        # index 1
        self.stackedWidget.addWidget(self.page_sales)        # index 2
        self.stackedWidget.addWidget(self.page_report)       # index 3
        self.stackedWidget.addWidget(self.page_employees)    # index 4
        self.stackedWidget.addWidget(self.page_return)       # index 5
        self.stackedWidget.addWidget(self.page_damage)       # index 6
        self.stackedWidget.addWidget(self.page_expenditure)  # index 7
        self.stackedWidget.addWidget(self.page_account)      # index 8
        self.stackedWidget.addWidget(self.page_settings)     # index 9

        self.mainLayout.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.mainContent)

        AdminDashboard.setCentralWidget(self.centralwidget)
        self.retranslateUi(AdminDashboard)
        QtCore.QMetaObject.connectSlotsByName(AdminDashboard)

        # ===== Page Switching Connections =====
        self.buttons["Dashboard"].clicked.connect(lambda: self.switch_page(0, "Dashboard"))
        self.buttons["Stock"].clicked.connect(lambda: self.switch_page(1, "Stock"))
        self.buttons["Sales"].clicked.connect(lambda: self.switch_page(2, "Sales"))
        self.buttons["Report"].clicked.connect(lambda: self.switch_page(3, "Report"))
        self.buttons["Employees"].clicked.connect(lambda: self.switch_page(4, "Employees"))
        self.buttons["Return"].clicked.connect(lambda: self.switch_page(5, "Return"))
        self.buttons["Damage"].clicked.connect(lambda: self.switch_page(6, "Damage"))
        self.buttons["Expenditure"].clicked.connect(lambda: self.switch_page(7, "Expenditure"))
        self.buttons["Account"].clicked.connect(lambda: self.switch_page(8, "Account"))
        self.buttons["Settings"].clicked.connect(lambda: self.switch_page(9, "Settings"))
        self.buttons["Logout"].clicked.connect(self.logout)


    # add this method inside AdminDashboard class
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

    def retranslateUi(self, AdminDashboard):
        _translate = QtCore.QCoreApplication.translate
        AdminDashboard.setWindowTitle(_translate("AdminDashboard", "Dashboard"))
