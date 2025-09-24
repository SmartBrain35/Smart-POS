from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Stock(object):
    def setupUi(self, Stock):
        stock_layout = QtWidgets.QVBoxLayout(Stock)
        stock_layout.setContentsMargins(10, 10, 0, 0)
        stock_layout.setSpacing(1)

        # ------------------- FORM CONTAINER -------------------
        form_container = QtWidgets.QWidget()
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(25)

        # Helpers
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
        self.inputRetailId = QtWidgets.QLineEdit()
        self.inputRetailId.setPlaceholderText("Auto / Enter ID")
        self.inputRetailId.setObjectName("inputRetailId")
        self.inputRetailId.setReadOnly(True)
        self.inputRetailId.setFixedHeight(40)
        form_layout.addWidget(vfield("ID:", self.inputRetailId), 0, 0)

        # Item Name
        self.inputRetailName = QtWidgets.QLineEdit()
        self.inputRetailName.setPlaceholderText("Enter item name")
        self.inputRetailName.setObjectName("inputRetailName")
        self.inputRetailName.setFixedHeight(40)
        form_layout.addWidget(vfield("Item Name:", self.inputRetailName), 0, 1)

        # Quantity
        self.inputRetailQty = QtWidgets.QLineEdit()
        self.inputRetailQty.setPlaceholderText("Enter quantity (integer)")
        self.inputRetailQty.setObjectName("inputRetailQty")
        self.inputRetailQty.setFixedHeight(40)
        form_layout.addWidget(vfield("Quantity:", self.inputRetailQty), 0, 2)

        # Cost Price
        self.inputRetailCost = QtWidgets.QLineEdit()
        self.inputRetailCost.setPlaceholderText("Unit cost price")
        self.inputRetailCost.setObjectName("inputRetailCost")
        self.inputRetailCost.setFixedHeight(40)
        form_layout.addWidget(vfield("Cost Price:", self.inputRetailCost), 1, 0)

        # Selling Price
        self.inputRetailSelling = QtWidgets.QLineEdit()
        self.inputRetailSelling.setPlaceholderText("Unit selling price")
        self.inputRetailSelling.setObjectName("inputRetailSelling")
        self.inputRetailSelling.setFixedHeight(40)
        form_layout.addWidget(vfield("Selling Price:", self.inputRetailSelling), 1, 1)

        # Expiry date + checkbox
        self.checkRetailExpiry = QtWidgets.QCheckBox("")
        self.checkRetailExpiry.setObjectName("checkRetailExpiry")
        self.checkRetailExpiry.setFixedWidth(18)

        self.dateRetailExpiry = QtWidgets.QDateEdit()
        self.dateRetailExpiry.setCalendarPopup(True)
        self.dateRetailExpiry.setDate(QtCore.QDate.currentDate())
        self.dateRetailExpiry.setEnabled(False)
        self.dateRetailExpiry.setObjectName("dateRetailExpiry")
        self.dateRetailExpiry.setFixedHeight(40)

        self.checkRetailExpiry.toggled.connect(self.dateRetailExpiry.setEnabled)

        expire_widget = QtWidgets.QWidget()
        expire_h = QtWidgets.QHBoxLayout(expire_widget)
        expire_h.setContentsMargins(0, 0, 0, 0)
        expire_h.setSpacing(4)
        expire_h.addWidget(self.checkRetailExpiry)
        expire_h.addWidget(self.dateRetailExpiry)

        form_layout.addWidget(vfield("Expire Date:", expire_widget), 1, 2)

        # Category
        self.inputRetailCategory = QtWidgets.QComboBox()
        self.inputRetailCategory.setObjectName("inputRetailCategory")
        self.inputRetailCategory.setFixedHeight(40)
        self.inputRetailCategory.addItems(["Retail", "Wholesale"])
        form_layout.addWidget(vfield("Category:", self.inputRetailCategory), 2, 0)

        # --- Action Buttons ---
        btn_container = QtWidgets.QWidget()
        btn_h = QtWidgets.QHBoxLayout(btn_container)
        btn_h.setContentsMargins(0, 0, 0, 0)
        btn_h.setSpacing(10)

        self.btnRetailAdd = QtWidgets.QPushButton("ADD")
        self.btnRetailAdd.setObjectName("btnRetailAdd")

        self.btnRetailEdit = QtWidgets.QPushButton("EDIT")
        self.btnRetailEdit.setObjectName("btnRetailEdit")

        self.btnRetailDelete = QtWidgets.QPushButton("DELETE")
        self.btnRetailDelete.setObjectName("btnRetailDelete")

        self.btnRetailClear = QtWidgets.QPushButton("CLEAR")
        self.btnRetailClear.setObjectName("btnRetailClear")

        for btn in [
            self.btnRetailAdd,
            self.btnRetailEdit,
            self.btnRetailDelete,
            self.btnRetailClear,
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
        filter_h.addStretch()
        self.inputRetailFilter = QtWidgets.QLineEdit()
        self.inputRetailFilter.setPlaceholderText("Filter by item name...")
        self.inputRetailFilter.setObjectName("inputRetailFilter")
        self.inputRetailFilter.setFixedHeight(40)
        filter_h.addWidget(self.inputRetailFilter)

        self.btnRetailFilter = QtWidgets.QPushButton("Search")
        self.btnRetailFilter.setObjectName("btnRetailFilter")
        self.btnRetailFilter.setFixedHeight(40)
        self.btnRetailFilter.setMinimumWidth(120)
        filter_h.addWidget(self.btnRetailFilter)

        content_v.addLayout(filter_h)

        # --- Table ---
        self.RetailTable = QtWidgets.QTableView()
        self.RetailTable.setObjectName("RetailTable")
        self.RetailTable.horizontalHeader().setStretchLastSection(True)
        self.RetailTable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.RetailTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.RetailTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.RetailTable.setAlternatingRowColors(True)
        self.RetailTable.verticalHeader().setVisible(False)
        self.RetailTable.setMinimumHeight(300)

        content_v.addWidget(self.RetailTable, stretch=1)

        # --- LCDs ---
        lcds_container = QtWidgets.QWidget()
        lcds_grid = QtWidgets.QGridLayout(lcds_container)

        self.lcdsWholesaleItemsWrapper, self.lcdsWholesaleItems = self._make_lcd(
            "Wholesale Items", "lcdsWholesaleItems"
        )
        lcds_grid.addWidget(self.lcdsWholesaleItemsWrapper, 0, 0)

        self.lcdsWholesaleCostsWrapper, self.lcdsWholesaleCosts = self._make_lcd(
            "Wholesale Costs", "lcdsWholesaleCosts"
        )
        lcds_grid.addWidget(self.lcdsWholesaleCostsWrapper, 1, 0)

        self.lcdsWholesaleValuesWrapper, self.lcdsWholesaleValues = self._make_lcd(
            "Wholesale Value", "lcdsWholesaleValues"
        )
        lcds_grid.addWidget(self.lcdsWholesaleValuesWrapper, 2, 0)

        self.lcdsWholesaleProfitsWrapper, self.lcdsWholesaleProfits = self._make_lcd(
            "Wholesale Profit", "lcdsWholesaleProfits"
        )
        lcds_grid.addWidget(self.lcdsWholesaleProfitsWrapper, 3, 0)

        self.lcdRetailItemsWrapper, self.lcdRetailItems = self._make_lcd(
            "Retail Items", "lcdRetailItems"
        )
        lcds_grid.addWidget(self.lcdRetailItemsWrapper, 0, 1)

        self.lcdRetailCostsWrapper, self.lcdRetailCosts = self._make_lcd(
            "Retail Costs", "lcdRetailCosts"
        )
        lcds_grid.addWidget(self.lcdRetailCostsWrapper, 1, 1)

        self.lcdRetailValuesWrapper, self.lcdRetailValues = self._make_lcd(
            "Retail Value", "lcdRetailValues"
        )
        lcds_grid.addWidget(self.lcdRetailValuesWrapper, 2, 1)

        self.lcdRetailProfitsWrapper, self.lcdRetailProfits = self._make_lcd(
            "Retail Profit", "lcdRetailProfits"
        )
        lcds_grid.addWidget(self.lcdRetailProfitsWrapper, 3, 1)

        # Combine
        table_lcd_h = QtWidgets.QHBoxLayout()
        table_lcd_h.addWidget(content_container, stretch=4)
        table_lcd_h.addWidget(
            lcds_container, stretch=1, alignment=QtCore.Qt.AlignBottom
        )

        stock_layout.addWidget(form_container, stretch=0, alignment=QtCore.Qt.AlignTop)
        stock_layout.addLayout(table_lcd_h)

    def _make_lcd(self, title, obj_name):
        wrapper = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout(wrapper)
        lbl = QtWidgets.QLabel(title)
        lbl.setStyleSheet("font-size: 10pt; font-weight: bold; color: black")
        lcd = QtWidgets.QLCDNumber()
        lcd.setObjectName(obj_name)
        lcd.setDigitCount(10)
        lcd.setSmallDecimalPoint(True)
        lcd.setMode(QtWidgets.QLCDNumber.Dec)  # <-- add this line
        lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        lcd.setMinimumWidth(150)
        lcd.setMinimumHeight(40)
        vbox.addWidget(lbl)
        vbox.addWidget(lcd)
        return wrapper, lcd
