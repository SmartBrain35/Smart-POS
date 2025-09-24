from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from backend.apis import DamageAPI


class DamageController:
    def __init__(self, ui):
        self.ui = ui
        self.load_damages()

        # Connect buttons
        self.ui.btnRecordDamage.clicked.connect(self.record_damage)
        self.ui.btnRefreshDamages.clicked.connect(self.load_damages)

    def load_damages(self):
        """Load all recorded damages into the table."""
        resp = DamageAPI.get_all_damages()
        if not resp.get("success"):
            QMessageBox.warning(
                self.ui, "Error", resp.get("error", "Failed to fetch damages")
            )
            return

        damages = resp["damages"]
        self.ui.tableDamages.setRowCount(0)

        for row, dmg in enumerate(damages):
            self.ui.tableDamages.insertRow(row)
            self.ui.tableDamages.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(dmg["id"]))
            )
            self.ui.tableDamages.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(dmg["stock_id"]))
            )
            self.ui.tableDamages.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(dmg["quantity_damaged"]))
            )
            self.ui.tableDamages.setItem(
                row, 3, QtWidgets.QTableWidgetItem(dmg["damage_status"])
            )
            self.ui.tableDamages.setItem(
                row, 4, QtWidgets.QTableWidgetItem(dmg["damage_date"])
            )
