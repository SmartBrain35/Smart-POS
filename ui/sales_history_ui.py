from PySide6 import QtWidgets, QtCore


class Ui_SalesHistory(object):
    def setupUi(self, SalesHistory):
        SalesHistory.setObjectName("SalesHistory")
        SalesHistory.resize(900, 600)

        # Main vertical layout
        self.verticalLayout = QtWidgets.QVBoxLayout(SalesHistory)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)

        # --- Top controls: Search, Date Filter, Refresh, Export ---
        self.controlsLayout = QtWidgets.QHBoxLayout()

        self.searchBox = QtWidgets.QLineEdit(SalesHistory)
        self.searchBox.setPlaceholderText("Search by invoice/customer...")
        self.searchBox.setStyleSheet("color: black; font-weight: bold")
        self.searchBox.setClearButtonEnabled(True)
        self.controlsLayout.addWidget(self.searchBox)

        self.dateFilter = QtWidgets.QDateEdit(SalesHistory)
        self.dateFilter.setStyleSheet("color: black; font-weight: bold")
        self.dateFilter.setCalendarPopup(True)
        self.dateFilter.setDisplayFormat("yyyy-MM-dd")
        self.dateFilter.setDate(QtCore.QDate.currentDate())
        self.controlsLayout.addWidget(self.dateFilter)

        self.refreshButton = QtWidgets.QPushButton("Refresh", SalesHistory)
        self.controlsLayout.addWidget(self.refreshButton)

        self.exportButton = QtWidgets.QPushButton("Export CSV", SalesHistory)
        self.controlsLayout.addWidget(self.exportButton)

        self.verticalLayout.addLayout(self.controlsLayout)

        # --- Sales History Table ---
        self.tableSalesHistory = QtWidgets.QTableView(SalesHistory)
        self.tableSalesHistory.setStyleSheet("color: black; font-weight: bold")
        self.tableSalesHistory.setAlternatingRowColors(True)
        self.tableSalesHistory.setSortingEnabled(True)
        self.tableSalesHistory.horizontalHeader().setStretchLastSection(True)
        self.tableSalesHistory.verticalHeader().setVisible(False)
        self.tableSalesHistory.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.tableSalesHistory.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.verticalLayout.addWidget(self.tableSalesHistory)

        # --- Status Bar Label ---
        self.labelStatus = QtWidgets.QLabel(SalesHistory)
        self.labelStatus.setText("Ready")
        self.labelStatus.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.labelStatus.setMinimumHeight(24)
        self.verticalLayout.addWidget(self.labelStatus)
