from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Sales(object):
    def setupUi(self, Sales):
        self.sales_layout = QtWidgets.QHBoxLayout(Sales)
        self.sales_layout.setContentsMargins(8, 8, 8, 8)
        self.sales_layout.setSpacing(12)

        # ---------------- LEFT COLUMN (Search + Item List) ----------------
        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(1)

        lbl_search = QtWidgets.QLabel("Search Item:")
        lbl_search.setObjectName("labelSearchItem")
        lbl_search.setStyleSheet("color: black; font-weight: bold;")
        self.inputSearchItem = QtWidgets.QLineEdit()
        self.inputSearchItem.setObjectName("inputSearchItem")
        self.inputSearchItem.setPlaceholderText("Search item name...")
        self.inputSearchItem.setMinimumHeight(40)
        self.inputSearchItem.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

        left_col.addWidget(lbl_search)
        left_col.addWidget(self.inputSearchItem)

        self.tableItemList = QtWidgets.QTableWidget()
        self.tableItemList.setObjectName("tableItemList")
        self.tableItemList.setColumnCount(1)
        self.tableItemList.setHorizontalHeaderLabels(["Stock Items"])
        self.tableItemList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableItemList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableItemList.setAlternatingRowColors(True)
        self.tableItemList.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch
        )
        self.tableItemList.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        left_col.addWidget(self.tableItemList, stretch=1)

        self.sales_layout.addLayout(left_col, 2)

        # ---------------- CENTER COLUMN (Top controls, Cart Table, Below area) ----------------
        center_col = QtWidgets.QVBoxLayout()
        center_col.setSpacing(10)
        center_col.setContentsMargins(0, 0, 0, 0)

        top_controls_v = QtWidgets.QVBoxLayout()
        top_controls_v.setSpacing(6)

        upper_h = QtWidgets.QHBoxLayout()
        upper_h.setSpacing(10)

        fields_h = QtWidgets.QHBoxLayout()
        fields_h.setSpacing(6)

        # Define input fields configurations
        input_configs = [
            ("Stock Qty:", "inputQtyInStock"),
            ("Price:", "inputStockPrice"),
            ("Category:", "inputCategory"),
        ]

        self.inputs = {}
        for label_text, obj_name in input_configs:
            lbl = QtWidgets.QLabel(label_text)
            lbl.setObjectName(f"label{obj_name[5:]}")
            lbl.setStyleSheet("color: black; font-weight: bold;")
            input_field = QtWidgets.QLineEdit()
            input_field.setReadOnly(True)
            input_field.setObjectName(obj_name)
            input_field.setMinimumHeight(40)
            input_field.setMinimumWidth(120)
            input_field.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            fields_h.addWidget(lbl)
            fields_h.addWidget(input_field)
            self.inputs[obj_name] = input_field

        self.inputQtyInStock = self.inputs["inputQtyInStock"]
        self.inputStockPrice = self.inputs["inputStockPrice"]
        self.inputCategory = self.inputs["inputCategory"]

        upper_h.addLayout(fields_h)

        group_right_top = QtWidgets.QHBoxLayout()
        group_right_top.setSpacing(8)
        group_right_top.setAlignment(QtCore.Qt.AlignRight)

        self.checkIncludeDate = QtWidgets.QCheckBox("Include Date")
        self.checkIncludeDate.setObjectName("checkIncludeDate")
        self.checkIncludeDate.setText("")

        self.dateInvoice = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.dateInvoice.setCalendarPopup(True)
        self.dateInvoice.setObjectName("dateInvoice")
        self.dateInvoice.setMinimumHeight(40)
        self.dateInvoice.setMinimumWidth(150)
        self.dateInvoice.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

        group_right_top.addWidget(self.checkIncludeDate)
        group_right_top.addWidget(self.dateInvoice)

        upper_h.addStretch(2)
        upper_h.addLayout(group_right_top)

        top_controls_v.addLayout(upper_h)

        lower_h = QtWidgets.QHBoxLayout()
        lower_h.setSpacing(10)

        qty_sold_h = QtWidgets.QHBoxLayout()
        qty_sold_h.setSpacing(2)

        lbl_qty_sold = QtWidgets.QLabel("Quantity Sold:")
        lbl_qty_sold.setObjectName("labelQtySold")
        lbl_qty_sold.setStyleSheet("color: black; font-weight: bold;")
        self.inputQtySold = QtWidgets.QSpinBox()
        self.inputQtySold.setObjectName("inputQtySold")
        self.inputQtySold.setRange(1, 9999)
        self.inputQtySold.setMinimumHeight(40)
        self.inputQtySold.setMinimumWidth(60)
        self.inputQtySold.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )

        qty_sold_h.addWidget(lbl_qty_sold)
        qty_sold_h.addWidget(self.inputQtySold)

        self.btnAddToCart = QtWidgets.QPushButton("ADD TO CART")
        self.btnAddToCart.setObjectName("btnAddToCart")
        self.btnAddToCart.setMinimumHeight(40)
        self.btnAddToCart.setMinimumWidth(130)

        bottom_controls_h = QtWidgets.QHBoxLayout()
        bottom_controls_h.setSpacing(8)
        bottom_controls_h.addLayout(qty_sold_h)
        bottom_controls_h.addWidget(self.btnAddToCart)

        lower_h.addLayout(bottom_controls_h)
        lower_h.addStretch(10)

        invoice_h = QtWidgets.QHBoxLayout()
        invoice_h.setSpacing(8)

        lbl_invoice = QtWidgets.QLabel("Invoice ID:")
        lbl_invoice.setObjectName("labelInvoiceID")
        lbl_invoice.setStyleSheet("color: black; font-weight: bold;")
        self.inputInvoiceID = QtWidgets.QLineEdit()
        self.inputInvoiceID.setReadOnly(True)
        self.inputInvoiceID.setObjectName("inputInvoiceID")
        self.inputInvoiceID.setMinimumHeight(40)
        self.inputInvoiceID.setMinimumWidth(160)
        self.inputInvoiceID.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )

        invoice_h.addWidget(lbl_invoice)
        invoice_h.addWidget(self.inputInvoiceID)

        lower_h.addLayout(invoice_h)

        top_controls_v.addLayout(lower_h)

        center_col.addLayout(top_controls_v)

        self.tableCheckoutCart = QtWidgets.QTableWidget()
        self.tableCheckoutCart.setObjectName("tableCheckoutCart")
        self.tableCheckoutCart.setColumnCount(6)
        self.tableCheckoutCart.setHorizontalHeaderLabels(
            ["Item Name", "Category", "Quantity", "Price (GHS)", "Total", "Action"]
        )
        self.tableCheckoutCart.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tableCheckoutCart.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableCheckoutCart.setAlternatingRowColors(False)
        header = self.tableCheckoutCart.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tableCheckoutCart.setMinimumHeight(250)
        self.tableCheckoutCart.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        center_col.addWidget(self.tableCheckoutCart, stretch=1)

        below_h = QtWidgets.QHBoxLayout()
        below_h.setSpacing(30)
        below_h.setAlignment(QtCore.Qt.AlignBottom)

        lcds_v = QtWidgets.QVBoxLayout()
        lcds_v.setSpacing(2)
        lcds_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        def _lcd_block(title, obj_name):
            w = QtWidgets.QWidget()
            w_layout = QtWidgets.QVBoxLayout(w)
            w_layout.setContentsMargins(0, 0, 0, 0)
            w_layout.setSpacing(4)
            lbl = QtWidgets.QLabel(title)
            lbl.setObjectName(f"label_{obj_name}")
            lbl.setStyleSheet("color: black; font-weight: bold;")
            lbl.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
            lcd = QtWidgets.QLCDNumber()
            lcd.setObjectName(obj_name)
            lcd.setDigitCount(9)
            lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            lcd.setMinimumHeight(50)
            lcd.setMinimumWidth(180)
            w_layout.addWidget(lbl)
            w_layout.addWidget(lcd)
            return w, lcd

        # LCD configs for gross, discount, total
        lcd_main_configs = [
            ("Gross", "lcdGross"),
            ("Discount", "lcdDiscount"),
            ("Total", "lcdTotal"),
        ]

        self.lcd_main = {}
        for title, obj_name in lcd_main_configs:
            box, lcd = _lcd_block(title, obj_name)
            lcds_v.addWidget(box)
            self.lcd_main[obj_name] = lcd

        self.lcdGross = self.lcd_main["lcdGross"]
        self.lcdDiscount = self.lcd_main["lcdDiscount"]
        self.lcdTotal = self.lcd_main["lcdTotal"]

        below_h.addLayout(lcds_v, stretch=2)

        pay_v = QtWidgets.QVBoxLayout()
        pay_v.setSpacing(8)
        pay_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        btns_v = QtWidgets.QVBoxLayout()
        btns_v.setSpacing(8)
        btns_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(20)
        row1.setAlignment(QtCore.Qt.AlignRight)

        self.btnSave = QtWidgets.QPushButton("SAVE")
        self.btnSave.setObjectName("btnSaveSale")
        self.btnSave.setMinimumHeight(28)
        self.btnSave.setMinimumWidth(150)

        self.btnPrint = QtWidgets.QPushButton("PRINT")
        self.btnPrint.setObjectName("btnPrintSale")
        self.btnPrint.setMinimumHeight(28)
        self.btnPrint.setMinimumWidth(150)

        row1.addWidget(self.btnSave)
        row1.addWidget(self.btnPrint)

        row2 = QtWidgets.QHBoxLayout()
        row2.setSpacing(15)
        row2.setAlignment(QtCore.Qt.AlignRight)

        self.btnComplete = QtWidgets.QPushButton("COMPLETE")
        self.btnComplete.setObjectName("btnCompleteSale")
        self.btnComplete.setMinimumHeight(28)
        self.btnComplete.setMinimumWidth(150)

        self.btnClear = QtWidgets.QPushButton("CLEAR")
        self.btnClear.setObjectName("btnClearSale")
        self.btnClear.setMinimumHeight(28)
        self.btnClear.setMinimumWidth(150)

        row2.addWidget(self.btnComplete)
        row2.addWidget(self.btnClear)

        btns_v.addLayout(row1)
        btns_v.addLayout(row2)

        payment_fields_v = QtWidgets.QVBoxLayout()
        payment_fields_v.setSpacing(8)

        # Button configs
        button_configs = [
            ("SAVE", "btnSaveSale", 28, 150, self.btnSave),
            ("PRINT", "btnPrintSale", 28, 150, self.btnPrint),
            ("COMPLETE", "btnCompleteSale", 28, 150, self.btnComplete),
            ("CLEAR", "btnClearSale", 28, 150, self.btnClear),
        ]
        # Payment fields configs
        payment_configs = [
            (
                "Method: ",
                "comboPaymentMethod",
                QtWidgets.QComboBox,
                ["Cash", "MoMo", "Card"],
            ),
            ("Discount:", "inputDiscount", QtWidgets.QLineEdit, None),
            ("Amount: ", "inputAmountPaid", QtWidgets.QLineEdit, None),
            ("Change:  ", "inputChange", QtWidgets.QLineEdit, None),
        ]

        self.payment_widgets = {}
        for label_text, obj_name, widget_type, items in payment_configs:
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setSpacing(8)
            lbl = QtWidgets.QLabel(label_text)
            lbl.setObjectName(f"label{obj_name[5:]}")
            lbl.setStyleSheet("color: black; font-weight: bold;")
            if widget_type == QtWidgets.QComboBox:
                widget = QtWidgets.QComboBox()
                widget.addItems(items)
            else:
                widget = QtWidgets.QLineEdit()
                if obj_name == "inputChange":
                    widget.setReadOnly(True)
            widget.setObjectName(obj_name)
            widget.setMinimumHeight(38)
            widget.setMinimumWidth(150)
            widget.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            h_layout.addWidget(lbl)
            h_layout.addWidget(widget)
            payment_fields_v.addLayout(h_layout)
            self.payment_widgets[obj_name] = widget

        self.comboPaymentMethod = self.payment_widgets["comboPaymentMethod"]
        self.inputDiscount = self.payment_widgets["inputDiscount"]
        self.inputAmountPaid = self.payment_widgets["inputAmountPaid"]
        self.inputChange = self.payment_widgets["inputChange"]

        pay_v.addLayout(payment_fields_v)
        pay_v.addLayout(btns_v)

        below_h.addLayout(pay_v, stretch=1)

        daily_v = QtWidgets.QVBoxLayout()
        daily_v.setSpacing(8)
        daily_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        # Daily LCD configs
        daily_lcd_configs = [
            ("Items Sold", "lcdItemsSold"),
            ("Daily Sales", "lcdDailySales"),
            ("Daily Profit", "lcdDailyProfit"),
        ]

        self.daily_lcds = {}
        for title, obj_name in daily_lcd_configs:
            box, lcd = _lcd_block(title, obj_name)
            daily_v.addWidget(box)
            self.daily_lcds[obj_name] = lcd

        self.lcdItemsSold = self.daily_lcds["lcdItemsSold"]
        self.lcdDailySales = self.daily_lcds["lcdDailySales"]
        self.lcdDailyProfit = self.daily_lcds["lcdDailyProfit"]

        below_h.addLayout(daily_v, stretch=1)
        below_h.addStretch(1)

        center_col.addLayout(below_h, stretch=0)

        self.sales_layout.addLayout(center_col, 6)
