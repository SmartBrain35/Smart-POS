from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Damage(object):
    def setupUi(self, Damage):
        damage_layout = QtWidgets.QVBoxLayout(Damage)
        damage_layout.setContentsMargins(20, 20, 20, 20)
        damage_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(950)  # wider form for damage
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
        self.damage_item_name = QtWidgets.QLineEdit()
        self.damage_item_name.setObjectName("damageItemNameInput")
        self.damage_item_name.setPlaceholderText("Enter item name")
        self.damage_item_name.setFixedHeight(40)  # increase input height
        form_layout.addWidget(
            create_field("Item Name:", self.damage_item_name, compulsory=True),
            0,
            0,
            1,
            2,
        )

        # Quantity (compulsory)
        self.damage_quantity = QtWidgets.QLineEdit()
        self.damage_quantity.setObjectName("damageQuantityInput")
        self.damage_quantity.setPlaceholderText("Enter quantity")
        self.damage_quantity.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Quantity:", self.damage_quantity, compulsory=True), 0, 2, 1, 2
        )

        # Price (compulsory, disabled)
        self.damage_price = QtWidgets.QLineEdit()
        self.damage_price.setObjectName("damagePriceInput")
        self.damage_price.setPlaceholderText("Enter price")
        self.damage_price.setFixedHeight(40)
        self.damage_price.setReadOnly(True)  # Disable price input
        form_layout.addWidget(
            create_field("Price:", self.damage_price, compulsory=True), 1, 0, 1, 2
        )

        # Damage Status (ComboBox, compulsory)
        self.damage_status = QtWidgets.QComboBox()
        self.damage_status.setObjectName("damageStatusInput")
        self.damage_status.addItems(["broken", "expired", "leakage", "other"])
        self.damage_status.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Damage Status:", self.damage_status, compulsory=True),
            1,
            2,
            1,
            2,
        )

        # Buttons Row
        btn_width = int(
            form_container.width() * 0.2
        )  # Reduced button width to create gaps

        self.btn_save_damage = QtWidgets.QPushButton("SAVE")
        self.btn_save_damage.setObjectName("btnSaveDamage")
        self.btn_save_damage.setFixedWidth(btn_width)
        self.btn_save_damage.setFixedHeight(40)  # Same height as inputs

        self.btn_edit_damage = QtWidgets.QPushButton("EDIT")
        self.btn_edit_damage.setObjectName("btnEditDamage")
        self.btn_edit_damage.setFixedWidth(btn_width)
        self.btn_edit_damage.setFixedHeight(40)  # Same height as inputs

        self.btn_delete_damage = QtWidgets.QPushButton("DELETE")
        self.btn_delete_damage.setObjectName("btnDeleteDamage")
        self.btn_delete_damage.setFixedWidth(btn_width)
        self.btn_delete_damage.setFixedHeight(40)  # Same height as inputs

        self.btn_clear_damage = QtWidgets.QPushButton("CLEAR")
        self.btn_clear_damage.setObjectName("btnClearDamage")
        self.btn_clear_damage.setFixedWidth(btn_width)
        self.btn_clear_damage.setFixedHeight(40)  # Same height as inputs

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(20)  # Horizontal spaces between buttons
        btn_row.addStretch()
        btn_row.addWidget(self.btn_save_damage)
        btn_row.addWidget(self.btn_edit_damage)
        btn_row.addWidget(self.btn_delete_damage)
        btn_row.addWidget(self.btn_clear_damage)
        btn_row.addStretch()
        form_layout.addLayout(btn_row, 2, 0, 1, 4)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        damage_layout.addLayout(form_wrapper)

        # === Filter Input (Top-left corner of table) ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)
        filter_container.setAlignment(QtCore.Qt.AlignLeft)

        self.filter_input_damage = QtWidgets.QLineEdit()
        self.filter_input_damage.setObjectName("filterInputDamage")
        self.filter_input_damage.setPlaceholderText("Filter by Item Name...")
        self.filter_input_damage.setFixedHeight(40)
        self.filter_input_damage.setFixedWidth(300)
        filter_container.addWidget(self.filter_input_damage)
        filter_container.addStretch()

        damage_layout.addLayout(filter_container)
        damage_layout.addSpacing(1)

        # === Table and LCDs Section ===
        table_lcds_h = QtWidgets.QHBoxLayout()
        table_lcds_h.setSpacing(2)

        # === Table Section ===
        self.table_damage = QtWidgets.QTableWidget()
        self.table_damage.setObjectName("tableDamage")
        self.table_damage.setColumnCount(
            7
        )  # ID, Item Name, Quantity, Price, Damage Status, Date Added, Action
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
        self.table_damage.horizontalHeader().setStretchLastSection(True)
        self.table_damage.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_damage.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_damage.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_damage.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_damage.setAlternatingRowColors(True)
        self.table_damage.verticalHeader().setVisible(False)
        self.table_damage.setFixedWidth(int(950 * 0.95))

        # Sample damage data
        damage_data = [
            (
                1,
                "Item A",
                "5",
                "10.00",
                "broken",
                "2023-09-01",
            ),
            (
                2,
                "Item B",
                "3",
                "15.00",
                "expired",
                "2023-09-10",
            ),
            (
                3,
                "Item C",
                "2",
                "20.00",
                "leakage",
                "2023-09-20",
            ),
        ]

        self.table_damage.setRowCount(len(damage_data))

        for row, (uid, name, qty, price, status, date) in enumerate(damage_data):
            self.table_damage.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_damage.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_damage.setItem(row, 2, QtWidgets.QTableWidgetItem(qty))
            self.table_damage.setItem(row, 3, QtWidgets.QTableWidgetItem(price))
            self.table_damage.setItem(row, 4, QtWidgets.QTableWidgetItem(status))
            self.table_damage.setItem(row, 5, QtWidgets.QTableWidgetItem(date))

            # Action column with delete button
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setObjectName("DamageTableBtnDelete")
            delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            delete_btn.setToolTip("Delete")
            delete_btn.setFixedSize(30, 30)
            self.table_damage.setCellWidget(row, 6, delete_btn)

        table_lcds_h.addWidget(self.table_damage, stretch=9)

        # === LCDs Section (Vertical on right of table, pinned to bottom) ===
        lcds_v = QtWidgets.QVBoxLayout()
        lcds_v.setSpacing(8)
        lcds_v.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight
        )

        def _lcd_block(title, obj_name):
            w = QtWidgets.QWidget()
            w_layout = QtWidgets.QVBoxLayout(w)
            w_layout.setContentsMargins(0, 0, 0, 0)
            w_layout.setSpacing(4)
            lbl = QtWidgets.QLabel(title)
            lbl.setObjectName(f"label_{obj_name}")
            lbl.setStyleSheet("color: black; font-weight: bold;")
            lbl.setAlignment(
                QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft
            )
            lcd = QtWidgets.QLCDNumber()
            lcd.setObjectName(obj_name)
            lcd.setDigitCount(9)
            lcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
            lcd.setFixedHeight(50)
            lcd.setFixedWidth(180)
            w_layout.addWidget(lbl)
            w_layout.addWidget(lcd)
            return w, lcd

        box_total_items, self.lcdTotalItems = _lcd_block("Total Items", "lcdTotalItems")
        box_total_price, self.lcdTotalPrice = _lcd_block("Total Price", "lcdTotalPrice")
        box_total_profit, self.lcdTotalProfit = _lcd_block(
            "Total Profit", "lcdTotalProfit"
        )

        lcds_v.addStretch()
        lcds_v.addWidget(box_total_items)
        lcds_v.addWidget(box_total_price)
        lcds_v.addWidget(box_total_profit)

        table_lcds_h.addLayout(lcds_v, stretch=1)
        damage_layout.addLayout(table_lcds_h)
