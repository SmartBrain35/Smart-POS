import logging
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
    QMessageBox,
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


class Ui_Report(object):
    def setupUi(self, Report):
        logging.debug("Setting up Ui_Report")
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
        logging.debug("Ui_Report setup completed")

    def setup_filter_section(self):
        self.filter_section = QWidget()
        self.filter_section.setObjectName("FilterSection")
        filter_layout = QGridLayout(self.filter_section)
        filter_layout.setColumnStretch(0, 0)
        filter_layout.setColumnStretch(1, 1)
        filter_layout.setColumnStretch(2, 0)
        filter_layout.setColumnStretch(3, 1)
        filter_layout.setColumnStretch(4, 0)
        filter_layout.setColumnStretch(5, 1)
        filter_layout.setColumnStretch(6, 0)
        filter_layout.setColumnStretch(7, 0)

        filter_configs = [
            ("From:", "report_date_from", QDateEdit, QDate.currentDate().addMonths(-1)),
            ("To:", "report_date_to", QDateEdit, QDate.currentDate()),
            ("Category:", "report_category", QComboBox, None),
        ]

        self.filter_widgets = {}
        col = 0
        for label_text, obj_name, widget_type, default in filter_configs:
            lbl = QLabel(label_text)

            if widget_type == QDateEdit:
                widget = QDateEdit(default)
                widget.setCalendarPopup(True)
            elif widget_type == QComboBox:
                widget = QComboBox()
                widget.addItems(
                    ["All", "Sales", "Expenditures", "Damages", "Returns", "Stock"]
                )

            widget.setObjectName(obj_name)
            widget.setMinimumHeight(35)
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            filter_layout.addWidget(lbl, 0, col)
            filter_layout.addWidget(widget, 0, col + 1)

            self.filter_widgets[obj_name] = widget
            col += 2

        self.report_date_from = self.filter_widgets["report_date_from"]
        self.report_date_to = self.filter_widgets["report_date_to"]
        self.report_category = self.filter_widgets["report_category"]

        self.btn_generate_report = QPushButton("Generate PDF Report")
        self.btn_generate_report.setObjectName("BtnGenerateReport")
        self.btn_generate_report.setMinimumHeight(35)
        self.btn_generate_report.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filter_layout.addWidget(self.btn_generate_report, 0, col)

        self.btn_clear_report = QPushButton("Clear")
        self.btn_clear_report.setObjectName("BtnClearReport")
        self.btn_clear_report.setMinimumHeight(35)
        self.btn_clear_report.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filter_layout.addWidget(self.btn_clear_report, 0, col + 1)

    def setup_lcd_section(self):
        self.lcd_section = QWidget()
        self.lcd_section.setObjectName("LcdSection")
        lcd_layout = QVBoxLayout(self.lcd_section)

        lcd_configs = [
            ("Total Revenue", "LcdRevenue"),
            ("Total Expenditures", "LcdExpenditures"),
            ("Net Profit", "LcdProfit"),
        ]

        self.lcds = {}
        for title, obj_name in lcd_configs:
            box, lcd = self.create_lcd(title, obj_name)
            lcd_layout.addWidget(box)
            self.lcds[obj_name] = lcd

        self.lcd_revenue = self.lcds["LcdRevenue"]
        self.lcd_expenditures = self.lcds["LcdExpenditures"]
        self.lcd_profit = self.lcds["LcdProfit"]

    def setup_pdf_viewer(self):
        self.pdf_container = QWidget()
        self.pdf_container.setObjectName("PdfContainer")
        self.pdf_layout = QHBoxLayout(self.pdf_container)
        self.pdf_layout.setContentsMargins(0, 0, 0, 0)

        self.pdf_layout.addStretch()
        # Initialize QPdfView directly
        self.pdf_viewer = QPdfView()
        self.pdf_viewer.setObjectName("PdfViewer")
        self.pdf_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pdf_layout.addWidget(self.pdf_viewer)
        self.pdf_layout.addStretch()

        self.btn_print_report = QPushButton("Print Report")
        self.btn_print_report.setObjectName("BtnPrintReport")
        self.btn_print_report.setMinimumHeight(35)
        self.btn_print_report.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.pdf_layout.addWidget(self.btn_print_report)
        logging.debug("PDF viewer setup with QPdfView")

    def create_lcd(self, title, obj_name):
        wrapper = QWidget()
        layout = QVBoxLayout(wrapper)
        layout.setSpacing(5)

        label = QLabel(title)
        label.setObjectName(f"Label_{obj_name}")
        lcd = QLCDNumber()
        lcd.setObjectName(obj_name)
        lcd.setDigitCount(9)
        lcd.setMinimumHeight(40)

        layout.addWidget(label)
        layout.addWidget(lcd)
        return wrapper, lcd
