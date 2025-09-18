from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Return(object):
    def setupUi(self, Return):
        return_layout = QtWidgets.QVBoxLayout(Return)
        return_layout.setContentsMargins(20, 20, 20, 20)
        return_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(35)
        form_layout.setVerticalSpacing(25)

        # Set stretches for responsiveness
        form_layout.setColumnStretch(0, 1)
        form_layout.setColumnStretch(1, 1)
        form_layout.setColumnStretch(2, 1)
        form_layout.setColumnStretch(3, 1)

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

        # Field configurations
        field_configs = [
            (
                "Item Name:",
                "returnItemNameInput",
                QtWidgets.QLineEdit,
                "Enter item name",
                True,
                0,
                0,
                1,
                2,
            ),
            (
                "Quantity:",
                "returnQuantityInput",
                QtWidgets.QLineEdit,
                "Enter quantity",
                True,
                0,
                2,
                1,
                2,
            ),
            (
                "Price:",
                "returnPriceInput",
                QtWidgets.QLineEdit,
                "Enter price",
                True,
                1,
                0,
                1,
                2,
            ),
            (
                "Return Reason:",
                "returnReasonInput",
                QtWidgets.QComboBox,
                None,
                True,
                1,
                2,
                1,
                2,
            ),
        ]

        self.fields = {}
        for (
            label_text,
            obj_name,
            widget_type,
            placeholder,
            compulsory,
            row,
            col,
            rowspan,
            colspan,
        ) in field_configs:
            if widget_type == QtWidgets.QComboBox:
                widget = QtWidgets.QComboBox()
                widget.addItems(["Defective", "Wrong Item", "Changed Mind", "Other"])
            else:
                widget = QtWidgets.QLineEdit()
                widget.setPlaceholderText(placeholder)
            widget.setObjectName(obj_name)
            widget.setMinimumHeight(40)
            widget.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            form_layout.addWidget(
                create_field(label_text, widget, compulsory), row, col, rowspan, colspan
            )
            self.fields[obj_name] = widget

        self.return_item_name = self.fields["returnItemNameInput"]
        self.return_quantity = self.fields["returnQuantityInput"]
        self.return_price = self.fields["returnPriceInput"]
        self.return_reason = self.fields["returnReasonInput"]

        # Buttons Row
        button_configs = [
            ("SAVE", "btn_save_return", "btnSaveReturn"),
            ("EDIT", "btn_edit_return", "btnEditReturn"),
            ("DELETE", "btn_delete_return", "btnDeleteReturn"),
            ("CLEAR", "btn_clear_return", "btnClearReturn"),
        ]

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()

        self.buttons = {}
        for text, attr_name, obj_name in button_configs:
            btn = QtWidgets.QPushButton(text)
            btn.setObjectName(obj_name)
            btn.setMinimumHeight(40)
            btn.setMinimumWidth(100)
            btn.setSizePolicy(
                QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
            )
            btn_row.addWidget(btn)
            self.buttons[attr_name] = btn

        self.btn_save_return = self.buttons["btn_save_return"]
        self.btn_edit_return = self.buttons["btn_edit_return"]
        self.btn_delete_return = self.buttons["btn_delete_return"]
        self.btn_clear_return = self.buttons["btn_clear_return"]

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
        self.filter_input_return.setMinimumHeight(40)
        self.filter_input_return.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        filter_container.addWidget(self.filter_input_return)
        filter_container.addStretch()

        return_layout.addLayout(filter_container)
        return_layout.addSpacing(2)

        # === Table and LCDs Section ===
        table_lcds_h = QtWidgets.QHBoxLayout()
        table_lcds_h.setSpacing(2)

        self.table_return = QtWidgets.QTableWidget()
        self.table_return.setObjectName("tableReturn")
        self.table_return.setColumnCount(7)
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
        self.table_return.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_return.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_return.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_return.setAlternatingRowColors(True)
        self.table_return.verticalHeader().setVisible(False)
        self.table_return.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
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
            lcd.setMinimumHeight(50)
            lcd.setMinimumWidth(180)
            w_layout.addWidget(lbl)
            w_layout.addWidget(lcd)
            return w, lcd

        lcd_configs = [
            ("Total Returned Items", "lcdTotalReturnedItems"),
            ("Total Refund Amount", "lcdTotalRefundAmount"),
            ("Total Loss", "lcdTotalLoss"),
        ]

        self.lcds = {}
        for title, obj_name in lcd_configs:
            box, lcd = _lcd_block(title, obj_name)
            lcds_v.addWidget(box)
            self.lcds[obj_name] = lcd

        self.lcdTotalReturnedItems = self.lcds["lcdTotalReturnedItems"]
        self.lcdTotalRefundAmount = self.lcds["lcdTotalRefundAmount"]
        self.lcdTotalLoss = self.lcds["lcdTotalLoss"]

        table_lcds_h.addLayout(lcds_v, stretch=1)
        return_layout.addLayout(table_lcds_h)
