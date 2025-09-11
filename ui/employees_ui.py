from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Employees(object):
    def setupUi(self, Employees):
        employees_layout = QtWidgets.QVBoxLayout(Employees)
        employees_layout.setContentsMargins(20, 20, 20, 20)
        employees_layout.setSpacing(20)

        # === Form Section (Grid Layout, labels on top with tight spacing) ===
        form_container = QtWidgets.QWidget()
        form_container.setFixedWidth(950)
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setHorizontalSpacing(35)
        form_layout.setVerticalSpacing(25)

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

        # Name (compulsory)
        self.emp_name = QtWidgets.QLineEdit()
        self.emp_name.setObjectName("empNameInput")
        self.emp_name.setPlaceholderText("Enter employee name")
        self.emp_name.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Name:", self.emp_name, compulsory=True), 0, 0, 1, 2
        )

        # Phone (compulsory)
        self.emp_phone = QtWidgets.QLineEdit()
        self.emp_phone.setObjectName("empPhoneInput")
        self.emp_phone.setPlaceholderText("Enter phone number")
        self.emp_phone.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Phone:", self.emp_phone, compulsory=True), 0, 2, 1, 2
        )

        # Ghana Card ID (compulsory)
        self.emp_card = QtWidgets.QLineEdit()
        self.emp_card.setObjectName("empCardInput")
        self.emp_card.setPlaceholderText("Enter Ghana card ID")
        self.emp_card.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Ghana Card ID:", self.emp_card, compulsory=True), 1, 0, 1, 2
        )

        # Address
        self.emp_address = QtWidgets.QLineEdit()
        self.emp_address.setObjectName("empAddressInput")
        self.emp_address.setPlaceholderText("Enter address")
        self.emp_address.setFixedHeight(40)
        form_layout.addWidget(create_field("Address:", self.emp_address), 1, 2, 1, 2)

        # Designation (changed to ComboBox)
        self.emp_designation = QtWidgets.QComboBox()
        self.emp_designation.setObjectName("empDesignationInput")
        self.emp_designation.addItems(["Admin", "Manager", "Sales Rep"])
        self.emp_designation.setFixedHeight(40)
        form_layout.addWidget(
            create_field("Designation:", self.emp_designation), 2, 0, 1, 2
        )

        # Salary
        self.emp_salary = QtWidgets.QLineEdit()
        self.emp_salary.setObjectName("empSalaryInput")
        self.emp_salary.setPlaceholderText("Enter salary")
        self.emp_salary.setFixedHeight(40)
        form_layout.addWidget(create_field("Salary:", self.emp_salary), 2, 2, 1, 2)

        # Buttons Row
        btn_width = int(form_container.width() * 0.35)

        self.btn_add_employee = QtWidgets.QPushButton("ADD EMPLOYEE")
        self.btn_add_employee.setObjectName("btnAddEmployee")
        self.btn_add_employee.setFixedWidth(btn_width)

        self.btn_clear_employee = QtWidgets.QPushButton("CLEAR")
        self.btn_clear_employee.setObjectName("btnClearEmployee")
        self.btn_clear_employee.setFixedWidth(btn_width)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.btn_add_employee)
        btn_row.addWidget(self.btn_clear_employee)
        btn_row.addStretch()
        form_layout.addLayout(btn_row, 3, 0, 1, 4)

        # Center the form
        form_wrapper = QtWidgets.QHBoxLayout()
        form_wrapper.addStretch()
        form_wrapper.addWidget(form_container)
        form_wrapper.addStretch()
        employees_layout.addLayout(form_wrapper)

        # === Filter Section ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setSpacing(10)

        self.btn_filter = QtWidgets.QPushButton("Filter")
        self.btn_filter.setObjectName("btnFilter")

        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setObjectName("filterInput")
        self.filter_input.setPlaceholderText("Filter by Phone or Ghana Card ID...")
        self.filter_input.setFixedHeight(40)
        self.filter_input.setFixedWidth(int(form_container.width() * 0.3))  # 30% width

        filter_container.addWidget(self.btn_filter)
        filter_container.addWidget(self.filter_input)
        filter_container.addStretch()

        employees_layout.addLayout(filter_container)

        # === Table Section ===
        self.table_employees = QtWidgets.QTableWidget()
        self.table_employees.setObjectName("tableEmployees")
        self.table_employees.setColumnCount(9)  # added Action column
        self.table_employees.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Phone",
                "Ghana Card ID",
                "Address",
                "Designation",
                "Salary",
                "Date Added",
                "Action",
            ]
        )
        self.table_employees.horizontalHeader().setStretchLastSection(True)
        self.table_employees.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table_employees.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.table_employees.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table_employees.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )
        self.table_employees.setAlternatingRowColors(True)
        self.table_employees.verticalHeader().setVisible(False)

        # Sample employee data
        employees_data = [
            (
                1,
                "John Doe",
                "0244000011",
                "GHA-123456789",
                "Accra",
                "Cashier",
                "1500",
                "2025-08-01",
            ),
            (
                2,
                "Mary Jane",
                "0244000022",
                "GHA-987654321",
                "Kumasi",
                "Manager",
                "3500",
                "2025-08-10",
            ),
            (
                3,
                "Peter Mensah",
                "0244000033",
                "GHA-555111222",
                "Takoradi",
                "Sales Rep",
                "2000",
                "2025-08-20",
            ),
        ]

        self.table_employees.setRowCount(len(employees_data))

        for row, (uid, name, phone, card, addr, desig, salary, date) in enumerate(
            employees_data
        ):
            self.table_employees.setItem(row, 0, QtWidgets.QTableWidgetItem(str(uid)))
            self.table_employees.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.table_employees.setItem(row, 2, QtWidgets.QTableWidgetItem(phone))
            self.table_employees.setItem(row, 3, QtWidgets.QTableWidgetItem(card))
            self.table_employees.setItem(row, 4, QtWidgets.QTableWidgetItem(addr))
            self.table_employees.setItem(row, 5, QtWidgets.QTableWidgetItem(desig))
            self.table_employees.setItem(row, 6, QtWidgets.QTableWidgetItem(salary))
            self.table_employees.setItem(row, 7, QtWidgets.QTableWidgetItem(date))

            # Action column with delete button
            delete_btn = QtWidgets.QPushButton()
            delete_btn.setObjectName("EmpTableBtnDelete")
            delete_btn.setIcon(QtGui.QIcon("assets/icons/delete.png"))
            delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            delete_btn.setToolTip("Delete")
            delete_btn.setFixedSize(30, 30)
            self.table_employees.setCellWidget(row, 8, delete_btn)

        employees_layout.addWidget(self.table_employees)
