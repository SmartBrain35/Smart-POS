from PySide6 import QtCore, QtGui, QtWidgets


class Ui_Employees(object):
    def setupUi(self, Employees):
        Employees.setObjectName("page_employees")

        employees_layout = QtWidgets.QVBoxLayout(Employees)
        employees_layout.setContentsMargins(20, 20, 20, 20)
        employees_layout.setSpacing(10)

        # === Form Section ===
        form_container = QtWidgets.QWidget()
        form_container.setObjectName("formContainer")
        form_layout = QtWidgets.QGridLayout(form_container)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(8)  # reduce spacing for tighter layout

        label_style = "color: black; font-weight: bold;"

        def form_field(label_text, widget, compulsory=False):
            wrapper = QtWidgets.QWidget()
            vbox = QtWidgets.QVBoxLayout(wrapper)
            vbox.setContentsMargins(0, 0, 0, 0)
            vbox.setSpacing(2)  # minimal spacing between label and input

            lbl = QtWidgets.QLabel(label_text + (" *" if compulsory else ""))
            if compulsory:
                lbl.setStyleSheet("color: red; font-weight: bold;")
            else:
                lbl.setStyleSheet(label_style)

            vbox.addWidget(lbl)
            vbox.addWidget(widget)
            return wrapper

        def styled_lineedit(object_name, placeholder):
            le = QtWidgets.QLineEdit()
            le.setObjectName(object_name)
            le.setPlaceholderText(placeholder)
            le.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
            )
            le.setMinimumHeight(36)
            return le

        # Name
        self.emp_name = styled_lineedit("empNameInput", "Enter employee name")
        form_layout.addWidget(form_field("Name", self.emp_name, True), 0, 0)

        # Phone
        self.emp_phone = styled_lineedit("empPhoneInput", "Enter phone number")
        form_layout.addWidget(form_field("Phone", self.emp_phone, True), 0, 1)

        # Ghana Card
        self.emp_card = styled_lineedit("empCardInput", "Enter Ghana card ID")
        form_layout.addWidget(form_field("Ghana Card ID", self.emp_card, True), 1, 0)

        # Address
        self.emp_address = styled_lineedit("empAddressInput", "Enter address")
        form_layout.addWidget(form_field("Address", self.emp_address), 1, 1)

        # Designation
        self.emp_designation = QtWidgets.QComboBox()
        self.emp_designation.setObjectName("empDesignationInput")
        self.emp_designation.addItems(["Admin", "Manager", "Sales Rep"])
        self.emp_designation.setMinimumHeight(36)
        form_layout.addWidget(form_field("Designation", self.emp_designation), 2, 0)

        # Salary
        self.emp_salary = styled_lineedit("empSalaryInput", "Enter salary")
        form_layout.addWidget(form_field("Salary", self.emp_salary), 2, 1)

        # Buttons Row
        self.btn_add_employee = QtWidgets.QPushButton("ADD EMPLOYEE")
        self.btn_add_employee.setObjectName("btnAddEmployee")
        self.btn_add_employee.setMinimumHeight(36)

        self.btn_clear_employee = QtWidgets.QPushButton("CLEAR")
        self.btn_clear_employee.setObjectName("btnClearEmployee")
        self.btn_clear_employee.setMinimumHeight(36)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(self.btn_add_employee)
        btn_row.addWidget(self.btn_clear_employee)
        btn_row.addStretch()
        form_layout.addLayout(btn_row, 3, 0, 1, 2)

        # Form shouldn't steal vertical space
        form_container.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
        )
        employees_layout.addWidget(form_container)

        # === Filter Section ===
        filter_container = QtWidgets.QHBoxLayout()
        filter_container.setContentsMargins(0, 0, 0, 0)

        self.filter_input = styled_lineedit(
            "filterInput", "Filter by Phone or Ghana Card ID..."
        )
        self.filter_input.setMaximumWidth(350)

        filter_container.addStretch()
        filter_container.addWidget(self.filter_input)
        employees_layout.addLayout(filter_container)

        # === Table Section ===
        self.table_employees = QtWidgets.QTableWidget()
        self.table_employees.setObjectName("tableEmployees")
        self.table_employees.setColumnCount(9)
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
        self.table_employees.setShowGrid(False)

        # Let the table take all leftover space
        self.table_employees.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        employees_layout.addWidget(self.table_employees)
