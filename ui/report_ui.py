from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Report(object):
    def setupUi(self, Report):
        report_layout = QtWidgets.QVBoxLayout(Report)
        report_layout.setContentsMargins(20, 20, 20, 20)
        report_layout.setSpacing(20)

        # === Filter Section (Date range, category, generate button) ===
        filter_container = QtWidgets.QWidget()
        filter_layout = QtWidgets.QGridLayout(filter_container)
        filter_layout.setContentsMargins(20, 20, 20, 20)
        filter_layout.setHorizontalSpacing(35)
        filter_layout.setVerticalSpacing(25)

        # Common label styling
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

        # Date From (compulsory)
        self.report_date_from = QtWidgets.QDateEdit(
            QtCore.QDate.currentDate().addMonths(-1)
        )
        self.report_date_from.setObjectName("reportDateFromInput")
        self.report_date_from.setCalendarPopup(True)
        self.report_date_from.setFixedHeight(40)
        filter_layout.addWidget(
            create_field("From Date:", self.report_date_from, compulsory=True),
            0,
            0,
            1,
            2,
        )

        # Date To (compulsory)
        self.report_date_to = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.report_date_to.setObjectName("reportDateToInput")
        self.report_date_to.setCalendarPopup(True)
        self.report_date_to.setFixedHeight(40)
        filter_layout.addWidget(
            create_field("To Date:", self.report_date_to, compulsory=True), 0, 2, 1, 2
        )

        # Category (ComboBox, optional)
        self.report_category = QtWidgets.QComboBox()
        self.report_category.setObjectName("reportCategoryInput")
        self.report_category.addItems(
            ["All", "Sales", "Expenditures", "Damages", "Returns"]
        )
        self.report_category.setFixedHeight(40)
        filter_layout.addWidget(
            create_field("Category:", self.report_category), 1, 0, 1, 2
        )

        # Buttons: Generate Report, Export, Clear
        btn_width = int(filter_container.width() * 0.2)

        self.btn_generate_report = QtWidgets.QPushButton("Generate Report")
        self.btn_generate_report.setObjectName("btnGenerateReport")
        self.btn_generate_report.setFixedWidth(btn_width)
        self.btn_generate_report.setFixedHeight(40)

        self.btn_export_report = QtWidgets.QPushButton("Export")
        self.btn_export_report.setObjectName("btnExportReport")
        self.btn_export_report.setFixedWidth(btn_width)
        self.btn_export_report.setFixedHeight(40)

        self.btn_clear_report = QtWidgets.QPushButton("Clear")
        self.btn_clear_report.setObjectName("btnClearReport")
        self.btn_clear_report.setFixedWidth(btn_width)
        self.btn_clear_report.setFixedHeight(40)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(20)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_generate_report)
        btn_row.addWidget(self.btn_export_report)
        btn_row.addWidget(self.btn_clear_report)
        btn_row.addStretch()
        filter_layout.addLayout(btn_row, 1, 2, 1, 2)

        # Center the filter form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(filter_container)
        form_wrapper.addStretch()
        report_layout.addLayout(form_wrapper)

        # === Table and LCDs Section ===
        table_lcds_h = QtWidgets.QHBoxLayout()
        table_lcds_h.setSpacing(2)  # Reduced space between table and LCDs

        # === Table Section ===
        self.table_report = QtWidgets.QTableWidget()
        self.table_report.setObjectName("tableReport")
        self.table_report.setColumnCount(
            6
        )  # ID, Date, Category, Description, Amount, Action (optional)
        self.table_report.setHorizontalHeaderLabels(
            [
                "ID",
                "Date",
                "Category",
                "Description",
                "Amount",
                "Action",
            ]
        )
        self.table_report.horizontalHeader().setStretchLastSection(True)
        self.table_report.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_report.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )  # Read-only
        self.table_report.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_report.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_report.setAlternatingRowColors(True)
        self.table_report.verticalHeader().setVisible(False)
        self.table_report.setFixedWidth(int(950 * 0.95))  # Extended table width

        # Sample report data (placeholder)
        report_data = [
            (
                1,
                "2025-09-01",
                "Sales",
                "Product Sale",
                "1000.00",
            ),
            (
                2,
                "2025-09-05",
                "Expenditures",
                "Office Rent",
                "5000.00",
            ),
            (
                3,
                "2025-09-10",
                "Damages",
                "Broken Item",
                "200.00",
            ),
        ]

        self.table_report.setRowCount(len(report_data))

        for row, (uid, date, category, desc, amount) in enumerate(report_data):
            self.table_report.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_report.setItem(row, 1, QtWidgets.QTableWidgetItem(date))
            self.table_report.setItem(row, 2, QtWidgets.QTableWidgetItem(category))
            self.table_report.setItem(row, 3, QtWidgets.QTableWidgetItem(desc))
            self.table_report.setItem(row, 4, QtWidgets.QTableWidgetItem(amount))

            # Action column (optional view details button)
            view_btn = QtWidgets.QPushButton()
            view_btn.setObjectName("ReportTableBtnView")
            view_btn.setIcon(QtGui.QIcon("assets/icons/view.png"))  # Assume icon exists
            view_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            view_btn.setToolTip("View Details")
            view_btn.setFixedSize(30, 30)
            self.table_report.setCellWidget(row, 5, view_btn)

        table_lcds_h.addWidget(self.table_report, stretch=9)

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

        box_total_revenue, self.lcdTotalRevenue = _lcd_block(
            "Total Revenue", "lcdTotalRevenue"
        )
        box_total_expenditures, self.lcdTotalExpenditures = _lcd_block(
            "Total Expenditures", "lcdTotalExpenditures"
        )
        box_net_profit, self.lcdNetProfit = _lcd_block("Net Profit", "lcdNetProfit")

        lcds_v.addStretch()
        lcds_v.addWidget(box_total_revenue)
        lcds_v.addWidget(box_total_expenditures)
        lcds_v.addWidget(box_net_profit)

        table_lcds_h.addLayout(lcds_v, stretch=1)
        report_layout.addLayout(table_lcds_h)
