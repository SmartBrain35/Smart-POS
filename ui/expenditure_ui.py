from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Expenditure(object):
    def setupUi(self, Expenditure):
        expenditure_layout = QtWidgets.QVBoxLayout(Expenditure)
        expenditure_layout.setContentsMargins(20, 20, 20, 20)
        expenditure_layout.setSpacing(20)

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
            lbl.setStyleSheet("color: red; font-weight: bold;" if compulsory else label_style)
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # Field configurations
        field_configs = [
            ("Date:", "expenditureDateInput", QtWidgets.QDateEdit, QtCore.QDate.currentDate(), True, 0, 0, 1, 2, {"calendarPopup": True}),
            ("Description:", "expenditureDescriptionInput", QtWidgets.QLineEdit, "Enter expenditure description", True, 0, 2, 1, 2, {}),
            ("Amount:", "expenditureAmountInput", QtWidgets.QLineEdit, "Enter amount", True, 1, 0, 1, 2, {}),
            ("Category:", "expenditureCategoryInput", QtWidgets.QComboBox, ["Utilities", "Supplies", "Salaries", "Other"], True, 1, 2, 1, 2, {}),
        ]

        self.fields = {}
        for label_text, obj_name, widget_type, default, compulsory, row, col, rowspan, colspan, props in field_configs:
            if widget_type == QtWidgets.QDateEdit:
                widget = QtWidgets.QDateEdit(default)
                for prop, value in props.items():
                    getattr(widget, f"set{prop[0].upper() + prop[1:]}")(value)
            elif widget_type == QtWidgets.QComboBox:
                widget = QtWidgets.QComboBox()
                widget.addItems(default)
            else:
                widget = QtWidgets.QLineEdit()
                widget.setPlaceholderText(default)
            widget.setObjectName(obj_name)
            widget.setMinimumHeight(40)
            widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            form_layout.addWidget(create_field(label_text, widget, compulsory), row, col, rowspan, colspan)
            self.fields[obj_name] = widget

        self.expenditure_date = self.fields["expenditureDateInput"]
        self.expenditure_description = self.fields["expenditureDescriptionInput"]
        self.expenditure_amount = self.fields["expenditureAmountInput"]
        self.expenditure_category = self.fields["expenditureCategoryInput"]

        # Buttons Row
        button_configs = [
            ("SAVE", "btn_save_expenditure", "btnSaveExpenditure"),
            ("EDIT", "btn_edit_expenditure", "btnEditExpenditure"),
            ("DELETE", "btn_delete_expenditure", "btnDeleteExpenditure"),
            ("CLEAR", "btn_clear_expenditure", "btnClearExpenditure"),
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
            btn.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
            btn_row.addWidget(btn)
            self.buttons[attr_name] = btn

        self.btn_save_expenditure = self.buttons["btn_save_expenditure"]
        self.btn_edit_expenditure = self.buttons["btn_edit_expenditure"]
        self.btn_delete_expenditure = self.buttons["btn_delete_expenditure"]
        self.btn_clear_expenditure = self.buttons["btn_clear_expenditure"]

        btn_row.addStretch()
        form_layout.addLayout(btn_row, 2, 0, 1, 4)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        expenditure_layout.addLayout(form_wrapper)

        # === Filter Input ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)
        filter_container.setAlignment(QtCore.Qt.AlignLeft)

        self.filter_input_expenditure = QtWidgets.QLineEdit()
        self.filter_input_expenditure.setObjectName("filterInputExpenditure")
        self.filter_input_expenditure.setPlaceholderText("Filter by Description or Category...")
        self.filter_input_expenditure.setMinimumHeight(40)
        self.filter_input_expenditure.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        filter_container.addWidget(self.filter_input_expenditure)
        filter_container.addStretch()

        expenditure_layout.addLayout(filter_container)
        expenditure_layout.addSpacing(2)

        # === Table and LCDs Section ===
        table_lcds_h = QtWidgets.QHBoxLayout()
        table_lcds_h.setSpacing(2)

        self.table_expenditure = QtWidgets.QTableWidget()
        self.table_expenditure.setObjectName("tableExpenditure")
        self.table_expenditure.setColumnCount(6)
        self.table_expenditure.setHorizontalHeaderLabels(["ID", "Date", "Description", "Amount", "Category", "Action"])
        header = self.table_expenditure.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_expenditure.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_expenditure.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_expenditure.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_expenditure.setAlternatingRowColors(True)
        self.table_expenditure.verticalHeader().setVisible(False)
        self.table_expenditure.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        table_lcds_h.addWidget(self.table_expenditure, stretch=9)

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
            ("Weekly Expenditures", "lcdWeeklyExpenditures"),
            ("Monthly Expenditures", "lcdMonthlyExpenditures"),
            ("Yearly Expenditures", "lcdYearlyExpenditures"),
        ]

        self.lcds = {}
        for title, obj_name in lcd_configs:
            box, lcd = _lcd_block(title, obj_name)
            lcds_v.addWidget(box)
            self.lcds[obj_name] = lcd

        self.lcdWeeklyExpenditures = self.lcds["lcdWeeklyExpenditures"]
        self.lcdMonthlyExpenditures = self.lcds["lcdMonthlyExpenditures"]
        self.lcdYearlyExpenditures = self.lcds["lcdYearlyExpenditures"]

        lcds_v.addStretch()
        table_lcds_h.addLayout(lcds_v, stretch=1)
        expenditure_layout.addLayout(table_lcds_h)
