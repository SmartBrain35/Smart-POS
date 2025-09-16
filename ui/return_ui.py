from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Return(object):
    def setupUi(self, Return):
        return_layout = QtWidgets.QVBoxLayout(Return)
        return_layout.setContentsMargins(20, 20, 20, 20)
        return_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(950)  # Consistent with other pages
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(35)
        form_layout.setVerticalSpacing(25)

        label_style = "color: black; font-weight: bold;"

        def create_field(label_text, widget, compulsory=False):
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

        # Item Name (compulsory)
        self.return_item_name = QtWidgets.QLineEdit()
        self.return_item_name.setObjectName("returnItemNameInput")
        self.return_item_name.setPlaceholderText("Enter item name")
        self.return_item_name.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Item Name:", self.return_item_name, compulsory=True),
            0,
            0,
            1,
            2,
        )

        # Quantity (compulsory)
        self.return_quantity = QtWidgets.QLineEdit()
        self.return_quantity.setObjectName("returnQuantityInput")
        self.return_quantity.setPlaceholderText("Enter quantity")
        self.return_quantity.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Quantity:", self.return_quantity, compulsory=True), 0, 2, 1, 2
        )

        # Price (compulsory, enabled for input)
        self.return_price = QtWidgets.QLineEdit()
        self.return_price.setObjectName("returnPriceInput")
        self.return_price.setPlaceholderText("Enter price")
        self.return_price.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Price:", self.return_price, compulsory=True), 1, 0, 1, 2
        )

        # Return Reason (ComboBox, compulsory)
        self.return_reason = QtWidgets.QComboBox()
        self.return_reason.setObjectName("returnReasonInput")
        self.return_reason.addItems(
            ["Defective", "Wrong Item", "Changed Mind", "Other"]
        )
        self.return_reason.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Return Reason:", self.return_reason, compulsory=True),
            1,
            2,
            1,
            2,
        )

        # Buttons Row
        btn_width = int(form_container.width() * 0.2)  # Reduced width for gaps

        self.btn_save_return = QtWidgets.QPushButton("SAVE")
        self.btn_save_return.setObjectName("btnSaveReturn")
        self.btn_save_return.setFixedWidth(btn_width)
        self.btn_save_return.setFixedHeight(40)

        self.btn_edit_return = QtWidgets.QPushButton("EDIT")
        self.btn_edit_return.setObjectName("btnEditReturn")
        self.btn_edit_return.setFixedWidth(btn_width)
        self.btn_edit_return.setFixedHeight(40)

        self.btn_delete_return = QtWidgets.QPushButton("DELETE")
        self.btn_delete_return.setObjectName("btnDeleteReturn")
        self.btn_delete_return.setFixedWidth(btn_width)
        self.btn_delete_return.setFixedHeight(40)

        self.btn_clear_return = QtWidgets.QPushButton("CLEAR")
        self.btn_clear_return.setObjectName("btnClearReturn")
        self.btn_clear_return.setFixedWidth(btn_width)
        self.btn_clear_return.setFixedHeight(40)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(20)  # Horizontal spaces between buttons
        btn_row.addStretch()
        btn_row.addWidget(self.btn_save_return)
        btn_row.addWidget(self.btn_edit_return)
        btn_row.addWidget(self.btn_delete_return)
        btn_row.addWidget(self.btn_clear_return)
        btn_row.addStretch()
        form_layout.addLayout(btn_row, 2, 0, 1, 4)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        return_layout.addLayout(form_wrapper)

        # === Filter Input (Top-left corner of table) ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)
        filter_container.setAlignment(QtCore.Qt.AlignLeft)

        self.filter_input_return = QtWidgets.QLineEdit()
        self.filter_input_return.setObjectName("filterInputReturn")
        self.filter_input_return.setPlaceholderText(
            "Filter by Item Name or Return Reason..."
        )
        self.filter_input_return.setFixedHeight(40)
        self.filter_input_return.setFixedWidth(300)
        filter_container.addWidget(self.filter_input_return)
        filter_container.addStretch()

        return_layout.addLayout(filter_container)
        return_layout.addSpacing(2)  # Reduced space between filter and table

        # === Table and LCDs Section ===
        table_lcds_h = QtWidgets.QHBoxLayout()
        table_lcds_h.setSpacing(2)  # Reduced space between table and LCDs

        # === Table Section ===
        self.table_return = QtWidgets.QTableWidget()
        self.table_return.setObjectName("tableReturn")
        self.table_return.setColumnCount(
            7
        )  # ID, Item Name, Quantity, Price, Return Reason, Date Returned, Action
        self.table_return.setHorizontalHeaderLabels(
            [
                "ID",
                "Item Name",
                "Quantity",
                "Price",
                "Return Reason",
                "Date Returned",
                "Action",
            ]
        )
        self.table_return.horizontalHeader().setStretchLastSection(True)
        self.table_return.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_return.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )  # Disable double-click editing
        self.table_return.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_return.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_return.setAlternatingRowColors(True)
        self.table_return.verticalHeader().setVisible(False)
        self.table_return.setFixedWidth(int(950 * 0.95))  # Extended table width

        table_lcds_h.addWidget(self.table_return, stretch=9)

        # === LCDs Section (Vertical on right of table, pinned to bottom) ===
        lcds_v = QtWidgets.QVBoxLayout()
        lcds_v.setSpacing(8)
        lcds_v.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

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
            return w, lcd

        box_total_returned_items, self.lcdTotalReturnedItems = _lcd_block(
            "Total Returned Items", "lcdTotalReturnedItems"
        )
        box_total_refund_amount, self.lcdTotalRefundAmount = _lcd_block(
            "Total Refund Amount", "lcdTotalRefundAmount"
        )
        box_total_loss, self.lcdTotalLoss = _lcd_block("Total Loss", "lcdTotalLoss")

        lcds_v.addStretch()
        lcds_v.addWidget(box_total_returned_items)
        lcds_v.addWidget(box_total_refund_amount)
        lcds_v.addWidget(box_total_loss)

        table_lcds_h.addLayout(lcds_v, stretch=1)
        return_layout.addLayout(table_lcds_h)
