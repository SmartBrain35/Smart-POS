from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtSql import QSqlTableModel


class Ui_Stock(object):
    def setupUi(self, Stock):
        stock_layout = QtWidgets.QVBoxLayout(Stock)
        stock_layout.setContentsMargins(10, 10, 10, 0)
        stock_layout.setSpacing(1)

        # ------------------- FORM CONTAINER -------------------
        form_container = QtWidgets.QWidget()
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(25)

        # Set column stretches for responsiveness
        form_layout.setColumnStretch(0, 1)
        form_layout.setColumnStretch(1, 2)
        form_layout.setColumnStretch(2, 1)

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
        content_v.setSpacing(6)

        # --- Left side: Filter on top, Table below ---
        left_container = QtWidgets.QWidget()
        left_v = QtWidgets.QVBoxLayout(left_container)
        left_v.setContentsMargins(0, 0, 0, 0)
        left_v.setSpacing(6)

        # Filter aligned top-right
        filter_h = QtWidgets.QHBoxLayout()
        filter_h.setContentsMargins(0, 0, 0, 0)
        filter_h.setSpacing(6)

        filter_h.addStretch()  # pushes filter to the right
        self.stock_filter_input = QtWidgets.QLineEdit()
        self.stock_filter_input.setPlaceholderText("Filter by item name...")
        self.stock_filter_input.setObjectName("inputRetailFilter")
        self.stock_filter_input.setFixedHeight(40)
        self.stock_filter_input.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        filter_h.addWidget(self.stock_filter_input)

        self.btn_filter_stock = QtWidgets.QPushButton("Search")
        self.btn_filter_stock.setObjectName("btnRetailFilter")
        self.btn_filter_stock.setFixedHeight(40)
        self.btn_filter_stock.setMinimumWidth(120)
        filter_h.addWidget(self.btn_filter_stock)

        left_v.addLayout(filter_h)

        # Table below filter
        self.table_stock = QtWidgets.QTableView()
        self.table_stock.setObjectName("RetailTable")
        self.table_stock.horizontalHeader().setStretchLastSection(True)
        self.table_stock.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_stock.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_stock.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_stock.setAlternatingRowColors(True)
        self.table_stock.setMinimumHeight(300)
        self.table_stock.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        left_v.addWidget(self.table_stock, stretch=1)

        # --- LCDs in 4x2 Grid ---
        lcds_container = QtWidgets.QWidget()
        lcds_grid = QtWidgets.QGridLayout(lcds_container)
        lcds_grid.setContentsMargins(0, 0, 0, 0)
        lcds_grid.setHorizontalSpacing(6)
        lcds_grid.setVerticalSpacing(12)

        # List of LCD configurations
        lcd_configs = [
            ("Wholesale Items", "lcdsWholesaleItems", 0, 0),
            ("Wholesale Costs", "lcdsWholesaleCosts", 1, 0),
            ("Wholesale Value", "lcdsWholesaleValues", 2, 0),
            ("Wholesale Profit", "lcdsWholesaleProfits", 3, 0),
            ("Retail Items", "lcdRetailItems", 0, 1),
            ("Retail Costs", "lcdRetailCosts", 1, 1),
            ("Retail Value", "lcdRetailValues", 2, 1),
            ("Retail Profit", "lcdRetailProfits", 3, 1),
        ]

        self.lcds = {}
        for title, obj_name, row, col in lcd_configs:
            box, lcd = self.make_lcd(title, obj_name)
            lcds_grid.addWidget(box, row, col)
            self.lcds[obj_name] = lcd

        # Assign to self.lcd1 etc. for backward compatibility if needed
        self.lcd1 = self.lcds["lcdsWholesaleItems"]
        self.lcd2 = self.lcds["lcdsWholesaleCosts"]
        self.lcd3 = self.lcds["lcdsWholesaleValues"]
        self.lcd4 = self.lcds["lcdsWholesaleProfits"]
        self.lcd5 = self.lcds["lcdRetailItems"]
        self.lcd6 = self.lcds["lcdRetailCosts"]
        self.lcd7 = self.lcds["lcdRetailValues"]
        self.lcd8 = self.lcds["lcdRetailProfits"]

        # --- Table + LCDs side by side ---
        table_lcd_h = QtWidgets.QHBoxLayout()
        table_lcd_h.setContentsMargins(0, 0, 0, 0)
        table_lcd_h.setSpacing(10)

        table_lcd_h.addWidget(left_container, stretch=4)
        table_lcd_h.addWidget(
            lcds_container,
            stretch=1,
            alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight,
        )

        content_v.addLayout(table_lcd_h)
        content_v.addSpacing(2)

        stock_layout.addWidget(form_container, stretch=0, alignment=QtCore.Qt.AlignTop)
        stock_layout.addWidget(content_container, stretch=1)

    def make_lcd(self, title, obj_name):
        wrapper = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(wrapper)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(3)

        lbl = QtWidgets.QLabel(title)
        lbl.setAlignment(QtCore.Qt.AlignLeft)
        lbl.setStyleSheet("font-size: 10pt; font-weight: bold; color: black")

        lcd = QtWidgets.QLCDNumber()
        lcd.setObjectName(obj_name)
        lcd.setDigitCount(7)
        lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        lcd.setMinimumWidth(150)
        lcd.setMinimumHeight(40)

        vbox.addWidget(lbl)
        vbox.addWidget(lcd)

        return wrapper, lcd
