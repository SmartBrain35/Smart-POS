from PySide6 import QtCore, QtGui, QtWidgets


class Ui_AdminDashboard(object):
    def setupUi(self, AdminDashboard):
        AdminDashboard.setObjectName("AdminDashboard")
        AdminDashboard.setMinimumSize(1200, 800)
        AdminDashboard.showMaximized()

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

        self.page_dashboard = QtWidgets.QLabel(
            "Welcome to Smart POS Dashboard", alignment=QtCore.Qt.AlignCenter
        )
        self.page_dashboard.setStyleSheet("font-size: 24px; font-weight: bold;")

        # === Stock Page UI with Tabs(Retail / Wholesale) ===
        self.page_stock = QtWidgets.QWidget()
        stock_layout = QtWidgets.QVBoxLayout(self.page_stock)
        stock_layout.setContentsMargins(10, 10, 10, 0)
        stock_layout.setSpacing(1)

        # --- Centered Tabs (now full width) ---
        self.stock_tabs = QtWidgets.QTabWidget()
        self.stock_tabs.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        stock_layout.addWidget(self.stock_tabs)

        # --- Table ---
        self.table_stock = QtWidgets.QTableWidget()
        self.table_stock.setColumnCount(9)
        self.table_stock.setHorizontalHeaderLabels(
            [
                "ID",
                "Item Name",
                "Quantity",
                "Cost Price",
                "Selling Price",
                "Expiry",
                "Total Cost",
                "Total Selling",
                "Profit",
            ]
        )
        self.table_stock.horizontalHeader().setStretchLastSection(True)
        self.table_stock.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_stock.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_stock.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_stock.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_stock.setAlternatingRowColors(True)
        self.table_stock.verticalHeader().setVisible(False)

        # Apply tab styling
        self.stock_tabs.setStyleSheet(
            """
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
        """
        )

        # === Retail Tab ===
        self.tab_retail = QtWidgets.QWidget()
        self.retail_layout = QtWidgets.QVBoxLayout(self.tab_retail)
        self.retail_layout.setSpacing(12)
        self.stock_tabs.addTab(self.tab_retail, "RETAIL")

        # ------------------- FORM CONTAINER -------------------
        form_container = QtWidgets.QWidget()
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(25)

        label_style = "color: black; font-weight: bold;"

        def vfield(label_text, widget):
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(4)
            lbl = QtWidgets.QLabel(label_text)
            lbl.setStyleSheet(label_style)
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # ID
        self.stock_id_input = QtWidgets.QLineEdit()
        self.stock_id_input.setPlaceholderText("Auto / Enter ID")
        self.stock_id_input.setObjectName("inputRetailId")
        form_layout.addWidget(vfield("ID:", self.stock_id_input), 0, 0)

        # Item Name
        self.stock_name_input = QtWidgets.QLineEdit()
        self.stock_name_input.setPlaceholderText("Enter item name")
        self.stock_name_input.setObjectName("inputRetailName")
        form_layout.addWidget(vfield("Item Name:", self.stock_name_input), 0, 1)

        # Quantity
        self.stock_qty_input = QtWidgets.QLineEdit()
        self.stock_qty_input.setPlaceholderText("Enter quantity (integer)")
        self.stock_qty_input.setObjectName("inputRetailQty")
        form_layout.addWidget(vfield("Quantity:", self.stock_qty_input), 0, 2)

        # Cost Price
        self.stock_cost_input = QtWidgets.QLineEdit()
        self.stock_cost_input.setPlaceholderText("Unit cost price")
        self.stock_cost_input.setObjectName("inputRetailCost")
        form_layout.addWidget(vfield("Cost Price:", self.stock_cost_input), 1, 0)

        # Selling Price
        self.stock_selling_input = QtWidgets.QLineEdit()
        self.stock_selling_input.setPlaceholderText("Unit selling price")
        self.stock_selling_input.setObjectName("inputRetailSelling")
        form_layout.addWidget(vfield("Selling Price:", self.stock_selling_input), 1, 1)

        # Expiry date + checkbox
        self.stock_expiry_checkbox = QtWidgets.QCheckBox("")
        self.stock_expiry_checkbox.setFixedWidth(18)
        self.stock_expiry_date = QtWidgets.QDateEdit()
        self.stock_expiry_date.setCalendarPopup(True)
        self.stock_expiry_date.setDate(QtCore.QDate.currentDate())
        self.stock_expiry_date.setEnabled(False)
        self.stock_expiry_checkbox.toggled.connect(self.stock_expiry_date.setEnabled)
        self.stock_expiry_checkbox.setObjectName("checkRetailExpiry")
        expire_widget = QtWidgets.QWidget()
        expire_h = QtWidgets.QHBoxLayout(expire_widget)
        expire_h.setContentsMargins(0, 0, 0, 0)
        expire_h.setSpacing(4)
        expire_h.addWidget(self.stock_expiry_checkbox)
        expire_h.addWidget(self.stock_expiry_date)

        self.stock_expiry_date.setObjectName("dateRetailExpiry")
        form_layout.addWidget(vfield("Expire Date:", expire_widget), 1, 2)

        # Category
        self.stock_category_input = QtWidgets.QComboBox()
        self.stock_category_input.setObjectName("inputRetailCategory")
        self.stock_category_input.addItems(["Retail", "Wholesale"])
        form_layout.addWidget(vfield("Category:", self.stock_category_input), 2, 0)

        # --- Action Buttons ---
        btn_container = QtWidgets.QWidget()
        btn_h = QtWidgets.QHBoxLayout(btn_container)
        btn_h.setContentsMargins(0, 0, 0, 0)
        btn_h.setSpacing(10)

        self.btn_add_stock = QtWidgets.QPushButton("ADD")
        self.btn_add_stock.setObjectName("btnRetailAdd")

        self.btn_edit_stock = QtWidgets.QPushButton("EDIT")
        self.btn_edit_stock.setObjectName("btnRetailEdit")

        self.btn_delete_stock = QtWidgets.QPushButton("DELETE")
        self.btn_delete_stock.setObjectName("btnRetailDelete")

        self.btn_clear_stock = QtWidgets.QPushButton("CLEAR")
        self.btn_clear_stock.setObjectName("btnRetailClear")

        for btn in [
            self.btn_add_stock,
            self.btn_edit_stock,
            self.btn_delete_stock,
            self.btn_clear_stock,
        ]:
            btn.setMinimumWidth(90)
            btn_h.addWidget(btn)

        form_layout.addWidget(btn_container, 2, 1, 1, 2)

        # ------------------- CONTENT CONTAINER -------------------
        content_container = QtWidgets.QWidget()
        content_v = QtWidgets.QVBoxLayout(content_container)
        content_v.setContentsMargins(0, 0, 0, 0)
        content_v.setSpacing(6)

        # --- Filter ---
        filter_h = QtWidgets.QHBoxLayout()
        filter_h.setContentsMargins(0, 0, 0, 0)
        filter_h.setSpacing(3)

        self.stock_filter_input = QtWidgets.QLineEdit()
        self.stock_filter_input.setPlaceholderText("Filter by item name or category...")
        filter_h.addWidget(self.stock_filter_input)
        self.stock_filter_input.setObjectName("inputRetailFilter")

        self.btn_filter_stock = QtWidgets.QPushButton("Search")
        self.btn_filter_stock.setObjectName("btnRetailFilter")

        filter_h.addWidget(self.btn_filter_stock)
        content_v.addLayout(filter_h)

        # --- Table ---
        self.table_stock = QtWidgets.QTableWidget()
        self.table_stock.setObjectName("RetailTable")
        self.table_stock.setColumnCount(7)
        self.table_stock.setHorizontalHeaderLabels(
            [
                "ID",
                "Item Name",
                "Quantity",
                "Cost Price",
                "Selling Price",
                "Expire Date",
                "Category",
            ]
        )
        self.table_stock.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_stock.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.table_stock.setAlternatingRowColors(True)
        self.table_stock.horizontalHeader().setStretchLastSection(True)
        self.table_stock.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_stock.setMinimumHeight(280)

        content_v.addWidget(self.table_stock, stretch=1)

        # --- LCD Totals (Labels beside LCDs) ---
        lcds_widget = QtWidgets.QWidget()
        lcd_h = QtWidgets.QHBoxLayout(lcds_widget)
        lcd_h.setContentsMargins(0, 0, 0, 0)
        lcd_h.setSpacing(0)

        def lcd_box(title):
            wrapper = QtWidgets.QWidget()
            hbox = QtWidgets.QHBoxLayout(wrapper)
            hbox.setContentsMargins(0, 0, 0, 0)
            hbox.setSpacing(0)

            lbl = QtWidgets.QLabel(title)
            lbl.setStyleSheet("font-weight: bold; color: black;")
            lbl.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

            lcd = QtWidgets.QLCDNumber()
            lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            lcd.setFixedWidth(150)
            lcd.display("0.00")

            hbox.addWidget(lbl)
            hbox.addWidget(lcd)
            return wrapper, lcd

        # total cost
        box_cost, self.lcd_total_cost = lcd_box("Total Cost Price:")
        self.lcd_total_cost.setObjectName("lcdRetailTotalCost")
        lcd_h.addWidget(box_cost)

        # total selling
        box_sell, self.lcd_total_selling = lcd_box("Total Selling Price:")
        self.lcd_total_selling.setObjectName("lcdRetailTotalSelling")
        lcd_h.addWidget(box_sell)

        # total profit
        box_profit, self.lcd_total_profit = lcd_box("Total Profit:")
        self.lcd_total_profit.setObjectName("lcdRetailTotalProfit")
        lcd_h.addWidget(box_profit)

        content_v.addWidget(lcds_widget, stretch=0)

        # ------------------- MAIN LAYOUT -------------------
        self.retail_layout.addWidget(
            form_container, stretch=0, alignment=QtCore.Qt.AlignTop
        )
        self.retail_layout.addWidget(content_container, stretch=1)
        
        # === Wholesale Tab Ui ===
        self.tab_wholesale = QtWidgets.QWidget()
        wholesale_layout = QtWidgets.QVBoxLayout(self.tab_wholesale)
        wholesale_layout.setContentsMargins(10, 10, 10, 0)
        wholesale_layout.setSpacing(10)

        # ======================================================
        # TOP CONTAINER (Form + Buttons together)
        # ======================================================
        form_buttons_container = QtWidgets.QWidget()
        form_buttons_layout = QtWidgets.QGridLayout(form_buttons_container)
        form_buttons_layout.setContentsMargins(0, 0, 0, 0)
        form_buttons_layout.setHorizontalSpacing(20)
        form_buttons_layout.setVerticalSpacing(10)

        # ID
        self.ws_id = QtWidgets.QLineEdit()
        self.ws_id.setObjectName("inputWholesaleId")
        lbl_id = QtWidgets.QLabel("ID:")
        lbl_id.setObjectName("labelWholesaleId")
        form_buttons_layout.addWidget(lbl_id, 0, 0)
        form_buttons_layout.addWidget(self.ws_id, 0, 1)

        # Item Name
        self.ws_name = QtWidgets.QLineEdit()
        self.ws_name.setObjectName("inputWholesaleName")
        lbl_name = QtWidgets.QLabel("Item Name:")
        lbl_name.setObjectName("labelWholesaleName")
        form_buttons_layout.addWidget(lbl_name, 0, 2)
        form_buttons_layout.addWidget(self.ws_name, 0, 3)

        # Quantity
        self.ws_qty = QtWidgets.QLineEdit()
        self.ws_qty.setObjectName("inputWholesaleQty")
        lbl_qty = QtWidgets.QLabel("Quantity:")
        lbl_qty.setObjectName("labelWholesaleQty")
        form_buttons_layout.addWidget(lbl_qty, 0, 4)
        form_buttons_layout.addWidget(self.ws_qty, 0, 5)

        # Cost Price
        self.ws_cost = QtWidgets.QLineEdit()
        self.ws_cost.setObjectName("inputWholesaleCost")
        lbl_cost = QtWidgets.QLabel("Cost Price:")
        lbl_cost.setObjectName("labelWholesaleCost")
        form_buttons_layout.addWidget(lbl_cost, 1, 0)
        form_buttons_layout.addWidget(self.ws_cost, 1, 1)

        # Selling Price
        self.ws_selling = QtWidgets.QLineEdit()
        self.ws_selling.setObjectName("inputWholesaleSelling")
        lbl_selling = QtWidgets.QLabel("Selling Price:")
        lbl_selling.setObjectName("labelWholesaleSelling")
        form_buttons_layout.addWidget(lbl_selling, 1, 2)
        form_buttons_layout.addWidget(self.ws_selling, 1, 3)

        # Expiry (label + checkbox + date)
        lbl_expiry = QtWidgets.QLabel("Expire:")
        lbl_expiry.setObjectName("labelWholesaleExpiry")

        expiry_container = QtWidgets.QHBoxLayout()
        expiry_container.setContentsMargins(0, 0, 0, 0)
        expiry_container.setSpacing(5)

        self.ws_expiry_checkbox = QtWidgets.QCheckBox()
        self.ws_expiry_checkbox.setObjectName("checkWholesaleExpiry")
        self.ws_expiry_checkbox.setText("")  # only box, no text
        self.ws_expiry_checkbox.setFixedWidth(20)

        self.ws_expiry_date = QtWidgets.QDateEdit()
        self.ws_expiry_date.setObjectName("dateWholesaleExpiry")
        self.ws_expiry_date.setCalendarPopup(True)
        self.ws_expiry_date.setFixedHeight(self.ws_id.sizeHint().height())
        self.ws_expiry_date.setFixedWidth(int(self.ws_id.sizeHint().width() * 0.8))

        expiry_container.addWidget(self.ws_expiry_checkbox)
        expiry_container.addWidget(self.ws_expiry_date)

        expiry_widget = QtWidgets.QWidget()
        expiry_widget.setLayout(expiry_container)

        form_buttons_layout.addWidget(lbl_expiry, 1, 4)
        form_buttons_layout.addWidget(expiry_widget, 1, 5)

        # Category (changed to ComboBox)
        self.ws_category = QtWidgets.QComboBox()
        self.ws_category.setObjectName("inputWholesaleCategory")
        self.ws_category.addItems(["Retail", "Wholesale"])
        lbl_category = QtWidgets.QLabel("Category:")
        lbl_category.setObjectName("labelWholesaleCategory")
        form_buttons_layout.addWidget(lbl_category, 2, 0)
        form_buttons_layout.addWidget(self.ws_category, 2, 1)

        # Buttons (equal width + centered text)
        self.ws_btn_add = QtWidgets.QPushButton("ADD")
        self.ws_btn_add.setObjectName("btnWholesaleAdd")
        self.ws_btn_edit = QtWidgets.QPushButton("EDIT")
        self.ws_btn_edit.setObjectName("btnWholesaleEdit")
        self.ws_btn_delete = QtWidgets.QPushButton("DELETE")
        self.ws_btn_delete.setObjectName("btnWholesaleDelete")
        self.ws_btn_clear = QtWidgets.QPushButton("CLEAR")
        self.ws_btn_clear.setObjectName("btnWholesaleClear")

        btns = [
            self.ws_btn_add,
            self.ws_btn_edit,
            self.ws_btn_delete,
            self.ws_btn_clear,
        ]
        for b in btns:
            b.setMinimumWidth(100)

        btn_widget = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(10)
        btn_layout.addStretch()
        [btn_layout.addWidget(b) for b in btns]
        btn_layout.addStretch()

        form_buttons_layout.addWidget(btn_widget, 2, 2, 1, 4)
        wholesale_layout.addWidget(form_buttons_container)

        # ======================================================
        # BOTTOM CONTAINER (Filter + Table + LCD)
        # ======================================================
        bottom_container = QtWidgets.QVBoxLayout()
        bottom_container.setContentsMargins(0, 0, 0, 0)
        bottom_container.setSpacing(10)

        # Filter bar
        filter_widget = QtWidgets.QWidget()
        filter_layout = QtWidgets.QHBoxLayout(filter_widget)
        filter_layout.setContentsMargins(0, 0, 0, 0)

        self.ws_txt_filter = QtWidgets.QLineEdit()
        self.ws_txt_filter.setObjectName("inputWholesaleFilter")
        self.ws_txt_filter.setPlaceholderText("Filter by item name...")
        self.ws_txt_filter.setMaximumWidth(int(self.tab_wholesale.width() * 0.5))

        filter_layout.addStretch()
        filter_layout.addWidget(self.ws_txt_filter)

        bottom_container.addWidget(filter_widget)

        # Wholesale Table
        self.ws_table_stock = QtWidgets.QTableWidget()
        self.ws_table_stock.setObjectName("WholesaleTable")
        self.ws_table_stock.setColumnCount(10)
        self.ws_table_stock.setHorizontalHeaderLabels(
            [
                "ID",
                "Item Name",
                "Category",
                "Quantity",
                "Cost Price",
                "Selling Price",
                "Expired",
                "Total Cost",
                "Total Selling",
                "Profit",
            ]
        )

        self.ws_table_stock.setMinimumHeight(300)
        self.ws_table_stock.verticalHeader().setDefaultSectionSize(30)
        self.ws_table_stock.horizontalHeader().setStretchLastSection(False)

        self.ws_table_stock.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        bottom_container.addWidget(self.ws_table_stock, stretch=10)

        # LCD row
        lcd_widget = QtWidgets.QWidget()
        lcd_layout = QtWidgets.QHBoxLayout(lcd_widget)
        lcd_layout.setContentsMargins(0, 0, 0, 5)
        lcd_layout.setSpacing(15)

        def make_lcd_block(label_text, obj_name):
            container = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setObjectName(obj_name + "Label")
            label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

            lcd = QtWidgets.QLCDNumber()
            lcd.setObjectName(obj_name)
            lcd.setDigitCount(10)
            lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            lcd.setMinimumHeight(40)
            lcd.setMinimumWidth(120)
            lcd.display("0.00")

            container.addWidget(label)
            container.addWidget(lcd)
            return container, lcd

        cost_block, self.ws_lcd_total_cost = make_lcd_block("Total Cost Value:", "lcdWholesaleCost")
        selling_block, self.ws_lcd_total_selling = make_lcd_block("Total Selling Value:", "lcdWholesaleSelling")
        profit_block, self.ws_lcd_total_profit = make_lcd_block("Total Profit:", "lcdWholesaleProfit")

        lcd_layout.addLayout(cost_block)
        lcd_layout.addLayout(selling_block)
        lcd_layout.addLayout(profit_block)

        bottom_container.addWidget(lcd_widget, stretch=0)
        wholesale_layout.addLayout(bottom_container, stretch=1)

        # Add wholesale tab
        self.stock_tabs.addTab(self.tab_wholesale, "WHOLESALE")


        self.page_sales = QtWidgets.QLabel(
            "🛒 Sales Page", alignment=QtCore.Qt.AlignCenter
        )
        self.page_report = QtWidgets.QLabel(
            "📊 Report Page", alignment=QtCore.Qt.AlignCenter
        )

        # === Employees Page UI ===
        self.page_employees = QtWidgets.QWidget()
        employees_layout = QtWidgets.QVBoxLayout(self.page_employees)
        employees_layout.setContentsMargins(20, 20, 20, 20)
        employees_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(950)  # wider form for employees
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
        form_layout.addWidget(
            create_field("Name:", self.emp_name, compulsory=True), 0, 0, 1, 2
        )

        # Phone (compulsory)
        self.emp_phone = QtWidgets.QLineEdit()
        self.emp_phone.setPlaceholderText("Enter phone number")
        form_layout.addWidget(
            create_field("Phone:", self.emp_phone, compulsory=True), 0, 2, 1, 2
        )

        # Ghana Card ID (compulsory)
        self.emp_card = QtWidgets.QLineEdit()
        self.emp_card.setPlaceholderText("Enter Ghana card ID")
        form_layout.addWidget(
            create_field("Ghana Card ID:", self.emp_card, compulsory=True), 1, 0, 1, 2
        )

        # Address
        self.emp_address = QtWidgets.QLineEdit()
        self.emp_address.setPlaceholderText("Enter address")
        form_layout.addWidget(create_field("Address:", self.emp_address), 1, 2, 1, 2)

        # Designation
        self.emp_designation = QtWidgets.QLineEdit()
        self.emp_designation.setPlaceholderText("Enter designation (e.g. Sales Rep)")
        form_layout.addWidget(
            create_field("Designation:", self.emp_designation), 2, 0, 1, 2
        )

        # Salary
        self.emp_salary = QtWidgets.QLineEdit()
        self.emp_salary.setPlaceholderText("Enter salary")
        form_layout.addWidget(create_field("Salary:", self.emp_salary), 2, 2, 1, 2)

        # Register Button (centered, extended)
        self.btn_add_employee = QtWidgets.QPushButton("Add Employee")
        self.btn_add_employee.setObjectName(
            "registerButton"
        )  # keeps original register button style
        self.btn_add_employee.setFixedWidth(int(form_container.width() * 0.5))
        form_layout.addWidget(
            self.btn_add_employee, 3, 0, 1, 4, alignment=QtCore.Qt.AlignCenter
        )

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
        self.filter_input.setFixedWidth(
            int(form_container.width() * 0.3)
        )  # 30% width of form

        # Add button first, then input, aligned to left
        filter_container.addWidget(self.btn_filter)
        filter_container.addWidget(self.filter_input)
        filter_container.addStretch()  # pushes everything to the left

        employees_layout.addLayout(filter_container)

        # === Table Section ===
        self.table_employees = QtWidgets.QTableWidget()
        self.table_employees.setColumnCount(8)  # Removed Actions column
        self.table_employees.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Phone",
                "Ghana Card ID",
                "Address",
                "Designation",
                "Salary",
                "Date Added",
            ]
        )
        self.table_employees.horizontalHeader().setStretchLastSection(True)
        self.table_employees.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        # ✅ Enable editing on double-click
        self.table_employees.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)

        self.table_employees.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table_employees.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.table_employees.setAlternatingRowColors(True)
        self.table_employees.verticalHeader().setVisible(False)

        # Sample employee data
        employees_data = [
            (
                1,
                "John Doe",
                "0244000011",
                "GHA-123456789",
                "Accra",
                "Cashier",
                "1500",
                "2025-08-01",
            ),
            (
                2,
                "Mary Jane",
                "0244000022",
                "GHA-987654321",
                "Kumasi",
                "Manager",
                "3500",
                "2025-08-10",
            ),
            (
                3,
                "Peter Mensah",
                "0244000033",
                "GHA-555111222",
                "Takoradi",
                "Sales Rep",
                "2000",
                "2025-08-20",
            ),
        ]

        self.table_employees.setRowCount(len(employees_data))

        for row, (uid, name, phone, card, addr, desig, salary, date) in enumerate(
            employees_data
        ):
            self.table_employees.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_employees.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_employees.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
            self.table_employees.setItem(row, 3, QtWidgets.QTableWidgetItem(card))
            self.table_employees.setItem(row, 4, QtWidgets.QTableWidgetItem(addr))
            self.table_employees.setItem(row, 5, QtWidgets.QTableWidgetItem(desig))
            self.table_employees.setItem(row, 6, QtWidgets.QTableWidgetItem(salary))
            self.table_employees.setItem(row, 7, QtWidgets.QTableWidgetItem(date))

        employees_layout.addWidget(self.table_employees)

        self.page_return = QtWidgets.QLabel(
            "↩ Return Page", alignment=QtCore.Qt.AlignCenter
        )
        self.page_damage = QtWidgets.QLabel(
            "💥 Damage Page", alignment=QtCore.Qt.AlignCenter
        )
        self.page_expenditure = QtWidgets.QLabel(
            "💵 Expenditure Page", alignment=QtCore.Qt.AlignCenter
        )

        # === Account Page UI ===
        self.page_account = QtWidgets.QWidget()
        account_layout = QtWidgets.QVBoxLayout(self.page_account)
        account_layout.setContentsMargins(20, 20, 20, 20)
        account_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(850)  # wider form
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(35)  # space between columns
        form_layout.setVerticalSpacing(25)  # space between field groups

        # Common label styling
        label_style = "color: black; font-weight: bold;"

        def create_field(label_text, widget):
            """Helper: stack label + widget vertically with small spacing"""
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(4)  # << reduce gap label-input here
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
        form_layout.addWidget(
            create_field("Password:", self.input_password), 2, 0, 1, 2
        )

        # Role
        self.input_role = QtWidgets.QComboBox()
        self.input_role.addItems(["Admin", "Manager", "Cashier", "Sales Person"])
        self.input_role.setMinimumWidth(int(form_container.width() * 0.4))
        form_layout.addWidget(create_field("Role:", self.input_role), 2, 2, 1, 2)

        # Register Button (centered, extended)
        self.btn_register = QtWidgets.QPushButton("Register User")
        self.btn_register.setObjectName("primaryButton")
        self.btn_register.setFixedWidth(int(form_container.width() * 0.5))
        form_layout.addWidget(
            self.btn_register, 3, 0, 1, 4, alignment=QtCore.Qt.AlignCenter
        )
        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        account_layout.addLayout(form_wrapper)

        # === Table Section ===
        self.table_users = QtWidgets.QTableWidget()
        self.table_users.setColumnCount(7)  # Removed Ghana Card column
        self.table_users.setHorizontalHeaderLabels(
            ["ID", "Name", "Phone", "Email", "Role", "Status", "Actions"]
        )
        self.table_users.horizontalHeader().setStretchLastSection(True)
        self.table_users.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_users.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_users.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_users.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_users.setAlternatingRowColors(True)
        self.table_users.verticalHeader().setVisible(False)

        # Sample data (without Ghana Card)
        users_data = [
            (1, "Admin User", "0244000001", "admin@pos.com", "Admin", "Active"),
            (2, "Cashier One", "0244000002", "cashier@pos.com", "Cashier", "Active"),
            (3, "Manager One", "0244000003", "manager@pos.com", "Manager", "Inactive"),
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

        self.page_settings = QtWidgets.QLabel(
            "🔧 Settings Page", alignment=QtCore.Qt.AlignCenter
        )

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

        AdminDashboard.setCentralWidget(self.centralwidget)
        self.retranslateUi(AdminDashboard)
        QtCore.QMetaObject.connectSlotsByName(AdminDashboard)

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
