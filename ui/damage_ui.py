from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Damage(object):
    def setupUi(self, Damage):
        damage_layout = QtWidgets.QVBoxLayout(Damage)
        damage_layout.setContentsMargins(20, 20, 20, 20)
        damage_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(35)
        form_layout.setVerticalSpacing(25)
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
            lbl.setStyleSheet(
                "color: red; font-weight: bold;" if compulsory else label_style
            )
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # Field configurations
        field_configs = [
            (
                "Item Name:",
                "damageItemNameInput",
                QtWidgets.QLineEdit,
                "Enter item name",
                True,
                0,
                0,
                1,
                2,
                {"readOnly": False},
            ),
            (
                "Quantity:",
                "damageQuantityInput",
                QtWidgets.QLineEdit,
                "Enter quantity",
                True,
                0,
                2,
                1,
                2,
                {"readOnly": False},
            ),
            (
                "Price:",
                "damagePriceInput",
                QtWidgets.QLineEdit,
                "Enter price",
                True,
                1,
                0,
                1,
                2,
                {"readOnly": True},
            ),
            (
                "Damage Status:",
                "damageStatusInput",
                QtWidgets.QComboBox,
                ["broken", "expired", "leakage", "other"],
                True,
                1,
                2,
                1,
                2,
                {},
            ),
        ]

        self.fields = {}
        for (
            label_text,
            obj_name,
            widget_type,
            default,
            compulsory,
            row,
            col,
            rowspan,
            colspan,
            props,
        ) in field_configs:
            if widget_type == QtWidgets.QComboBox:
                widget = QtWidgets.QComboBox()
                widget.addItems(default)
            else:
                widget = QtWidgets.QLineEdit()
                widget.setPlaceholderText(default)
            widget.setObjectName(obj_name)
            widget.setMinimumHeight(40)
            widget.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            for prop, value in props.items():
                getattr(widget, f"set{prop[0].upper() + prop[1:]}")(value)
            form_layout.addWidget(
                create_field(label_text, widget, compulsory), row, col, rowspan, colspan
            )
            self.fields[obj_name] = widget

        self.damage_item_name = self.fields["damageItemNameInput"]
        self.damage_quantity = self.fields["damageQuantityInput"]
        self.damage_price = self.fields["damagePriceInput"]
        self.damage_status = self.fields["damageStatusInput"]

        # Buttons Row
        button_configs = [
            ("SAVE", "btn_save_damage", "btnSaveDamage"),
            ("EDIT", "btn_edit_damage", "btnEditDamage"),
            ("DELETE", "btn_delete_damage", "btnDeleteDamage"),
            ("CLEAR", "btn_clear_damage", "btnClearDamage"),
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

        self.btn_save_damage = self.buttons["btn_save_damage"]
        self.btn_edit_damage = self.buttons["btn_edit_damage"]
        self.btn_delete_damage = self.buttons["btn_delete_damage"]
        self.btn_clear_damage = self.buttons["btn_clear_damage"]

        btn_row.addStretch()
        form_layout.addLayout(btn_row, 2, 0, 1, 4)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        damage_layout.addLayout(form_wrapper)

        # === Filter Input ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)
        filter_container.setAlignment(QtCore.Qt.AlignLeft)

        self.filter_input_damage = QtWidgets.QLineEdit()
        self.filter_input_damage.setObjectName("filterInputDamage")
        self.filter_input_damage.setPlaceholderText("Filter by Item Name...")
        self.filter_input_damage.setMinimumHeight(40)
        self.filter_input_damage.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        filter_container.addWidget(self.filter_input_damage)
        filter_container.addStretch()

        damage_layout.addLayout(filter_container)
        damage_layout.addSpacing(1)

        # === Table and LCDs Section ===
        table_lcds_h = QtWidgets.QHBoxLayout()
        table_lcds_h.setSpacing(2)

        self.table_damage = QtWidgets.QTableWidget()
        self.table_damage.setObjectName("tableDamage")
        self.table_damage.setColumnCount(7)
        self.table_damage.setHorizontalHeaderLabels(
            [
                "ID",
                "Item Name",
                "Quantity",
                "Price",
                "Damage Status",
                "Date Added",
                "Action",
            ]
        )
        header = self.table_damage.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_damage.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_damage.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_damage.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_damage.setAlternatingRowColors(True)
        self.table_damage.verticalHeader().setVisible(False)
        self.table_damage.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        table_lcds_h.addWidget(self.table_damage, stretch=9)

        # === LCDs Section ===
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
            ("Total Items", "lcdTotalItems"),
            ("Total Price", "lcdTotalPrice"),
            ("Total Profit", "lcdTotalProfit"),
        ]

        self.lcds = {}
        for title, obj_name in lcd_configs:
            box, lcd = _lcd_block(title, obj_name)
            lcds_v.addWidget(box)
            self.lcds[obj_name] = lcd

        self.lcdTotalItems = self.lcds["lcdTotalItems"]
        self.lcdTotalPrice = self.lcds["lcdTotalPrice"]
        self.lcdTotalProfit = self.lcds["lcdTotalProfit"]

        lcds_v.addStretch()
        table_lcds_h.addLayout(lcds_v, stretch=1)
        damage_layout.addLayout(table_lcds_h)
