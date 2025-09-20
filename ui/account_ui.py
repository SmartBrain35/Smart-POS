from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Account(object):
    def setupUi(self, Account):
        account_layout = QtWidgets.QVBoxLayout(Account)
        account_layout.setContentsMargins(20, 20, 20, 20)
        account_layout.setSpacing(15)

        # === Form Section (Grid Layout, labels on top, tighter spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setMinimumWidth(850)  # Changed to minimum for responsiveness
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(25)
        form_layout.setVerticalSpacing(6)

        label_style = "color: black; font-weight: bold;"

        def create_field(label_text, widget):
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(2)
            lbl = QtWidgets.QLabel(label_text)
            lbl.setStyleSheet(label_style)
            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        # Inputs
        self.input_name = QtWidgets.QLineEdit()
        self.input_name.setObjectName("inputAccountName")
        self.input_name.setPlaceholderText("Enter name")
        self.input_name.setFixedHeight(40)
        form_layout.addWidget(create_field("Name:", self.input_name), 0, 0, 1, 2)

        self.input_phone = QtWidgets.QLineEdit()
        self.input_phone.setObjectName("inputAccountPhone")
        self.input_phone.setPlaceholderText("Enter phone number")
        self.input_phone.setFixedHeight(40)
        form_layout.addWidget(create_field("Phone:", self.input_phone), 0, 2, 1, 2)

        self.input_email = QtWidgets.QLineEdit()
        self.input_email.setObjectName("inputAccountEmail")
        self.input_email.setPlaceholderText("Enter email")
        self.input_email.setFixedHeight(40)
        form_layout.addWidget(create_field("Email:", self.input_email), 1, 0, 1, 2)

        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setObjectName("inputAccountPassword")
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_password.setPlaceholderText("Enter password")
        self.input_password.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Password:", self.input_password), 1, 2, 1, 2
        )

        self.input_role = QtWidgets.QComboBox()
        self.input_role.setObjectName("inputAccountRole")
        self.input_role.addItems(["Admin", "Manager", "Cashier", "Sales Person"])
        self.input_role.setFixedHeight(40)
        form_layout.addWidget(create_field("Role:", self.input_role), 2, 0, 1, 2)

        # Buttons - reduced width
        self.btn_register = QtWidgets.QPushButton("ADD")
        self.btn_register.setObjectName("btnAccountRegister")
        self.btn_register.setFixedWidth(120)

        self.btn_edit = QtWidgets.QPushButton("EDIT")
        self.btn_edit.setObjectName("btnAccountEdit")
        self.btn_edit.setFixedWidth(120)

        self.btn_clear = QtWidgets.QPushButton("CLEAR")
        self.btn_clear.setObjectName("btnAccountClear")
        self.btn_clear.setFixedWidth(120)

        btn_widget = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)
        btn_layout.addWidget(self.btn_register)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_clear)

        # Place buttons beside Role field (same row, columns 2-3)
        form_layout.addWidget(btn_widget, 2, 2, 1, 2)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        account_layout.addLayout(form_wrapper)

        # === Filter Input (top-right of table, 30% width) ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setObjectName("filterInputAccount")
        self.filter_input.setPlaceholderText("Filter by Name or Email...")
        self.filter_input.setFixedHeight(40)
        self.filter_input.setMaximumWidth(
            int(form_container.minimumWidth() * 0.3)
        )  # 30% of form width
        self.filter_input.textChanged.connect(self.filter_table)
        filter_container.addStretch()  # Push to right
        filter_container.addWidget(self.filter_input)
        account_layout.addLayout(filter_container)

        # === Table Section ===
        self.table_users = QtWidgets.QTableWidget()
        self.table_users.setObjectName("tableUsers")
        self.table_users.setColumnCount(6)
        self.table_users.setHorizontalHeaderLabels(
            ["ID", "Name", "Phone", "Email", "Role", "Actions"]
        )
        self.table_users.horizontalHeader().setStretchLastSection(True)
        self.table_users.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_users.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_users.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_users.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_users.setAlternatingRowColors(True)
        self.table_users.verticalHeader().setVisible(False)

        account_layout.addWidget(self.table_users, stretch=1)

    def filter_table(self, text):
        # Manual filter for QTableWidget by hiding rows
        for row in range(self.table_users.rowCount()):
            match = False
            for col in [1, 3]:  # Name (col 1), Email (col 3)
                item = self.table_users.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.table_users.setRowHidden(row, not match)
