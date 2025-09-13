from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Account(object):
    def setupUi(self, Account):
        account_layout = QtWidgets.QVBoxLayout(Account)
        account_layout.setContentsMargins(20, 20, 20, 20)
        account_layout.setSpacing(15)

        # === Form Section (Grid Layout, labels on top, tighter spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(850)
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

        # Sample data (6 cols now, no "Status")
        users_data = [
            (1, "Admin User", "0244000001", "admin@pos.com", "Admin"),
            (2, "Cashier One", "0244000002", "cashier@pos.com", "Cashier"),
            (3, "Manager One", "0244000003", "manager@pos.com", "Manager"),
        ]

        self.table_users.setRowCount(len(users_data))

        for row, (uid, name, phone, email, role) in enumerate(users_data):
            self.table_users.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_users.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_users.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
            self.table_users.setItem(row, 3, QtWidgets.QTableWidgetItem(email))
            self.table_users.setItem(row, 4, QtWidgets.QTableWidgetItem(role))

            # --- Action cell with icons ---
            action_widget = QtWidgets.QWidget()
            action_layout = QtWidgets.QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(15)

            btn_edit = QtWidgets.QPushButton()
            btn_edit.setObjectName("tableBtnEdit")
            btn_edit.setIcon(QtGui.QIcon("assets/icons/edit.png"))
            btn_edit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn_edit.setToolTip("Edit User")
            btn_edit.setFixedSize(30, 30)

            btn_delete = QtWidgets.QPushButton()
            btn_delete.setObjectName("tableBtnDelete")
            btn_delete.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            btn_delete.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            btn_delete.setToolTip("Delete User")
            btn_delete.setFixedSize(30, 30)

            action_layout.addStretch()
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.addStretch()

            self.table_users.setCellWidget(row, 5, action_widget)

        account_layout.addWidget(self.table_users, stretch=1)
