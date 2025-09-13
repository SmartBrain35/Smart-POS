from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSeries,
    QBarSet,
    QCategoryAxis,
    QValueAxis,
    QLineSeries,
)


class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        dashboard_layout = QtWidgets.QVBoxLayout(Dashboard)
        dashboard_layout.setContentsMargins(20, 20, 20, 20)
        dashboard_layout.setSpacing(15)

        # === Header Section ===
        header_label = QtWidgets.QLabel("Smart POS Dashboard Overview")
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #00c2ff;"
        )
        dashboard_layout.addWidget(header_label)

        # === KPI Cards Section ===
        kpi_layout = QtWidgets.QHBoxLayout()
        kpi_layout.setSpacing(20)

        def create_kpi_card(title, value, color="#00c2ff"):
            card = QtWidgets.QFrame()
            card.setStyleSheet(
                f"""
                QFrame {{
                    background-color: #1e1e2f;
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 10px;
                }}
            """
            )
            card_layout = QtWidgets.QVBoxLayout(card)
            card_layout.setSpacing(5)

            title_label = QtWidgets.QLabel(title)
            title_label.setStyleSheet("font-size: 16px; color: white;")
            title_label.setAlignment(QtCore.Qt.AlignCenter)

            value_label = QtWidgets.QLabel(value)
            value_label.setStyleSheet(
                f"font-size: 20px; font-weight: bold; color: {color};"
            )
            value_label.setAlignment(QtCore.Qt.AlignCenter)

            card_layout.addWidget(title_label)
            card_layout.addWidget(value_label)

            return card

        # Sample KPIs
        kpi_layout.addWidget(create_kpi_card("Total Sales", "GHS 15,240", "#00c2ff"))
        kpi_layout.addWidget(create_kpi_card("Total Profit", "GHS 4,560", "#19db33"))
        kpi_layout.addWidget(create_kpi_card("Return rate", "23%", "#e610b7"))
        kpi_layout.addWidget(create_kpi_card("Damage rate", "18%", "#f01f1f"))
        kpi_layout.addWidget(create_kpi_card("Low Stock Items", "12", "#f07523"))
        kpi_layout.addWidget(create_kpi_card("Expiring Soon", "5", "#f3c808"))

        dashboard_layout.addLayout(kpi_layout)

        # === Graphs Section ===
        graphs_layout = QtWidgets.QHBoxLayout()
        graphs_layout.setSpacing(20)

        # Sales Trend Line Chart
        sales_chart_view = self.create_sales_trend_chart()
        graphs_layout.addWidget(sales_chart_view)

        # Top Items Bar Chart
        top_items_chart_view = self.create_top_items_chart()
        graphs_layout.addWidget(top_items_chart_view)

        dashboard_layout.addLayout(graphs_layout)

        # === Recent Activity Table ===
        recent_table = QtWidgets.QTableWidget()
        recent_table.setObjectName("tableRecentActivity")
        recent_table.setColumnCount(4)
        recent_table.setHorizontalHeaderLabels(
            ["Time", "Type", "Description", "Amount"]
        )
        recent_table.horizontalHeader().setStretchLastSection(True)
        recent_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        recent_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        recent_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        recent_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        recent_table.setAlternatingRowColors(True)
        recent_table.verticalHeader().setVisible(False)

        # Sample data
        recent_data = [
            ("2025-09-11 14:30", "Sale", "Invoice #1234", "GHS 250"),
            ("2025-09-11 13:45", "Return", "Item X returned", "GHS -50"),
            ("2025-09-11 12:00", "Damage", "Item Y damaged", "GHS -30"),
            ("2025-09-11 11:15", "Expenditure", "Office supplies", "GHS -100"),
        ]

        recent_table.setRowCount(len(recent_data))
        for row, (time, typ, desc, amt) in enumerate(recent_data):
            recent_table.setItem(row, 0, QtWidgets.QTableWidgetItem(time))
            recent_table.setItem(row, 1, QtWidgets.QTableWidgetItem(typ))
            recent_table.setItem(row, 2, QtWidgets.QTableWidgetItem(desc))
            recent_table.setItem(row, 3, QtWidgets.QTableWidgetItem(amt))

        dashboard_layout.addWidget(recent_table, stretch=1)

        # Suggestions: Add a section for quick actions or notifications
        # For example, a list of alerts or buttons to navigate

    def create_sales_trend_chart(self):
        chart = QChart()
        chart.setTitle("Sales Trend (Last 7 Days)")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QLineSeries()
        # Sample data
        series.append(0, 1200)
        series.append(1, 1500)
        series.append(2, 1300)
        series.append(3, 1800)
        series.append(4, 1600)
        series.append(5, 2000)
        series.append(6, 1520)
        chart.addSeries(series)

        axisX = QCategoryAxis()
        axisX.append("Mon", 0)
        axisX.append("Tue", 1)
        axisX.append("Wed", 2)
        axisX.append("Thu", 3)
        axisX.append("Fri", 4)
        axisX.append("Sat", 5)
        axisX.append("Sun", 6)
        chart.addAxis(axisX, QtCore.Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTitleText("Sales (GHS)")
        chart.addAxis(axisY, QtCore.Qt.AlignLeft)
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_view.setStyleSheet(
            "background-color: #1e1e2f; border: 1px solid #00c2ff; border-radius: 10px;"
        )
        return chart_view

    def create_top_items_chart(self):
        chart = QChart()
        chart.setTitle("Top Selling Items")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QBarSeries()
        set0 = QBarSet("Sales")
        # Sample data
        set0 << 500 << 400 << 300 << 250 << 200
        series.append(set0)
        chart.addSeries(series)

        axisX = QCategoryAxis()
        categories = ["Item A", "Item B", "Item C", "Item D", "Item E"]
        for i, cat in enumerate(categories):
            axisX.append(cat, i)
        chart.addAxis(axisX, QtCore.Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setTitleText("Quantity Sold")
        chart.addAxis(axisY, QtCore.Qt.AlignLeft)
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_view.setStyleSheet(
            "background-color: #1e1e2f; border: 1px solid #00c2ff; border-radius: 10px;"
        )
        return chart_view
