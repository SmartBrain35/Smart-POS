from PySide6 import QtCore, QtGui, QtWidgets


class Ui_SimplePage(object):
    def __init__(self, text, style_sheet=""):
        self.text = text
        self.style_sheet = style_sheet

    def setupUi(self, Page):
        layout = QtWidgets.QVBoxLayout(Page)
        label = QtWidgets.QLabel(self.text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet(self.style_sheet)
        layout.addWidget(label)
