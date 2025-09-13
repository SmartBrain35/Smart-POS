import tempfile
import os
from PySide6.QtCore import QDate, QUrl
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm


class ReportController:
    def __init__(self, ui):
        self.ui = ui
        self.filtered_data = []
        self.sample_data = [
            {
                "id": 1,
                "date": "2025-09-01",
                "category": "Sales",
                "description": "Product Sale",
                "amount": "1000.00",
            },
            {
                "id": 2,
                "date": "2025-09-05",
                "category": "Expenditures",
                "description": "Office Rent",
                "amount": "5000.00",
            },
            {
                "id": 3,
                "date": "2025-09-10",
                "category": "Damages",
                "description": "Broken Item",
                "amount": "200.00",
            },
            {
                "id": 4,
                "date": "2025-09-20",
                "category": "Sales",
                "description": "Service",
                "amount": "2500.00",
            },
        ]

        self.ui.btn_generate_report.clicked.connect(self.generate_report)
        self.ui.btn_clear_report.clicked.connect(self.clear_report)

        # set up PDF viewer
        self.ui.pdf_viewer.setHtml("<h3>No report generated yet</h3>")

    def generate_report(self):
        from_date = self.ui.report_date_from.date()
        to_date = self.ui.report_date_to.date()
        category = self.ui.report_category.currentText()

        self.filtered_data = [
            item
            for item in self.sample_data
            if (from_date <= QDate.fromString(item["date"], "yyyy-MM-dd") <= to_date)
            and (category == "All" or item["category"] == category)
        ]

        # Update LCDs so user sees if there's data
        self.update_lcds()

        # Build and preview PDF
        self.generate_pdf_preview()

    def generate_pdf_preview(self):
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Smart POS - Report", styles["Title"]))
        elements.append(Spacer(1, 12))

        if not self.filtered_data:
            elements.append(
                Paragraph("No data available for selected filters.", styles["Normal"])
            )
        else:
            table_data = [["ID", "Date", "Category", "Description", "Amount"]]
            for item in self.filtered_data:
                table_data.append(
                    [
                        str(item["id"]),
                        item["date"],
                        item["category"],
                        item["description"],
                        item["amount"],
                    ]
                )

            table = Table(table_data, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ]
                )
            )
            elements.append(table)

        # Footer callback
        def add_footer(canvas_obj, doc_obj):
            page_num = canvas_obj.getPageNumber()
            text = f"Page {page_num}"
            canvas_obj.setFont("Helvetica", 9)
            # Use mm since imported
            canvas_obj.drawRightString((letter[0] - 20 * mm), 15 * mm, text)

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_path = tmp.name

        doc = SimpleDocTemplate(tmp_path, pagesize=letter)
        doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)

        # Load into the viewer
        if os.path.exists(tmp_path):
            self.ui.pdf_viewer.load(QUrl.fromLocalFile(tmp_path))
        else:
            QMessageBox.critical(
                None, "Error", "Could not generate PDF file for preview."
            )

    def update_lcds(self):
        sales = sum(
            float(item["amount"])
            for item in self.filtered_data
            if item["category"] == "Sales"
        )
        expenditures = sum(
            float(item["amount"])
            for item in self.filtered_data
            if item["category"] == "Expenditures"
        )
        net = sales - expenditures

        self.ui.lcd_revenue.display(sales)
        self.ui.lcd_expenditures.display(expenditures)
        self.ui.lcd_profit.display(net)

    def clear_report(self):
        self.ui.report_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.ui.report_date_to.setDate(QDate.currentDate())
        self.ui.report_category.setCurrentIndex(0)
        self.filtered_data = []
        self.ui.lcd_revenue.display(0)
        self.ui.lcd_expenditures.display(0)
        self.ui.lcd_profit.display(0)
        self.ui.pdf_viewer.setHtml("<h3>No report generated yet</h3>")
