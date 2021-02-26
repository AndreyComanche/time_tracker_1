from PyQt5 import QtGui, QtWidgets


class ControlButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumWidth(150)
        self.setMinimumHeight(32)
        font = QtGui.QFont('Consolas', 16, 4)
        self.setFont(font)
