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
        self.stock_id_input.setFixedHeight(40)
        form_layout.addWidget(vfield("ID:", self.stock_id_input), 0, 0)

        # Item Name
        self.stock_name_input = QtWidgets.QLineEdit()
        self.stock_name_input.setPlaceholderText("Enter item name")
        self.stock_name_input.setObjectName("inputRetailName")
        self.stock_name_input.setFixedHeight(40)
        form_layout.addWidget(vfield("Item Name:", self.stock_name_input), 0, 1)

        # Quantity
        self.stock_qty_input = QtWidgets.QLineEdit()
        self.stock_qty_input.setPlaceholderText("Enter quantity (integer)")
        self.stock_qty_input.setObjectName("inputRetailQty")
        self.stock_qty_input.setFixedHeight(40)
        form_layout.addWidget(vfield("Quantity:", self.stock_qty_input), 0, 2)

        # Cost Price
        self.stock_cost_input = QtWidgets.QLineEdit()
        self.stock_cost_input.setPlaceholderText("Unit cost price")
        self.stock_cost_input.setObjectName("inputRetailCost")
        self.stock_cost_input.setFixedHeight(40)
        form_layout.addWidget(vfield("Cost Price:", self.stock_cost_input), 1, 0)

        # Selling Price
        self.stock_selling_input = QtWidgets.QLineEdit()
        self.stock_selling_input.setPlaceholderText("Unit selling price")
        self.stock_selling_input.setObjectName("inputRetailSelling")
        self.stock_selling_input.setFixedHeight(40)
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
        self.stock_expiry_date.setFixedHeight(40)
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
        self.stock_category_input.setFixedHeight(40)
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
        content_v.setSpacing(12)

        # --- Filter Row ---
        filter_h = QtWidgets.QHBoxLayout()
        filter_h.setContentsMargins(0, 0, 0, 0)
        filter_h.setSpacing(6)

        self.stock_filter_input = QtWidgets.QLineEdit()
        self.stock_filter_input.setPlaceholderText("Filter by item name or category...")
        self.stock_filter_input.setObjectName("inputRetailFilter")
        self.stock_filter_input.setFixedHeight(40)
        filter_h.addWidget(self.stock_filter_input, stretch=1)

        self.btn_filter_stock = QtWidgets.QPushButton("Search")
        self.btn_filter_stock.setObjectName("btnRetailFilter")
        self.btn_filter_stock.setFixedHeight(40)
        self.btn_filter_stock.setFixedWidth(120)
        filter_h.addWidget(self.btn_filter_stock)

        content_v.addLayout(filter_h)

        # --- Table + LCDs side by side ---
        table_lcd_h = QtWidgets.QHBoxLayout()
        table_lcd_h.setContentsMargins(0, 0, 0, 0)
        table_lcd_h.setSpacing(4)  # 🔹 very small gap between table and LCDs

        # Table
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
        self.table_stock.setMinimumHeight(300)
        self.table_stock.setMaximumWidth(920)

        # LCDs on right (stacked vertically with labels)
        lcds_container = QtWidgets.QWidget()
        lcds_v = QtWidgets.QVBoxLayout(lcds_container)
        lcds_v.setContentsMargins(0, 0, 0, 0)
        lcds_v.setSpacing(12)  # keep space between LCD blocks

        def make_lcd(title, obj_name):
            """Helper to build label + LCD pair with QSS objectName"""
            lcd = QtWidgets.QLCDNumber()
            lcd.setObjectName(obj_name)
            lcd.setDigitCount(7)
            lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            lcd.setFixedWidth(180)
            lcd.setFixedHeight(60)

            lbl = QtWidgets.QLabel(title)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 13pt; font-weight: bold;")

            box = QtWidgets.QVBoxLayout()
            box.setSpacing(4)  # small gap between label & LCD
            box.addWidget(lbl)
            box.addWidget(lcd)
            return box, lcd

        # --- Total Cost Price ---
        box_cost, self.lcd_total_cost = make_lcd(
            "Total Cost Price", "lcdRetailTotalCost"
        )
        lcds_v.addLayout(box_cost)

        # --- Total Selling Price ---
        box_sell, self.lcd_total_selling = make_lcd(
            "Total Selling Price", "lcdRetailTotalSelling"
        )
        lcds_v.addLayout(box_sell)

        # --- Total Profit ---
        box_profit, self.lcd_total_profit = make_lcd(
            "Total Profit", "lcdRetailTotalProfit"
        )
        lcds_v.addLayout(box_profit)

        # 🔹 Add *only once* to horizontal layout
        table_lcd_h.addWidget(self.table_stock, stretch=2)
        table_lcd_h.addWidget(
            lcds_container, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
        )

        # 🔹 Finally, add the table + lcds layout into content container
        content_v.addLayout(table_lcd_h)

        # ------------------- MAIN LAYOUT -------------------
        self.retail_layout.addWidget(
            form_container, stretch=0, alignment=QtCore.Qt.AlignTop
        )
        self.retail_layout.addWidget(content_container, stretch=1)

        # === Wholesale Tab ===
        self.tab_wholesale = QtWidgets.QWidget()
        self.wholesale_layout = QtWidgets.QVBoxLayout(self.tab_wholesale)
        self.wholesale_layout.setSpacing(12)
        self.stock_tabs.addTab(self.tab_wholesale, "WHOLESALE")

        # ------------------- FORM CONTAINER -------------------
        form_container_w = QtWidgets.QWidget()
        form_layout_w = QtWidgets.QGridLayout(form_container_w)
        form_layout_w.setContentsMargins(10, 10, 10, 10)
        form_layout_w.setVerticalSpacing(10)
        form_layout_w.setHorizontalSpacing(25)

        label_style = "color: black; font-weight: bold;"

        def vfield_w(label_text, widget):
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
        self.wholesale_id_input = QtWidgets.QLineEdit()
        self.wholesale_id_input.setPlaceholderText("Auto / Enter ID")
        self.wholesale_id_input.setObjectName("inputWholesaleId")
        self.wholesale_id_input.setFixedHeight(40)
        form_layout_w.addWidget(vfield_w("ID:", self.wholesale_id_input), 0, 0)

        # Item Name
        self.wholesale_name_input = QtWidgets.QLineEdit()
        self.wholesale_name_input.setPlaceholderText("Enter item name")
        self.wholesale_name_input.setObjectName("inputWholesaleName")
        self.wholesale_name_input.setFixedHeight(40)
        form_layout_w.addWidget(vfield_w("Item Name:", self.wholesale_name_input), 0, 1)

        # Quantity
        self.wholesale_qty_input = QtWidgets.QLineEdit()
        self.wholesale_qty_input.setPlaceholderText("Enter quantity (integer)")
        self.wholesale_qty_input.setObjectName("inputWholesaleQty")
        self.wholesale_qty_input.setFixedHeight(40)
        form_layout_w.addWidget(vfield_w("Quantity:", self.wholesale_qty_input), 0, 2)

        # Cost Price
        self.wholesale_cost_input = QtWidgets.QLineEdit()
        self.wholesale_cost_input.setPlaceholderText("Unit cost price")
        self.wholesale_cost_input.setObjectName("inputWholesaleCost")
        self.wholesale_cost_input.setFixedHeight(40)
        form_layout_w.addWidget(vfield_w("Cost Price:", self.wholesale_cost_input), 1, 0)

        # Selling Price
        self.wholesale_selling_input = QtWidgets.QLineEdit()
        self.wholesale_selling_input.setPlaceholderText("Unit selling price")
        self.wholesale_selling_input.setObjectName("inputWholesaleSelling")
        self.wholesale_selling_input.setFixedHeight(40)
        form_layout_w.addWidget(vfield_w("Selling Price:", self.wholesale_selling_input), 1, 1)

        # Expiry date + checkbox
        self.wholesale_expiry_checkbox = QtWidgets.QCheckBox("")
        self.wholesale_expiry_checkbox.setFixedWidth(18)
        self.wholesale_expiry_date = QtWidgets.QDateEdit()
        self.wholesale_expiry_date.setCalendarPopup(True)
        self.wholesale_expiry_date.setDate(QtCore.QDate.currentDate())
        self.wholesale_expiry_date.setEnabled(False)
        self.wholesale_expiry_checkbox.toggled.connect(self.wholesale_expiry_date.setEnabled)
        self.wholesale_expiry_checkbox.setObjectName("checkWholesaleExpiry")
        self.wholesale_expiry_date.setFixedHeight(40)
        expire_widget_w = QtWidgets.QWidget()
        expire_h_w = QtWidgets.QHBoxLayout(expire_widget_w)
        expire_h_w.setContentsMargins(0, 0, 0, 0)
        expire_h_w.setSpacing(4)
        expire_h_w.addWidget(self.wholesale_expiry_checkbox)
        expire_h_w.addWidget(self.wholesale_expiry_date)

        self.wholesale_expiry_date.setObjectName("dateWholesaleExpiry")
        form_layout_w.addWidget(vfield_w("Expire Date:", expire_widget_w), 1, 2)

        # Category
        self.wholesale_category_input = QtWidgets.QComboBox()
        self.wholesale_category_input.setObjectName("inputWholesaleCategory")
        self.wholesale_category_input.setFixedHeight(40)
        self.wholesale_category_input.addItems(["Retail", "Wholesale"])
        form_layout_w.addWidget(vfield_w("Category:", self.wholesale_category_input), 2, 0)

        # --- Action Buttons ---
        btn_container_w = QtWidgets.QWidget()
        btn_h_w = QtWidgets.QHBoxLayout(btn_container_w)
        btn_h_w.setContentsMargins(0, 0, 0, 0)
        btn_h_w.setSpacing(10)

        self.btn_add_wholesale = QtWidgets.QPushButton("ADD")
        self.btn_add_wholesale.setObjectName("btnWholesaleAdd")

        self.btn_edit_wholesale = QtWidgets.QPushButton("EDIT")
        self.btn_edit_wholesale.setObjectName("btnWholesaleEdit")

        self.btn_delete_wholesale = QtWidgets.QPushButton("DELETE")
        self.btn_delete_wholesale.setObjectName("btnWholesaleDelete")

        self.btn_clear_wholesale = QtWidgets.QPushButton("CLEAR")
        self.btn_clear_wholesale.setObjectName("btnWholesaleClear")

        for btn in [
            self.btn_add_wholesale,
            self.btn_edit_wholesale,
            self.btn_delete_wholesale,
            self.btn_clear_wholesale,
        ]:
            btn.setMinimumWidth(90)
            btn_h_w.addWidget(btn)

        form_layout_w.addWidget(btn_container_w, 2, 1, 1, 2)

        # ------------------- CONTENT CONTAINER -------------------
        content_container_w = QtWidgets.QWidget()
        content_v_w = QtWidgets.QVBoxLayout(content_container_w)
        content_v_w.setContentsMargins(0, 0, 0, 0)
        content_v_w.setSpacing(12)

        # --- Filter Row ---
        filter_h_w = QtWidgets.QHBoxLayout()
        filter_h_w.setContentsMargins(0, 0, 0, 0)
        filter_h_w.setSpacing(6)

        self.wholesale_filter_input = QtWidgets.QLineEdit()
        self.wholesale_filter_input.setPlaceholderText("Filter by item name or category...")
        self.wholesale_filter_input.setObjectName("inputWholesaleFilter")
        self.wholesale_filter_input.setFixedHeight(40)
        filter_h_w.addWidget(self.wholesale_filter_input, stretch=1)

        self.btn_filter_wholesale = QtWidgets.QPushButton("Search")
        self.btn_filter_wholesale.setObjectName("btnWholesaleFilter")
        self.btn_filter_wholesale.setFixedHeight(40)
        self.btn_filter_wholesale.setFixedWidth(120)
        filter_h_w.addWidget(self.btn_filter_wholesale)

        content_v_w.addLayout(filter_h_w)

        # --- Table + LCDs side by side ---
        table_lcd_h_w = QtWidgets.QHBoxLayout()
        table_lcd_h_w.setContentsMargins(0, 0, 0, 0)
        table_lcd_h_w.setSpacing(4)  # small gap between table and LCDs

        # Table
        self.table_wholesale = QtWidgets.QTableWidget()
        self.table_wholesale.setObjectName("WholesaleTable")
        self.table_wholesale.setColumnCount(7)
        self.table_wholesale.setHorizontalHeaderLabels(
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
        self.table_wholesale.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_wholesale.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.table_wholesale.setAlternatingRowColors(True)
        self.table_wholesale.horizontalHeader().setStretchLastSection(True)
        self.table_wholesale.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_wholesale.setMinimumHeight(300)
        self.table_wholesale.setMaximumWidth(920)

        # LCDs on right
        lcds_container_w = QtWidgets.QWidget()
        lcds_v_w = QtWidgets.QVBoxLayout(lcds_container_w)
        lcds_v_w.setContentsMargins(0, 0, 0, 0)
        lcds_v_w.setSpacing(12)

        def make_lcd_w(title, obj_name):
            lcd = QtWidgets.QLCDNumber()
            lcd.setObjectName(obj_name)
            lcd.setDigitCount(7)
            lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            lcd.setFixedWidth(180)
            lcd.setFixedHeight(60)

            lbl = QtWidgets.QLabel(title)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 13pt; font-weight: bold;")

            box = QtWidgets.QVBoxLayout()
            box.setSpacing(4)
            box.addWidget(lbl)
            box.addWidget(lcd)
            return box, lcd

        # --- Total Cost Price ---
        box_cost_w, self.lcd_wholesale_cost = make_lcd_w(
            "Total Cost Price", "lcdWholesaleTotalCost"
        )
        lcds_v_w.addLayout(box_cost_w)

        # --- Total Selling Price ---
        box_sell_w, self.lcd_wholesale_selling = make_lcd_w(
            "Total Selling Price", "lcdWholesaleTotalSelling"
        )
        lcds_v_w.addLayout(box_sell_w)

        # --- Total Profit ---
        box_profit_w, self.lcd_wholesale_profit = make_lcd_w(
            "Total Profit", "lcdWholesaleTotalProfit"
        )
        lcds_v_w.addLayout(box_profit_w)

        # Add table + LCDs
        table_lcd_h_w.addWidget(self.table_wholesale, stretch=2)
        table_lcd_h_w.addWidget(
            lcds_container_w, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
        )

        # Add to content
        content_v_w.addLayout(table_lcd_h_w)

        # ------------------- MAIN LAYOUT -------------------
        self.wholesale_layout.addWidget(
            form_container_w, stretch=0, alignment=QtCore.Qt.AlignTop
        )
        self.wholesale_layout.addWidget(content_container_w, stretch=1)

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
        self.emp_name.setObjectName("empNameInput")
        self.emp_name.setPlaceholderText("Enter employee name")
        self.emp_name.setFixedHeight(40)  # ⬆ increase input height
        form_layout.addWidget(
            create_field("Name:", self.emp_name, compulsory=True), 0, 0, 1, 2
        )

        # Phone (compulsory)
        self.emp_phone = QtWidgets.QLineEdit()
        self.emp_phone.setObjectName("empPhoneInput")
        self.emp_phone.setPlaceholderText("Enter phone number")
        self.emp_phone.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Phone:", self.emp_phone, compulsory=True), 0, 2, 1, 2
        )

        # Ghana Card ID (compulsory)
        self.emp_card = QtWidgets.QLineEdit()
        self.emp_card.setObjectName("empCardInput")
        self.emp_card.setPlaceholderText("Enter Ghana card ID")
        self.emp_card.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Ghana Card ID:", self.emp_card, compulsory=True), 1, 0, 1, 2
        )

        # Address
        self.emp_address = QtWidgets.QLineEdit()
        self.emp_address.setObjectName("empAddressInput")
        self.emp_address.setPlaceholderText("Enter address")
        self.emp_address.setFixedHeight(40)
        form_layout.addWidget(create_field("Address:", self.emp_address), 1, 2, 1, 2)

        # Designation (⬇ changed to ComboBox)
        self.emp_designation = QtWidgets.QComboBox()
        self.emp_designation.setObjectName("empDesignationInput")
        self.emp_designation.addItems(["Admin", "Manager", "Sales Rep"])
        self.emp_designation.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Designation:", self.emp_designation), 2, 0, 1, 2
        )

        # Salary
        self.emp_salary = QtWidgets.QLineEdit()
        self.emp_salary.setObjectName("empSalaryInput")
        self.emp_salary.setPlaceholderText("Enter salary")
        self.emp_salary.setFixedHeight(40)
        form_layout.addWidget(create_field("Salary:", self.emp_salary), 2, 2, 1, 2)

        # Buttons Row
        btn_width = int(form_container.width() * 0.35)

        self.btn_add_employee = QtWidgets.QPushButton("Add Employee")
        self.btn_add_employee.setObjectName("btnAddEmployee")
        self.btn_add_employee.setFixedWidth(btn_width)

        self.btn_clear_employee = QtWidgets.QPushButton("Clear")
        self.btn_clear_employee.setObjectName("btnClearEmployee")
        self.btn_clear_employee.setFixedWidth(btn_width)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.btn_add_employee)
        btn_row.addWidget(self.btn_clear_employee)
        btn_row.addStretch()
        form_layout.addLayout(btn_row, 3, 0, 1, 4)

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
        self.btn_filter.setObjectName("btnFilter")

        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setObjectName("filterInput")
        self.filter_input.setPlaceholderText("Filter by Phone or Ghana Card ID...")
        self.filter_input.setFixedHeight(40)
        self.filter_input.setFixedWidth(int(form_container.width() * 0.3))  # 30% width

        filter_container.addWidget(self.btn_filter)
        filter_container.addWidget(self.filter_input)
        filter_container.addStretch()

        employees_layout.addLayout(filter_container)

        # === Table Section ===
        self.table_employees = QtWidgets.QTableWidget()
        self.table_employees.setObjectName("tableEmployees")
        self.table_employees.setColumnCount(9)  # added Action column
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
                "Action",  # ✅ added column
            ]
        )
        self.table_employees.horizontalHeader().setStretchLastSection(True)
        self.table_employees.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
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

            # Action column with delete button
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setObjectName("EmpTableBtnDelete")
            delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            delete_btn.setToolTip("Delete")
            delete_btn.setFixedSize(30, 30)
            self.table_employees.setCellWidget(row, 8, delete_btn)

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
        account_layout.setSpacing(15)

        # === Form Section (Grid Layout, labels on top, tighter spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(850)
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(25)
        form_layout.setVerticalSpacing(6)  # tighter rows

        label_style = "color: black; font-weight: bold;"

        def create_field(label_text, widget):
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(2)
            lbl = QtWidgets.QLabel(label_text)
            lbl.setStyleSheet(label_style)
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # Inputs
        self.input_name = QtWidgets.QLineEdit()
        self.input_name.setObjectName("inputAccountName")
        self.input_name.setPlaceholderText("Enter name")
        self.input_name.setFixedHeight(40)
        form_layout.addWidget(create_field("Name:", self.input_name), 0, 0, 1, 2)

        self.input_phone = QtWidgets.QLineEdit()
        self.input_phone.setObjectName("inputAccountPhone")
        self.input_phone.setPlaceholderText("Enter phone number")
        self.input_phone.setFixedHeight(40)
        form_layout.addWidget(create_field("Phone:", self.input_phone), 0, 2, 1, 2)

        self.input_email = QtWidgets.QLineEdit()
        self.input_email.setObjectName("inputAccountEmail")
        self.input_email.setPlaceholderText("Enter email")
        self.input_email.setFixedHeight(40)
        form_layout.addWidget(create_field("Email:", self.input_email), 1, 0, 1, 2)

        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setObjectName("inputAccountPassword")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Password:", self.input_password), 1, 2, 1, 2
        )

        self.input_role = QtWidgets.QComboBox()
        self.input_role.setObjectName("inputAccountRole")
        self.input_role.addItems(["Admin", "Manager", "Cashier", "Sales Person"])
        self.input_role.setFixedHeight(40)
        form_layout.addWidget(create_field("Role:", self.input_role), 2, 0, 1, 2)

        # Buttons - reduced width
        self.btn_register = QtWidgets.QPushButton("ADD")
        self.btn_register.setObjectName("btnAccountRegister")
        self.btn_register.setFixedWidth(120)

        self.btn_edit = QtWidgets.QPushButton("EDIT")
        self.btn_edit.setObjectName("btnAccountEdit")
        self.btn_edit.setFixedWidth(120)

        self.btn_clear = QtWidgets.QPushButton("CLEAR")
        self.btn_clear.setObjectName("btnAccountClear")
        self.btn_clear.setFixedWidth(120)

        btn_widget = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)  # small space between buttons
        btn_layout.addWidget(self.btn_register)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_clear)

        # Place buttons beside Role field (same row, columns 2-3)
        form_layout.addWidget(btn_widget, 2, 2, 1, 2)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        account_layout.addLayout(form_wrapper)

        # === Table Section ===
        self.table_users = QtWidgets.QTableWidget()
        self.table_users.setObjectName("tableUsers")
        self.table_users.setColumnCount(6)  # Removed Status column
        self.table_users.setHorizontalHeaderLabels(
            ["ID", "Name", "Phone", "Email", "Role", "Actions"]
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

        # Sample data (6 cols now, no "Status")
        users_data = [
            (1, "Admin User", "0244000001", "admin@pos.com", "Admin"),
            (2, "Cashier One", "0244000002", "cashier@pos.com", "Cashier"),
            (3, "Manager One", "0244000003", "manager@pos.com", "Manager"),
        ]

        self.table_users.setRowCount(len(users_data))

        for row, (uid, name, phone, email, role) in enumerate(users_data):
            self.table_users.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_users.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_users.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
            self.table_users.setItem(row, 3, QtWidgets.QTableWidgetItem(email))
            self.table_users.setItem(row, 4, QtWidgets.QTableWidgetItem(role))

            # --- Action cell with icons ---
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(15)

            btn_edit = QtWidgets.QPushButton()
            btn_edit.setObjectName("tableBtnEdit")
            btn_edit.setIcon(QtGui.QIcon("assets/icons/edit.png"))
            btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn_edit.setToolTip("Edit User")
            btn_edit.setFixedSize(30, 30)

            btn_delete = QtWidgets.QPushButton()
            btn_delete.setObjectName("tableBtnDelete")
            btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn_delete.setToolTip("Delete User")
            btn_delete.setFixedSize(30, 30)

            action_layout.addStretch()
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.addStretch()

            self.table_users.setCellWidget(row, 5, action_widget)

        account_layout.addWidget(self.table_users, stretch=1)

        # self.page_settings = QtWidgets.QLabel("🔧 Settings Page", alignment=QtCore.Qt.AlignCentern)

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
        # self.stackedWidget.addWidget(self.page_settings)  # index 9

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
