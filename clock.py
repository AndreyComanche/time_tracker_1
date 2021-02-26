from PyQt5 import QtGui, QtCore, QtWidgets
from datetime import datetime
from pytz import timezone


class ClockTable(QtWidgets.QGroupBox):
    def __init__(self, location, parent=None):
        super().__init__(parent)
        self.work_tz = timezone(location)
        font = QtGui.QFont('Consolas', 16, 1)
        self.setFont(font)
        location = location.split('/')[1].replace('_', ' ')
        self.setTitle(f"Time in {location}")
        self.date_label = QtWidgets.QLabel()
        font = QtGui.QFont('Consolas', 16, 50)
        self.date_label.setFont(font)
        self.time_label = QtWidgets.QLabel()
        font = QtGui.QFont('Consolas', 30, 100)
        self.time_label.setFont(font)
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.start_time = None
        self.init_ui()

    def init_ui(self):
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.date_label)
        vbox.addWidget(self.time_label)

    def timerEvent(self, tme):
        now = datetime.now(self.work_tz)
        self.date_label.setText(now.strftime('%A, %B %d'))
        self.time_label.setText(now.strftime('%H:%M:%S'))

    def get_time(self):
        return datetime.now(self.work_tz)

    def get_date(self):
        return datetime.now(self.work_tz).strftime('%Y.%m.%d')
