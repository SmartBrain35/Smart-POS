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


     # === Stock Page UI with Tabs ===
        self.page_stock = QtWidgets.QWidget()
        stock_layout = QtWidgets.QVBoxLayout(self.page_stock)
        stock_layout.setContentsMargins(20, 20, 20, 20)
        stock_layout.setSpacing(12)  # reduced spacing

        # --- Centered Tabs ---
        tabs_wrapper = QtWidgets.QHBoxLayout()
        tabs_wrapper.addStretch()
        self.stock_tabs = QtWidgets.QTabWidget()
        self.stock_tabs.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # ✅ keep centered
        tabs_wrapper.addWidget(self.stock_tabs)
        tabs_wrapper.addStretch()
        stock_layout.addLayout(tabs_wrapper)

        # Apply tab styling
        self.stock_tabs.setStyleSheet("""
            QTabBar::tab {
                min-width: 150px;
                font-size: 14px;
                font-weight: bold;
                color: #0f172a;
                padding: 6px 12px;
                margin: 4px;
                border-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #00c2ff;
                color: black;
            }
            QTabWidget::pane {
                border: none;
            }
        """)

        # === Retail Tab ===
        self.tab_retail = QtWidgets.QWidget()
        retail_layout = QtWidgets.QVBoxLayout(self.tab_retail)
        retail_layout.setContentsMargins(20, 20, 20, 20)
        retail_layout.setSpacing(12)  # reduced spacing
        self.stock_tabs.addTab(self.tab_retail, "Retail")

        # --- Retail Page UI (inserted here) ---
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(820)
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(12, 12, 12, 12)
        form_layout.setHorizontalSpacing(24)
        form_layout.setVerticalSpacing(12)

        label_style = "color: black; font-weight: bold;"

        def vfield(label_text, widget):
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(4)  # tighter gap
            lbl = QtWidgets.QLabel(label_text)
            lbl.setStyleSheet(label_style)
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # ID
        self.stock_id_input = QtWidgets.QLineEdit()
        self.stock_id_input.setPlaceholderText("Auto / Enter ID")
        form_layout.addWidget(vfield("ID:", self.stock_id_input), 0, 0)

        # Item Name
        self.stock_name_input = QtWidgets.QLineEdit()
        self.stock_name_input.setPlaceholderText("Enter item name")
        form_layout.addWidget(vfield("Item Name:", self.stock_name_input), 0, 1)

        # Quantity
        self.stock_qty_input = QtWidgets.QLineEdit()
        self.stock_qty_input.setPlaceholderText("Enter quantity (integer)")
        form_layout.addWidget(vfield("Quantity:", self.stock_qty_input), 0, 2)

        # Cost Price
        self.stock_cost_input = QtWidgets.QLineEdit()
        self.stock_cost_input.setPlaceholderText("Unit cost price")
        form_layout.addWidget(vfield("Cost Price:", self.stock_cost_input), 1, 0)

        # Selling Price
        self.stock_selling_input = QtWidgets.QLineEdit()
        self.stock_selling_input.setPlaceholderText("Unit selling price")
        form_layout.addWidget(vfield("Selling Price:", self.stock_selling_input), 1, 1)

        # Expiry date + checkbox
        expire_widget = QtWidgets.QWidget()
        expire_h = QtWidgets.QHBoxLayout(expire_widget)
        expire_h.setContentsMargins(0, 0, 0, 0)
        expire_h.setSpacing(4)
        self.stock_expiry_checkbox = QtWidgets.QCheckBox("")
        self.stock_expiry_checkbox.setFixedWidth(18)
        self.stock_expiry_date = QtWidgets.QDateEdit()
        self.stock_expiry_date.setCalendarPopup(True)
        self.stock_expiry_date.setDate(QtCore.QDate.currentDate())
        self.stock_expiry_date.setEnabled(False)

        self.stock_expiry_checkbox.toggled.connect(self.stock_expiry_date.setEnabled)

        expire_h.addWidget(self.stock_expiry_checkbox)
        expire_h.addWidget(self.stock_expiry_date)
        form_layout.addWidget(vfield("Expire Date:", expire_widget), 1, 2)

        # Buttons
        btn_widget = QtWidgets.QWidget()
        btn_h = QtWidgets.QHBoxLayout(btn_widget)
        btn_h.setContentsMargins(0, 0, 0, 0)
        btn_h.setSpacing(12)

        self.stock_add_btn = QtWidgets.QPushButton("Add Item")
        self.stock_update_btn = QtWidgets.QPushButton("Update")
        self.stock_delete_btn = QtWidgets.QPushButton("Delete")
        self.stock_clear_btn = QtWidgets.QPushButton("Clear")

        for b in (self.stock_add_btn, self.stock_update_btn, self.stock_delete_btn, self.stock_clear_btn):
            b.setObjectName("primaryButton")

        btn_h.addStretch()
        btn_h.addWidget(self.stock_add_btn)
        btn_h.addWidget(self.stock_update_btn)
        btn_h.addWidget(self.stock_delete_btn)
        btn_h.addWidget(self.stock_clear_btn)
        btn_h.addStretch()
        form_layout.addWidget(btn_widget, 2, 0, 1, 3)

        # center form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        retail_layout.addLayout(form_wrapper)

        # === Filter Section ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(8)  # reduced spacing

        self.btn_filter = QtWidgets.QPushButton("Filter")
        self.btn_filter.setObjectName("primaryButton")
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText("Filter by item name...")
        self.filter_input.setFixedWidth(int(form_container.width() * 0.3))

        filter_container.addWidget(self.btn_filter)
        filter_container.addWidget(self.filter_input)
        filter_container.addStretch()
        retail_layout.addLayout(filter_container)

        # --- Table ---
        self.table_stock = QtWidgets.QTableWidget()
        self.table_stock.setColumnCount(9)
        self.table_stock.setHorizontalHeaderLabels([
            "ID", "Item Name", "Quantity", "Cost Price", "Selling Price", "Expiry",
            "Total Cost", "Total Selling", "Profit"
        ])
        self.table_stock.horizontalHeader().setStretchLastSection(True)
        self.table_stock.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_stock.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_stock.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_stock.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_stock.setAlternatingRowColors(True)
        self.table_stock.verticalHeader().setVisible(False)
        self.table_stock.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)  # ✅ extend table

        # ✅ click-row to fill inputs
        def on_stock_row_click():
            row = self.table_stock.currentRow()
            if row >= 0:
                self.stock_id_input.setText(self.table_stock.item(row, 0).text())
                self.stock_name_input.setText(self.table_stock.item(row, 1).text())
                self.stock_qty_input.setText(self.table_stock.cellWidget(row, 2).text()) if self.table_stock.cellWidget(row, 2) else None
                self.stock_cost_input.setText(self.table_stock.item(row, 3).text())
                self.stock_selling_input.setText(self.table_stock.item(row, 4).text())
                expiry_val = self.table_stock.item(row, 5).text()
                if expiry_val != "N/A":
                    self.stock_expiry_checkbox.setChecked(True)
                    self.stock_expiry_date.setDate(QtCore.QDate.fromString(expiry_val, "yyyy-MM-dd"))
                else:
                    self.stock_expiry_checkbox.setChecked(False)

        self.table_stock.itemSelectionChanged.connect(on_stock_row_click)

        # sample rows
        def create_quantity_progress(qty: int):
            bar = QtWidgets.QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(min(qty, 100))
            if qty <= 10:
                color = "#ff4d4d"        # red
            elif qty >= 11 and qty < 20:
                color = "#ffae42"        # sunset yellow
            else:
                color = "#4caf50"        # green
            bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {color}; }}")
            bar.setTextVisible(True)
            bar.setFormat(str(qty))
            return bar

        sample_rows = [
            ("1", "Milk 1L", 3, 1.20, 1.80, "N/A"),
            ("2", "Sugar 2kg", 25, 2.00, 3.00, "N/A"),
            ("3", "Yogurt", 50, 0.80, 1.50, "2025-10-01")
        ]
        self.table_stock.setRowCount(len(sample_rows))
        for r, (pk, name, qty, cost, sell, expiry) in enumerate(sample_rows):
            self.table_stock.setItem(r, 0, QtWidgets.QTableWidgetItem(pk))
            self.table_stock.setItem(r, 1, QtWidgets.QTableWidgetItem(name))
            self.table_stock.setCellWidget(r, 2, create_quantity_progress(int(qty)))
            self.table_stock.setItem(r, 3, QtWidgets.QTableWidgetItem(f"{cost:.2f}"))
            self.table_stock.setItem(r, 4, QtWidgets.QTableWidgetItem(f"{sell:.2f}"))
            self.table_stock.setItem(r, 5, QtWidgets.QTableWidgetItem(expiry))
            total_cost = qty * cost
            total_sell = qty * sell
            profit = total_sell - total_cost
            self.table_stock.setItem(r, 6, QtWidgets.QTableWidgetItem(f"{total_cost:.2f}"))
            self.table_stock.setItem(r, 7, QtWidgets.QTableWidgetItem(f"{total_sell:.2f}"))
            self.table_stock.setItem(r, 8, QtWidgets.QTableWidgetItem(f"{profit:.2f}"))

        retail_layout.addWidget(self.table_stock, stretch=1)  # ✅ extend downwards

        # Totals
        totals_widget = QtWidgets.QWidget()
        totals_h = QtWidgets.QHBoxLayout(totals_widget)
        totals_h.setContentsMargins(0, 0, 0, 0)
        totals_h.setSpacing(20)

        self.lbl_total_cost = QtWidgets.QLabel("Total Cost Price: 0.00")
        self.lbl_total_selling = QtWidgets.QLabel("Total Selling Price: 0.00")
        self.lbl_total_profit = QtWidgets.QLabel("Total Profit: 0.00")

        totals_h.addStretch()
        totals_h.addWidget(self.lbl_total_cost)
        totals_h.addWidget(self.lbl_total_selling)
        totals_h.addWidget(self.lbl_total_profit)
        retail_layout.addWidget(totals_widget)

        # === Wholesale Tab (placeholder for now) ===
        self.tab_wholesale = QtWidgets.QWidget()
        wholesale_layout = QtWidgets.QVBoxLayout(self.tab_wholesale)
        wholesale_layout.addWidget(QtWidgets.QLabel("Wholesale stock management coming soon..."))
        self.stock_tabs.addTab(self.tab_wholesale, "Wholesale")








        self.page_sales = QtWidgets.QLabel("🛒 Sales Page", alignment=QtCore.Qt.AlignCenter)
        self.page_report = QtWidgets.QLabel("📊 Report Page", alignment=QtCore.Qt.AlignCenter)


        # === Employees Page UI ===
        self.page_employees = QtWidgets.QWidget()
        employees_layout = QtWidgets.QVBoxLayout(self.page_employees)
        employees_layout.setContentsMargins(20, 20, 20, 20)
        employees_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(950)   # wider form for employees
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(35)
        form_layout.setVerticalSpacing(25)

        # Common label styling
        label_style = "color: black; font-weight: bold;"

        def create_field(label_text, widget, compulsory=False):
            """Helper: stack label + widget vertically with small spacing"""
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(4)
            lbl = QtWidgets.QLabel(label_text + (" *" if compulsory else ""))
            if compulsory:
                lbl.setStyleSheet("color: red; font-weight: bold;")
            else:
                lbl.setStyleSheet(label_style)
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # Name (compulsory)
        self.emp_name = QtWidgets.QLineEdit()
        self.emp_name.setPlaceholderText("Enter employee name")
        form_layout.addWidget(create_field("Name:", self.emp_name, compulsory=True), 0, 0, 1, 2)

        # Phone (compulsory)
        self.emp_phone = QtWidgets.QLineEdit()
        self.emp_phone.setPlaceholderText("Enter phone number")
        form_layout.addWidget(create_field("Phone:", self.emp_phone, compulsory=True), 0, 2, 1, 2)

        # Ghana Card ID (compulsory)
        self.emp_card = QtWidgets.QLineEdit()
        self.emp_card.setPlaceholderText("Enter Ghana card ID")
        form_layout.addWidget(create_field("Ghana Card ID:", self.emp_card, compulsory=True), 1, 0, 1, 2)

        # Address
        self.emp_address = QtWidgets.QLineEdit()
        self.emp_address.setPlaceholderText("Enter address")
        form_layout.addWidget(create_field("Address:", self.emp_address), 1, 2, 1, 2)

        # Designation
        self.emp_designation = QtWidgets.QLineEdit()
        self.emp_designation.setPlaceholderText("Enter designation (e.g. Sales Rep)")
        form_layout.addWidget(create_field("Designation:", self.emp_designation), 2, 0, 1, 2)

        # Salary
        self.emp_salary = QtWidgets.QLineEdit()
        self.emp_salary.setPlaceholderText("Enter salary")
        form_layout.addWidget(create_field("Salary:", self.emp_salary), 2, 2, 1, 2)

        # Register Button (centered, extended)
        self.btn_add_employee = QtWidgets.QPushButton("Add Employee")
        self.btn_add_employee.setObjectName("registerButton")   # keeps original register button style
        self.btn_add_employee.setFixedWidth(int(form_container.width() * 0.5))
        form_layout.addWidget(self.btn_add_employee, 3, 0, 1, 4, alignment=QtCore.Qt.AlignCenter)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        employees_layout.addLayout(form_wrapper)

        # === Filter Section ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)

        self.btn_filter = QtWidgets.QPushButton("Filter")
        self.btn_filter.setObjectName("primaryButton")

        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText("Filter by Phone or Ghana Card ID...")
        self.filter_input.setFixedWidth(int(form_container.width() * 0.3))  # 30% width of form

        # Add button first, then input, aligned to left
        filter_container.addWidget(self.btn_filter)
        filter_container.addWidget(self.filter_input)
        filter_container.addStretch()  # pushes everything to the left

        employees_layout.addLayout(filter_container)


        # === Table Section ===
        self.table_employees = QtWidgets.QTableWidget()
        self.table_employees.setColumnCount(8)  # Removed Actions column
        self.table_employees.setHorizontalHeaderLabels([
            "ID", "Name", "Phone", "Ghana Card ID", "Address", "Designation", "Salary", "Date Added"
        ])
        self.table_employees.horizontalHeader().setStretchLastSection(True)
        self.table_employees.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # ✅ Enable editing on double-click
        self.table_employees.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)

        self.table_employees.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_employees.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_employees.setAlternatingRowColors(True)
        self.table_employees.verticalHeader().setVisible(False)

        # Sample employee data
        employees_data = [
            (1, "John Doe", "0244000011", "GHA-123456789", "Accra", "Cashier", "1500", "2025-08-01"),
            (2, "Mary Jane", "0244000022", "GHA-987654321", "Kumasi", "Manager", "3500", "2025-08-10"),
            (3, "Peter Mensah", "0244000033", "GHA-555111222", "Takoradi", "Sales Rep", "2000", "2025-08-20")
        ]

        self.table_employees.setRowCount(len(employees_data))

        for row, (uid, name, phone, card, addr, desig, salary, date) in enumerate(employees_data):
            self.table_employees.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_employees.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_employees.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
            self.table_employees.setItem(row, 3, QtWidgets.QTableWidgetItem(card))
            self.table_employees.setItem(row, 4, QtWidgets.QTableWidgetItem(addr))
            self.table_employees.setItem(row, 5, QtWidgets.QTableWidgetItem(desig))
            self.table_employees.setItem(row, 6, QtWidgets.QTableWidgetItem(salary))
            self.table_employees.setItem(row, 7, QtWidgets.QTableWidgetItem(date))

        employees_layout.addWidget(self.table_employees)





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
