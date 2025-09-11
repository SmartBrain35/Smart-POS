from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Expenditure(object):
    def setupUi(self, Expenditure):
        expenditure_layout = QtWidgets.QVBoxLayout(Expenditure)
        expenditure_layout.setContentsMargins(20, 20, 20, 20)
        expenditure_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(950)  # Consistent with Damage Page
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

        # Date (compulsory)
        self.expenditure_date = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.expenditure_date.setObjectName("expenditureDateInput")
        self.expenditure_date.setCalendarPopup(True)
        self.expenditure_date.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Date:", self.expenditure_date, compulsory=True), 0, 0, 1, 2
        )

        # Description (compulsory)
        self.expenditure_description = QtWidgets.QLineEdit()
        self.expenditure_description.setObjectName("expenditureDescriptionInput")
        self.expenditure_description.setPlaceholderText("Enter expenditure description")
        self.expenditure_description.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Description:", self.expenditure_description, compulsory=True),
            0,
            2,
            1,
            2,
        )

        # Amount (compulsory)
        self.expenditure_amount = QtWidgets.QLineEdit()
        self.expenditure_amount.setObjectName("expenditureAmountInput")
        self.expenditure_amount.setPlaceholderText("Enter amount")
        self.expenditure_amount.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Amount:", self.expenditure_amount, compulsory=True),
            1,
            0,
            1,
            2,
        )

        # Category (ComboBox, compulsory)
        self.expenditure_category = QtWidgets.QComboBox()
        self.expenditure_category.setObjectName("expenditureCategoryInput")
        self.expenditure_category.addItems(
            ["Utilities", "Supplies", "Salaries", "Other"]
        )
        self.expenditure_category.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Category:", self.expenditure_category, compulsory=True),
            1,
            2,
            1,
            2,
        )

        # Buttons Row
        btn_width = int(form_container.width() * 0.2)  # Reduced width for gaps

        self.btn_save_expenditure = QtWidgets.QPushButton("SAVE")
        self.btn_save_expenditure.setObjectName("btnSaveExpenditure")
        self.btn_save_expenditure.setFixedWidth(btn_width)
        self.btn_save_expenditure.setFixedHeight(40)

        self.btn_edit_expenditure = QtWidgets.QPushButton("EDIT")
        self.btn_edit_expenditure.setObjectName("btnEditExpenditure")
        self.btn_edit_expenditure.setFixedWidth(btn_width)
        self.btn_edit_expenditure.setFixedHeight(40)

        self.btn_delete_expenditure = QtWidgets.QPushButton("DELETE")
        self.btn_delete_expenditure.setObjectName("btnDeleteExpenditure")
        self.btn_delete_expenditure.setFixedWidth(btn_width)
        self.btn_delete_expenditure.setFixedHeight(40)

        self.btn_clear_expenditure = QtWidgets.QPushButton("CLEAR")
        self.btn_clear_expenditure.setObjectName("btnClearExpenditure")
        self.btn_clear_expenditure.setFixedWidth(btn_width)
        self.btn_clear_expenditure.setFixedHeight(40)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(20)  # Horizontal spaces between buttons
        btn_row.addStretch()
        btn_row.addWidget(self.btn_save_expenditure)
        btn_row.addWidget(self.btn_edit_expenditure)
        btn_row.addWidget(self.btn_delete_expenditure)
        btn_row.addWidget(self.btn_clear_expenditure)
        btn_row.addStretch()
        form_layout.addLayout(btn_row, 2, 0, 1, 4)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        expenditure_layout.addLayout(form_wrapper)

        # === Filter Input (Top-left corner of table) ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)
        filter_container.setAlignment(QtCore.Qt.AlignLeft)

        self.filter_input_expenditure = QtWidgets.QLineEdit()
        self.filter_input_expenditure.setObjectName("filterInputExpenditure")
        self.filter_input_expenditure.setPlaceholderText(
            "Filter by Description or Category..."
        )
        self.filter_input_expenditure.setFixedHeight(40)
        self.filter_input_expenditure.setFixedWidth(300)
        filter_container.addWidget(self.filter_input_expenditure)
        filter_container.addStretch()

        expenditure_layout.addLayout(filter_container)
        expenditure_layout.addSpacing(2)

        # === Table and LCDs Section ===
        table_lcds_h = QtWidgets.QHBoxLayout()
        table_lcds_h.setSpacing(2)

        # === Table Section ===
        self.table_expenditure = QtWidgets.QTableWidget()
        self.table_expenditure.setObjectName("tableExpenditure")
        self.table_expenditure.setColumnCount(
            6
        )  # ID, Date, Description, Amount, Category, Action
        self.table_expenditure.setHorizontalHeaderLabels(
            [
                "ID",
                "Date",
                "Description",
                "Amount",
                "Category",
                "Action",
            ]
        )
        self.table_expenditure.horizontalHeader().setStretchLastSection(True)
        self.table_expenditure.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_expenditure.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.table_expenditure.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table_expenditure.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.table_expenditure.setAlternatingRowColors(True)
        self.table_expenditure.verticalHeader().setVisible(False)
        self.table_expenditure.setFixedWidth(int(950 * 0.95))

        # Sample expenditure data
        expenditure_data = [
            (
                1,
                "2023-09-01",
                "Office Rent",
                "5000.00",
                "Utilities",
            ),
            (
                2,
                "2023-09-10",
                "Stationery Supplies",
                "200.00",
                "Supplies",
            ),
            (
                3,
                "2023-09-20",
                "Staff Salaries",
                "10000.00",
                "Salaries",
            ),
        ]

        self.table_expenditure.setRowCount(len(expenditure_data))

        for row, (uid, date, desc, amount, category) in enumerate(expenditure_data):
            self.table_expenditure.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_expenditure.setItem(row, 1, QtWidgets.QTableWidgetItem(date))
            self.table_expenditure.setItem(row, 2, QtWidgets.QTableWidgetItem(desc))
            self.table_expenditure.setItem(row, 3, QtWidgets.QTableWidgetItem(amount))
            self.table_expenditure.setItem(row, 4, QtWidgets.QTableWidgetItem(category))

            # Action column with delete button
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setObjectName("ExpenditureTableBtnDelete")
            delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            delete_btn.setToolTip("Delete")
            delete_btn.setFixedSize(30, 30)
            self.table_expenditure.setCellWidget(row, 5, delete_btn)

        table_lcds_h.addWidget(self.table_expenditure, stretch=9)

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

        box_total_expenditures, self.lcdTotalExpenditures = _lcd_block(
            "Weekly Expenditures", "lcdWeeklyExpenditures"
        )
        box_monthly_expenditures, self.lcdMonthlyExpenditures = _lcd_block(
            "Monthly Expenditures", "lcdMonthlyExpenditures"
        )
        box_yearly_expenditures, self.lcdYearlyExpenditures = _lcd_block(
            "Yearly Expenditures", "lcdYearlyExpenditures"
        )

        lcds_v.addStretch()
        lcds_v.addWidget(box_total_expenditures)
        lcds_v.addWidget(box_monthly_expenditures)
        lcds_v.addWidget(box_yearly_expenditures)

        table_lcds_h.addLayout(lcds_v, stretch=1)
        expenditure_layout.addLayout(table_lcds_h)
