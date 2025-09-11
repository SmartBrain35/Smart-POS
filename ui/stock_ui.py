from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Stock(object):
    def setupUi(self, Stock):
        stock_layout = QtWidgets.QVBoxLayout(Stock)
        stock_layout.setContentsMargins(10, 10, 10, 0)
        stock_layout.setSpacing(1)

        # --- Centered Tabs (now full width) ---
        self.stock_tabs = QtWidgets.QTabWidget()
        self.stock_tabs.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        stock_layout.addWidget(self.stock_tabs)

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
        self.stock_filter_input.setPlaceholderText("Filter by item name...")
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
        table_lcd_h.setSpacing(4)  # very small gap between table and LCDs

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
        self.table_stock.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_stock.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
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
            lcd = QtWidgets.QLCDNumber()
            lcd.setObjectName(obj_name)
            lcd.setDigitCount(7)
            lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            lcd.setFixedWidth(180)
            lcd.setFixedHeight(60)

            lbl = QtWidgets.QLabel(title)
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 12pt; font-weight: bold; color: black")

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

        table_lcd_h.addWidget(self.table_stock, stretch=2)
        table_lcd_h.addWidget(
            lcds_container, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
        )

        content_v.addLayout(table_lcd_h)

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
        form_layout_w.addWidget(
            vfield_w("Cost Price:", self.wholesale_cost_input), 1, 0
        )

        # Selling Price
        self.wholesale_selling_input = QtWidgets.QLineEdit()
        self.wholesale_selling_input.setPlaceholderText("Unit selling price")
        self.wholesale_selling_input.setObjectName("inputWholesaleSelling")
        self.wholesale_selling_input.setFixedHeight(40)
        form_layout_w.addWidget(
            vfield_w("Selling Price:", self.wholesale_selling_input), 1, 1
        )

        # Expiry date + checkbox
        self.wholesale_expiry_checkbox = QtWidgets.QCheckBox("")
        self.wholesale_expiry_checkbox.setFixedWidth(18)
        self.wholesale_expiry_date = QtWidgets.QDateEdit()
        self.wholesale_expiry_date.setCalendarPopup(True)
        self.wholesale_expiry_date.setDate(QtCore.QDate.currentDate())
        self.wholesale_expiry_date.setEnabled(False)
        self.wholesale_expiry_checkbox.toggled.connect(
            self.wholesale_expiry_date.setEnabled
        )
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
        self.wholesale_category_input.addItems(["Wholesale", "Retail"])
        form_layout_w.addWidget(
            vfield_w("Category:", self.wholesale_category_input), 2, 0
        )

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
        self.wholesale_filter_input.setPlaceholderText("Filter by item name...")
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
        self.table_wholesale.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_wholesale.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
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
            lbl.setStyleSheet("font-size: 12pt; font-weight: bold; color: black")

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

        table_lcd_h_w.addWidget(self.table_wholesale, stretch=2)
        table_lcd_h_w.addWidget(
            lcds_container_w, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight
        )

        content_v_w.addLayout(table_lcd_h_w)

        self.wholesale_layout.addWidget(
            form_container_w, stretch=0, alignment=QtCore.Qt.AlignTop
        )
        self.wholesale_layout.addWidget(content_container_w, stretch=1)
