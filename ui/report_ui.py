from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QDateEdit,
    QComboBox,
    QPushButton,
    QLCDNumber,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtWebEngineWidgets import QWebEngineView


class Ui_Report(object):
    def setupUi(self, Report):
        Report.setObjectName("ReportPage")
        self.report_layout = QVBoxLayout(Report)
        self.report_layout.setContentsMargins(30, 30, 30, 30)
        self.report_layout.setSpacing(20)

        # === Filter Section ===
        filter_section = QWidget()
        filter_section.setObjectName("FilterSection")
        filter_layout = QGridLayout(filter_section)

        self.report_date_from = QDateEdit(QDate.currentDate().addMonths(-1))
        self.report_date_from.setCalendarPopup(True)
        self.report_date_from.setFixedHeight(35)
        self.report_date_from.setObjectName("InputDateFrom")

        self.report_date_to = QDateEdit(QDate.currentDate())
        self.report_date_to.setCalendarPopup(True)
        self.report_date_to.setFixedHeight(35)
        self.report_date_to.setObjectName("InputDateTo")

        self.report_category = QComboBox()
        self.report_category.addItems(
            ["All", "Sales", "Expenditures", "Damages", "Returns", "Stock"]
        )
        self.report_category.setFixedHeight(35)
        self.report_category.setObjectName("InputCategory")

        self.btn_generate_report = QPushButton("Generate PDF Report")
        self.btn_generate_report.setFixedHeight(35)
        self.btn_generate_report.setObjectName("BtnGenerateReport")

        self.btn_clear_report = QPushButton("Clear")
        self.btn_clear_report.setFixedHeight(35)
        self.btn_clear_report.setObjectName("BtnClearReport")

        filter_layout.addWidget(QLabel("From:"), 0, 0)
        filter_layout.addWidget(self.report_date_from, 0, 1)

        filter_layout.addWidget(QLabel("To:"), 0, 2)
        filter_layout.addWidget(self.report_date_to, 0, 3)

        filter_layout.addWidget(QLabel("Category:"), 1, 0)
        filter_layout.addWidget(self.report_category, 1, 1)

        filter_layout.addWidget(self.btn_generate_report, 1, 2)
        filter_layout.addWidget(self.btn_clear_report, 1, 3)

        self.report_layout.addWidget(filter_section)

        # === LCD Section ===
        lcd_section = QWidget()
        lcd_section.setObjectName("LcdSection")
        lcd_layout = QHBoxLayout(lcd_section)

        def create_lcd(title, obj_name):
            wrapper = QWidget()
            layout = QVBoxLayout(wrapper)
            layout.setSpacing(5)

            label = QLabel(title)
            label.setObjectName(f"Label_{obj_name}")
            lcd = QLCDNumber()
            lcd.setObjectName(obj_name)
            lcd.setDigitCount(9)
            lcd.setFixedHeight(40)

            layout.addWidget(label)
            layout.addWidget(lcd)
            return wrapper, lcd

        revenue_box, self.lcd_revenue = create_lcd("Total Revenue", "LcdRevenue")
        exp_box, self.lcd_expenditures = create_lcd(
            "Total Expenditures", "LcdExpenditures"
        )
        profit_box, self.lcd_profit = create_lcd("Net Profit", "LcdProfit")

        lcd_layout.addWidget(revenue_box)
        lcd_layout.addWidget(exp_box)
        lcd_layout.addWidget(profit_box)

        self.report_layout.addWidget(lcd_section)

        # === PDF Viewer Centered ===
        self.pdf_container = QWidget()
        self.pdf_container.setObjectName("PdfContainer")
        pdf_layout = QHBoxLayout(self.pdf_container)
        pdf_layout.setContentsMargins(0, 0, 0, 0)

        pdf_layout.addStretch()
        self.pdf_viewer = QWebEngineView()
        self.pdf_viewer.setMinimumSize(700, 900)
        self.pdf_viewer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.pdf_viewer.setObjectName("PdfViewer")
        pdf_layout.addWidget(self.pdf_viewer)
        pdf_layout.addStretch()

        self.report_layout.addWidget(self.pdf_container, stretch=1)
