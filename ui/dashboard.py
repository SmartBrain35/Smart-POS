# ui/admin_dashboard.py

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdminDashboard(object):
    def setupUi(self, AdminDashboard):
        AdminDashboard.setObjectName("AdminDashboard")
        AdminDashboard.resize(1200, 800)

        # Main window central widget
        self.centralwidget = QtWidgets.QWidget(AdminDashboard)
        self.centralwidget.setObjectName("centralwidget")

        # Horizontal layout (Sidebar + Main content)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)

        # ================= Sidebar =================
        self.sidebar = QtWidgets.QFrame(self.centralwidget)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #2C3E50;")
        self.sidebar.setObjectName("sidebar")

        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(0, 0, 0, 0)

        # Sidebar buttons
        self.btn_dashboard = self._create_sidebar_button("Dashboard")
        self.btn_stock = self._create_sidebar_button("Stock")
        self.btn_sales = self._create_sidebar_button("Sales")
        self.btn_report = self._create_sidebar_button("Report")
        self.btn_employees = self._create_sidebar_button("Employees")
        self.btn_return = self._create_sidebar_button("Return")
        self.btn_damage = self._create_sidebar_button("Damage")
        self.btn_expenditure = self._create_sidebar_button("Expenditure")
        self.btn_account = self._create_sidebar_button("Account")

        self.sidebarLayout.addStretch()
        self.btn_logout = self._create_sidebar_button("Logout")
        self.sidebarLayout.addWidget(self.btn_logout)

        # Add sidebar to main layout
        self.horizontalLayout.addWidget(self.sidebar)

        # ================= Main Content =================
        self.mainContent = QtWidgets.QFrame(self.centralwidget)
        self.mainContent.setStyleSheet("background-color: #ECF0F1;")
        self.mainContent.setObjectName("mainContent")

        self.mainLayout = QtWidgets.QVBoxLayout(self.mainContent)

        # Header
        self.header = QtWidgets.QFrame(self.mainContent)
        self.header.setFixedHeight(60)
        self.header.setStyleSheet("background-color: #34495E; color: white;")
        self.headerLayout = QtWidgets.QHBoxLayout(self.header)
        self.lbl_title = QtWidgets.QLabel("Admin Dashboard")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.lbl_title.setFont(font)
        self.lbl_title.setStyleSheet("color: white;")
        self.headerLayout.addWidget(self.lbl_title)
        self.headerLayout.addStretch()
        self.mainLayout.addWidget(self.header)

        # Stacked Widget (Pages)
        self.stackedWidget = QtWidgets.QStackedWidget(self.mainContent)
        self.stackedWidget.setObjectName("stackedWidget")

        # Pages
        self.page_dashboard = QtWidgets.QWidget()
        self.page_dashboard.setObjectName("page_dashboard")
        self.stackedWidget.addWidget(self.page_dashboard)

        self.page_stock = QtWidgets.QWidget()
        self.page_stock.setObjectName("page_stock")
        self.stackedWidget.addWidget(self.page_stock)

        self.page_sales = QtWidgets.QWidget()
        self.page_sales.setObjectName("page_sales")
        self.stackedWidget.addWidget(self.page_sales)

        self.page_report = QtWidgets.QWidget()
        self.page_report.setObjectName("page_report")
        self.stackedWidget.addWidget(self.page_report)

        self.page_employees = QtWidgets.QWidget()
        self.page_employees.setObjectName("page_employees")
        self.stackedWidget.addWidget(self.page_employees)

        self.page_return = QtWidgets.QWidget()
        self.page_return.setObjectName("page_return")
        self.stackedWidget.addWidget(self.page_return)

        self.page_damage = QtWidgets.QWidget()
        self.page_damage.setObjectName("page_damage")
        self.stackedWidget.addWidget(self.page_damage)

        self.page_expenditure = QtWidgets.QWidget()
        self.page_expenditure.setObjectName("page_expenditure")
        self.stackedWidget.addWidget(self.page_expenditure)

        self.page_account = QtWidgets.QWidget()
        self.page_account.setObjectName("page_account")
        self.stackedWidget.addWidget(self.page_account)

        self.mainLayout.addWidget(self.stackedWidget)

        self.horizontalLayout.addWidget(self.mainContent)

        AdminDashboard.setCentralWidget(self.centralwidget)

        self.retranslateUi(AdminDashboard)
        QtCore.QMetaObject.connectSlotsByName(AdminDashboard)

    # Helper function to make sidebar buttons consistent
    def _create_sidebar_button(self, text):
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(40)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2C3E50;
                color: white;
                border: none;
                text-align: left;
                padding-left: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
            """
        )
        self.sidebarLayout.addWidget(btn)
        return btn

    def retranslateUi(self, AdminDashboard):
        _translate = QtCore.QCoreApplication.translate
        AdminDashboard.setWindowTitle(_translate("AdminDashboard", "Admin Dashboard"))
