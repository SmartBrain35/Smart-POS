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
from PySide6.QtCore import Qt, QDate, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtPrintSupport import QPrinter, QPrintDialog


class Ui_Report(object):
    def setupUi(self, Report):
        Report.setObjectName("ReportPage")
        self.report_layout = QVBoxLayout(Report)
        self.report_layout.setContentsMargins(15, 15, 15, 15)
        self.report_layout.setSpacing(15)

        # === Filter Section ===
        self.setup_filter_section()
        self.report_layout.addWidget(self.filter_section)

        # === Content Section for PDF and LCDs ===
        self.content_widget = QWidget()
        content_layout = QHBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)

        # === PDF Viewer Centered ===
        self.setup_pdf_viewer()
        content_layout.addWidget(self.pdf_container, stretch=1)

        # === Right Side for LCDs ===
        self.right_side = QWidget()
        right_layout = QVBoxLayout(self.right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addStretch(1)  # Push LCDs to bottom

        # === LCD Section (Vertical) ===
        self.setup_lcd_section()
        right_layout.addWidget(self.lcd_section)

        content_layout.addWidget(self.right_side)
        self.report_layout.addWidget(self.content_widget, stretch=1)

    def setup_filter_section(self):
        self.filter_section = QWidget()
        self.filter_section.setObjectName("FilterSection")
        filter_layout = QGridLayout(self.filter_section)

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

    def setup_lcd_section(self):
        self.lcd_section = QWidget()
        self.lcd_section.setObjectName("LcdSection")
        lcd_layout = QVBoxLayout(self.lcd_section)

        revenue_box, self.lcd_revenue = self.create_lcd("Total Revenue", "LcdRevenue")
        exp_box, self.lcd_expenditures = self.create_lcd(
            "Total Expenditures", "LcdExpenditures"
        )
        profit_box, self.lcd_profit = self.create_lcd("Net Profit", "LcdProfit")

        lcd_layout.addWidget(revenue_box)
        lcd_layout.addWidget(exp_box)
        lcd_layout.addWidget(profit_box)

    def setup_pdf_viewer(self):
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

        # Add Print Button (new feature)
        self.btn_print_report = QPushButton("Print Report")
        self.btn_print_report.setFixedHeight(35)
        self.btn_print_report.setObjectName("BtnPrintReport")
        pdf_layout.addWidget(self.btn_print_report)

    def create_lcd(self, title, obj_name):
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
