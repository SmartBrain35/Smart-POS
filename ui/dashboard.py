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


        # === Account Page UI ===
        self.page_account = QtWidgets.QWidget()
        account_layout = QtWidgets.QVBoxLayout(self.page_account)
        account_layout.setContentsMargins(20, 20, 20, 20)
        account_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(850)   # wider form
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(35)   # space between columns
        form_layout.setVerticalSpacing(25)     # space between field groups

        # Common label styling
        label_style = "color: black; font-weight: bold;"

        def create_field(label_text, widget):
            """Helper: stack label + widget vertically with small spacing"""
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(4)   # << reduce gap label-input here
            lbl = QtWidgets.QLabel(label_text)
            lbl.setStyleSheet(label_style)
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # Name
        self.input_name = QtWidgets.QLineEdit()
        self.input_name.setPlaceholderText("Enter name")
        self.input_name.setMinimumWidth(int(form_container.width() * 0.4))
        form_layout.addWidget(create_field("Name:", self.input_name), 0, 0, 1, 2)

        # Phone
        self.input_phone = QtWidgets.QLineEdit()
        self.input_phone.setPlaceholderText("Enter phone number")
        self.input_phone.setMinimumWidth(int(form_container.width() * 0.4))
        form_layout.addWidget(create_field("Phone:", self.input_phone), 0, 2, 1, 2)

        # Town
        self.input_town = QtWidgets.QLineEdit()
        self.input_town.setPlaceholderText("Enter town")
        self.input_town.setMinimumWidth(int(form_container.width() * 0.4))
        form_layout.addWidget(create_field("Town:", self.input_town), 1, 0, 1, 2)

        # Email
        self.input_email = QtWidgets.QLineEdit()
        self.input_email.setPlaceholderText("Enter email")
        self.input_email.setMinimumWidth(int(form_container.width() * 0.4))
        form_layout.addWidget(create_field("Email:", self.input_email), 1, 2, 1, 2)

        # Password
        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setMinimumWidth(int(form_container.width() * 0.4))
        form_layout.addWidget(create_field("Password:", self.input_password), 2, 0, 1, 2)

        # Role
        self.input_role = QtWidgets.QComboBox()
        self.input_role.addItems(["Admin", "Manager", "Cashier", "Sales Person"])
        self.input_role.setMinimumWidth(int(form_container.width() * 0.4))
        form_layout.addWidget(create_field("Role:", self.input_role), 2, 2, 1, 2)

        # Register Button (centered, extended)
        self.btn_register = QtWidgets.QPushButton("Register User")
        self.btn_register.setObjectName("primaryButton")
        self.btn_register.setFixedWidth(int(form_container.width() * 0.5))
        form_layout.addWidget(self.btn_register, 3, 0, 1, 4, alignment=QtCore.Qt.AlignCenter)
        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        account_layout.addLayout(form_wrapper)

        # === Table Section ===
        self.table_users = QtWidgets.QTableWidget()
        self.table_users.setColumnCount(7)  # Removed Ghana Card column
        self.table_users.setHorizontalHeaderLabels([
            "ID", "Name", "Phone", "Email", "Role", "Status", "Actions"
        ])
        self.table_users.horizontalHeader().setStretchLastSection(True)
        self.table_users.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_users.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_users.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_users.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_users.setAlternatingRowColors(True)
        self.table_users.verticalHeader().setVisible(False)

        # Sample data (without Ghana Card)
        users_data = [
            (1, "Admin User", "0244000001", "admin@pos.com", "Admin", "Active"),
            (2, "Cashier One", "0244000002", "cashier@pos.com", "Cashier", "Active"),
            (3, "Manager One", "0244000003", "manager@pos.com", "Manager", "Inactive")
        ]

        self.table_users.setRowCount(len(users_data))

        for row, (uid, name, phone, email, role, status) in enumerate(users_data):
            self.table_users.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_users.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_users.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
            self.table_users.setItem(row, 3, QtWidgets.QTableWidgetItem(email))
            self.table_users.setItem(row, 4, QtWidgets.QTableWidgetItem(role))
            self.table_users.setItem(row, 5, QtWidgets.QTableWidgetItem(status))

            # Actions cell (Edit + Delete together in one cell)
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(45)

            btn_edit = QtWidgets.QPushButton()
            btn_edit.setObjectName("iconButton")
            btn_edit.setIcon(QtGui.QIcon("assets/icons/edit.png"))
            btn_edit.setToolTip("Edit User")
            btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            btn_delete = QtWidgets.QPushButton()
            btn_delete.setObjectName("iconButton")
            btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            btn_delete.setToolTip("Delete User")
            btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.addStretch()

            self.table_users.setCellWidget(row, 6, action_widget)

        account_layout.addWidget(self.table_users)


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
