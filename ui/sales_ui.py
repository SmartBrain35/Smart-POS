from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Sales(object):
    def setupUi(self, Sales):
        self.sales_layout = QtWidgets.QHBoxLayout(Sales)
        self.sales_layout.setContentsMargins(8, 8, 8, 8)
        self.sales_layout.setSpacing(12)

        # ---------------- LEFT COLUMN (Search + Item List) ----------------
        left_col = QtWidgets.QVBoxLayout()
        left_col.setSpacing(
            1
        )  # Reduced spacing to 1 between search input and item list

        # Search label + input (top-left)
        lbl_search = QtWidgets.QLabel("Search Item:")
        lbl_search.setObjectName("labelSearchItem")
        lbl_search.setStyleSheet("color: black; font-weight: bold;")
        self.inputSearchItem = QtWidgets.QLineEdit()
        self.inputSearchItem.setObjectName("inputSearchItem")
        self.inputSearchItem.setPlaceholderText("Search item name...")
        self.inputSearchItem.setFixedHeight(40)
        self.inputSearchItem.setFixedWidth(350)  # Increased width for usability

        left_col.addWidget(lbl_search)
        left_col.addWidget(self.inputSearchItem)

        # Item list (e.g., search results) - QTableWidget for tabular list
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
        left_col.addWidget(self.tableItemList, stretch=1)

        self.sales_layout.addLayout(left_col, 2)
        # ---------------- CENTER COLUMN (Top controls, Cart Table, Below area) ----------------
        center_col = QtWidgets.QVBoxLayout()
        center_col.setSpacing(10)
        center_col.setContentsMargins(0, 0, 0, 0)

        # Top controls (vertical to have two rows for alignment)
        top_controls_v = QtWidgets.QVBoxLayout()
        top_controls_v.setSpacing(6)

        # Upper row: fields_h and group_right_top
        upper_h = QtWidgets.QHBoxLayout()
        upper_h.setSpacing(10)

        # Horizontal fields for qty stock, price, category
        fields_h = QtWidgets.QHBoxLayout()
        fields_h.setSpacing(6)

        lbl_qty_in_stock = QtWidgets.QLabel("Stock Qty:")
        lbl_qty_in_stock.setObjectName("labelQtyInStock")
        lbl_qty_in_stock.setStyleSheet("color: black; font-weight: bold;")
        self.inputQtyInStock = QtWidgets.QLineEdit()
        self.inputQtyInStock.setReadOnly(True)
        self.inputQtyInStock.setObjectName("inputQtyInStock")
        self.inputQtyInStock.setFixedHeight(40)
        self.inputQtyInStock.setFixedWidth(120)

        lbl_stock_price = QtWidgets.QLabel("Price:")
        lbl_stock_price.setObjectName("labelStockPrice")
        lbl_stock_price.setStyleSheet("color: black; font-weight: bold;")
        self.inputStockPrice = QtWidgets.QLineEdit()
        self.inputStockPrice.setReadOnly(True)
        self.inputStockPrice.setObjectName("inputStockPrice")
        self.inputStockPrice.setFixedHeight(40)
        self.inputStockPrice.setFixedWidth(120)

        lbl_category = QtWidgets.QLabel("Category:")
        lbl_category.setObjectName("labelCategory")
        lbl_category.setStyleSheet("color: black; font-weight: bold;")
        self.inputCategory = QtWidgets.QLineEdit()
        self.inputCategory.setReadOnly(True)
        self.inputCategory.setObjectName("inputCategory")
        self.inputCategory.setFixedHeight(40)
        self.inputCategory.setFixedWidth(120)

        fields_h.addWidget(lbl_qty_in_stock)
        fields_h.addWidget(self.inputQtyInStock)
        fields_h.addSpacing(4)
        fields_h.addWidget(lbl_stock_price)
        fields_h.addWidget(self.inputStockPrice)
        fields_h.addSpacing(4)
        fields_h.addWidget(lbl_category)
        fields_h.addWidget(self.inputCategory)

        upper_h.addLayout(fields_h)

        # Right side upper: Checkbox + Date
        group_right_top = QtWidgets.QHBoxLayout()
        group_right_top.setSpacing(8)
        group_right_top.setAlignment(QtCore.Qt.AlignRight)

        self.checkIncludeDate = QtWidgets.QCheckBox("Include Date")
        self.checkIncludeDate.setObjectName("checkIncludeDate")
        self.checkIncludeDate.setText("")

        self.dateInvoice = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.dateInvoice.setCalendarPopup(True)
        self.dateInvoice.setObjectName("dateInvoice")
        self.dateInvoice.setFixedHeight(40)
        self.dateInvoice.setFixedWidth(150)

        group_right_top.addWidget(self.checkIncludeDate)
        group_right_top.addWidget(self.dateInvoice)

        upper_h.addStretch(2)
        upper_h.addLayout(group_right_top)

        top_controls_v.addLayout(upper_h)

        # Lower row: QSpinBox with label, Add to Cart, huge gap, Invoice label and field side by side
        lower_h = QtWidgets.QHBoxLayout()
        lower_h.setSpacing(10)

        # Quantity sold with label (close gap)
        qty_sold_h = QtWidgets.QHBoxLayout()
        qty_sold_h.setSpacing(2)
        
        lbl_qty_sold = QtWidgets.QLabel("Quantity Sold:")
        lbl_qty_sold.setObjectName("labelQtySold")
        lbl_qty_sold.setStyleSheet("color: black; font-weight: bold;")
        self.inputQtySold = QtWidgets.QSpinBox()
        self.inputQtySold.setObjectName("inputQtySold")
        self.inputQtySold.setRange(1, 9999)
        self.inputQtySold.setFixedHeight(40)
        self.inputQtySold.setFixedWidth(60)

        qty_sold_h.addWidget(lbl_qty_sold)
        qty_sold_h.addWidget(self.inputQtySold)

        # Add to Cart button
        self.btnAddToCart = QtWidgets.QPushButton("ADD TO CART")
        self.btnAddToCart.setObjectName("btnAddToCart")
        self.btnAddToCart.setFixedHeight(40)
        self.btnAddToCart.setFixedWidth(130)

        # Bottom controls horizontal: qty_sold_h and btnAddToCart
        bottom_controls_h = QtWidgets.QHBoxLayout()
        bottom_controls_h.setSpacing(8)
        bottom_controls_h.addLayout(qty_sold_h)
        bottom_controls_h.addWidget(self.btnAddToCart)

        lower_h.addLayout(bottom_controls_h)

        # Huge gap
        lower_h.addStretch(10)

        # Invoice: label and field side by side
        invoice_h = QtWidgets.QHBoxLayout()
        invoice_h.setSpacing(8)

        lbl_invoice = QtWidgets.QLabel("Invoice ID:")
        lbl_invoice.setObjectName("labelInvoiceID")
        lbl_invoice.setStyleSheet("color: black; font-weight: bold;")
        self.inputInvoiceID = QtWidgets.QLineEdit()
        self.inputInvoiceID.setReadOnly(True)
        self.inputInvoiceID.setObjectName("inputInvoiceID")
        self.inputInvoiceID.setFixedHeight(40)
        self.inputInvoiceID.setFixedWidth(160)

        invoice_h.addWidget(lbl_invoice)
        invoice_h.addWidget(self.inputInvoiceID)

        lower_h.addLayout(invoice_h)

        top_controls_v.addLayout(lower_h)

        center_col.addLayout(top_controls_v)

        # Cart table (middle of page, fills space to bottom LCDs)
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
        self.tableCheckoutCart.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch
        )
        self.tableCheckoutCart.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableCheckoutCart.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableCheckoutCart.horizontalHeader().setSectionResizeMode(
            3, QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableCheckoutCart.horizontalHeader().setSectionResizeMode(
            4, QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableCheckoutCart.horizontalHeader().setSectionResizeMode(
            5, QtWidgets.QHeaderView.ResizeToContents
        )
        self.tableCheckoutCart.setMinimumHeight(250)
        center_col.addWidget(self.tableCheckoutCart, stretch=1)

        # Below cart table: LCDs, payment, buttons, daily sales/profit
        below_h = QtWidgets.QHBoxLayout()
        below_h.setSpacing(30)
        below_h.setAlignment(QtCore.Qt.AlignBottom)

        # LCDs (vertical stack, below cart) - Gross, Discount, Total
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
            lcd.setFixedHeight(50)
            lcd.setFixedWidth(180)
            w_layout.addWidget(lbl)
            w_layout.addWidget(lcd)
            w_layout.addStretch(0)
            return w, lcd

        box_gross, self.lcdGross = _lcd_block("Gross", "lcdGross")
        box_discount, self.lcdDiscount = _lcd_block("Discount", "lcdDiscount")
        box_total, self.lcdTotal = _lcd_block("Total", "lcdTotal")

        lcds_v.addWidget(box_gross)
        lcds_v.addWidget(box_discount)
        lcds_v.addWidget(box_total)

        below_h.addLayout(lcds_v, stretch=2)

        # Payment & action column (vertical)
        pay_v = QtWidgets.QVBoxLayout()
        pay_v.setSpacing(8)
        pay_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        # Action buttons (two rows: Save Print, Complete Clear)
        btns_v = QtWidgets.QVBoxLayout()
        btns_v.setSpacing(8)
        btns_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        # First row: Save and Print
        row1 = QtWidgets.QHBoxLayout()
        row1.setSpacing(20)
        row1.setAlignment(QtCore.Qt.AlignRight)

        self.btnSave = QtWidgets.QPushButton("SAVE")
        self.btnSave.setObjectName("btnSaveSale")
        self.btnSave.setFixedHeight(30)
        self.btnSave.setFixedWidth(150)

        self.btnPrint = QtWidgets.QPushButton("PRINT")
        self.btnPrint.setObjectName("btnPrintSale")
        self.btnPrint.setFixedHeight(30)
        self.btnPrint.setFixedWidth(150)

        row1.addWidget(self.btnSave)
        row1.addWidget(self.btnPrint)

        # Second row: Complete and Clear
        row2 = QtWidgets.QHBoxLayout()
        row2.setSpacing(20)
        row2.setAlignment(QtCore.Qt.AlignRight)

        self.btnComplete = QtWidgets.QPushButton("COMPLETE")
        self.btnComplete.setObjectName("btnCompleteSale")
        self.btnComplete.setFixedHeight(35)
        self.btnComplete.setFixedWidth(150)

        self.btnClear = QtWidgets.QPushButton("CLEAR")
        self.btnClear.setObjectName("btnClearSale")
        self.btnClear.setFixedHeight(35)
        self.btnClear.setFixedWidth(150)

        row2.addWidget(self.btnComplete)
        row2.addWidget(self.btnClear)

        btns_v.addLayout(row1)
        btns_v.addLayout(row2)

        pay_v.addLayout(btns_v)

        # Container for payment fields
        payment_fields_v = QtWidgets.QVBoxLayout()
        payment_fields_v.setSpacing(8)

        # Payment Method: label and combo side by side
        payment_method_h = QtWidgets.QHBoxLayout()
        payment_method_h.setSpacing(8)
        lbl_payment_method = QtWidgets.QLabel("Payment Method:")
        lbl_payment_method.setObjectName("labelPaymentMethod")
        lbl_payment_method.setStyleSheet("color: black; font-weight: bold;")
        self.comboPaymentMethod = QtWidgets.QComboBox()
        self.comboPaymentMethod.setObjectName("comboPaymentMethod")
        self.comboPaymentMethod.addItems(["Cash", "MoMo", "Card"])
        self.comboPaymentMethod.setFixedHeight(40)
        self.comboPaymentMethod.setFixedWidth(150)
        payment_method_h.addWidget(lbl_payment_method)
        payment_method_h.addWidget(self.comboPaymentMethod)
        payment_fields_v.addLayout(payment_method_h)

        # Discount: label and input side by side
        discount_h = QtWidgets.QHBoxLayout()
        discount_h.setSpacing(8)
        lbl_discount = QtWidgets.QLabel("Discount:")
        lbl_discount.setObjectName("labelDiscountInput")
        lbl_discount.setStyleSheet("color: black; font-weight: bold;")
        self.inputDiscount = QtWidgets.QLineEdit()
        self.inputDiscount.setObjectName("inputDiscount")
        self.inputDiscount.setFixedHeight(40)
        self.inputDiscount.setFixedWidth(150)
        discount_h.addWidget(lbl_discount)
        discount_h.addWidget(self.inputDiscount)
        payment_fields_v.addLayout(discount_h)

        # Amount Paid: label and input side by side
        amount_h = QtWidgets.QHBoxLayout()
        amount_h.setSpacing(8)
        lbl_amount = QtWidgets.QLabel("Amount Paid:")
        lbl_amount.setObjectName("labelAmountPaid")
        lbl_amount.setStyleSheet("color: black; font-weight: bold;")
        self.inputAmountPaid = QtWidgets.QLineEdit()
        self.inputAmountPaid.setObjectName("inputAmountPaid")
        self.inputAmountPaid.setFixedHeight(40)
        self.inputAmountPaid.setFixedWidth(150)
        amount_h.addWidget(lbl_amount)
        amount_h.addWidget(self.inputAmountPaid)
        payment_fields_v.addLayout(amount_h)

        # Change: label and input side by side
        change_h = QtWidgets.QHBoxLayout()
        change_h.setSpacing(8)
        lbl_change = QtWidgets.QLabel("Change:")
        lbl_change.setObjectName("labelChange")
        lbl_change.setStyleSheet("color: black; font-weight: bold;")
        self.inputChange = QtWidgets.QLineEdit()
        self.inputChange.setObjectName("inputChange")
        self.inputChange.setReadOnly(True)
        self.inputChange.setFixedHeight(40)
        self.inputChange.setFixedWidth(150)
        change_h.addWidget(lbl_change)
        change_h.addWidget(self.inputChange)
        payment_fields_v.addLayout(change_h)

        pay_v.addLayout(payment_fields_v)

        below_h.addLayout(pay_v, stretch=1)

        # Daily Sales and Daily Profit LCDs (far right)
        daily_v = QtWidgets.QVBoxLayout()
        daily_v.setSpacing(8)
        daily_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        box_items_sold, self.lcdItemsSold = _lcd_block("Items Sold", "lcdItemsSold")
        box_daily_sales, self.lcdDailySales = _lcd_block("Daily Sales", "lcdDailySales")
        box_daily_profit, self.lcdDailyProfit = _lcd_block(
            "Daily Profit", "lcdDailyProfit"
        )

        daily_v.addWidget(box_items_sold)
        daily_v.addWidget(box_daily_sales)
        daily_v.addWidget(box_daily_profit)

        below_h.addLayout(daily_v, stretch=1)

        below_h.addStretch(1)

        center_col.addLayout(below_h, stretch=0)

        self.sales_layout.addLayout(center_col, 6)
