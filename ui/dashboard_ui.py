from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSeries,
    QBarSet,
    QCategoryAxis,
    QValueAxis,
    QPieSeries,
    QPieSlice,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect, QDialog, QListWidget


class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        dashboard_layout = QtWidgets.QVBoxLayout(Dashboard)
        dashboard_layout.setContentsMargins(20, 20, 20, 20)
        dashboard_layout.setSpacing(15)

        # === Header Section ===
        header_container = QtWidgets.QWidget()
        header_container_layout = QtWidgets.QHBoxLayout(header_container)
        header_container_layout.setContentsMargins(0, 0, 0, 0)

        self.alert_button = QtWidgets.QPushButton("🔔", header_container)
        self.alert_button.setFlat(True)

        self.alert_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 24px;
                color: #f3c808;
            }
            QPushButton:hover {
                color: #ffffff;
            }
            """
        )
        self.alert_button.setFixedSize(40, 40)
        self.alert_button.clicked.connect(self.show_notification_ui)

        header_container_layout.addStretch()
        header_container_layout.addWidget(self.alert_button)

        dashboard_layout.addWidget(header_container)

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
                QFrame:hover {{
                    background-color: #28283a;
                    border: 2px solid #ffffff;
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
        kpi_layout.addWidget(create_kpi_card("Low Items", "12", "#f07523"))
        kpi_layout.addWidget(create_kpi_card("Expiring Soon", "5", "#f3c808"))

        dashboard_layout.addLayout(kpi_layout)

        # === Graphs Section ===
        graphs_layout = QtWidgets.QHBoxLayout()
        graphs_layout.setSpacing(20)

        # Sales Trend Line Chart
        sales_chart_view = self.create_sales_trend_chart()
        sales_chart_view.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        graphs_layout.addWidget(sales_chart_view)

        # Top Items Pie Chart
        top_items_chart_view = self.create_top_items_chart()
        top_items_chart_view.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        graphs_layout.addWidget(top_items_chart_view)

        dashboard_layout.addLayout(graphs_layout)

        # System Tray Notification
        self.tray_icon = QtWidgets.QSystemTrayIcon(Dashboard)
        icon = QtGui.QIcon("alert.png")
        if not icon.isNull():
            self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("Expiring Soon Alert")
        self.tray_icon.activated.connect(
            lambda reason: (
                self.show_notification_ui()
                if reason == QtWidgets.QSystemTrayIcon.Trigger
                else None
            )
        )
        self.tray_icon.show()

        # Expiring Items (sample)
        self.expiring_items = ["a", "b", "c", "d", "e"]
        items_list = ", ".join(self.expiring_items)

        # Show tray notification if expiring items > 0
        if len(self.expiring_items) > 0:
            self.tray_icon.showMessage("Expiring Soon", f"items({items_list})")

            # Animate alert icon
            self.opacity_effect = QGraphicsOpacityEffect()
            self.alert_button.setGraphicsEffect(self.opacity_effect)
            self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
            self.animation.setDuration(1000)
            self.animation.setStartValue(1.0)
            self.animation.setEndValue(0.2)
            self.animation.setLoopCount(-1)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutSine)
            self.animation.start()

    def show_notification_ui(self):
        dialog = QDialog()
        dialog.setWindowTitle("Expiring Soon Items")
        layout = QtWidgets.QVBoxLayout(dialog)

        list_widget = QListWidget()
        for item in self.expiring_items:
            list_widget.addItem(item)
        layout.addWidget(list_widget)

        ok_button = QtWidgets.QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)

        dialog.exec()

    def create_sales_trend_chart(self):
        chart = QChart()
        chart.setTitle("Sales Trend (Last 7 Days)")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QBarSeries()
        set0 = QBarSet("Sales")
        # Sample data
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        sales = [1200, 1500, 1300, 1800, 1600, 2000, 1520]
        for val in sales:
            set0.append(val)
        series.append(set0)
        chart.addSeries(series)

        axisX = QCategoryAxis()
        for i, day in enumerate(days):
            axisX.append(day, i)
        chart.addAxis(axisX, QtCore.Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setLabelFormat("%i")
        axisY.setTitleText("Sales (GHS)")
        chart.addAxis(axisY, QtCore.Qt.AlignLeft)
        series.attachAxis(axisY)

        def on_bar_hover(status, index, barset):
            if status:
                day = days[index]
                value = barset.at(index)
                QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), f"{day}: {value} GHS")
            else:
                QtWidgets.QToolTip.hideText()

        series.hovered.connect(on_bar_hover)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_view.setStyleSheet(
            """
            QChartView {
                background-color: #1e1e2f;
                border: 1px solid #00c2ff;
                border-radius: 10px;
            }
            QChartView:hover {
                border: 2px solid #ffffff;
            }
            """
        )
        return chart_view

    def create_top_items_chart(self):
        chart = QChart()
        chart.setTitle("Top Selling Items")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QPieSeries()
        # Sample data
        items = ["Item A", "Item B", "Item C", "Item D", "Item E"]
        quantities = [500, 400, 300, 250, 200]
        for item, q in zip(items, quantities):
            series.append(item, q)
        chart.addSeries(series)

        def on_slice_hover(pie_slice, state):
            if state:
                QtWidgets.QToolTip.showText(
                    QtGui.QCursor.pos(), f"{pie_slice.label()}: {pie_slice.value()} sold"
                )
            else:
                QtWidgets.QToolTip.hideText()

        series.hovered.connect(on_slice_hover)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_view.setStyleSheet(
            """
            QChartView {
                background-color: #1e1e2f;
                border: 1px solid #00c2ff;
                border-radius: 10px;
            }
            QChartView:hover {
                border: 2px solid #ffffff;
            }
            """
        )
        return chart_view