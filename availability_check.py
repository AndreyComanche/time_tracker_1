from PyQt5 import QtGui, QtCore, QtWidgets
import pyautogui as ag

from control_button import ControlButton
from sound import TextToSpeech


class AvailabilityCheck(QtWidgets.QGroupBox):
    start_check = QtCore.pyqtSignal()
    stop_check = QtCore.pyqtSignal()
    login = QtCore.pyqtSignal()
    logout = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        font = QtGui.QFont('Consolas', 16, 50)
        self.setFont(font)
        self.setTitle("Checking the availability of tasks")
        self.setMinimumWidth(640)
        self.setMinimumHeight(80)
        self.check = True

        self.start_text = "Start check"
        self.stop_text = "Stop check"
        self.start_btn = ControlButton(self.stop_text, self)
        self.start_btn.setMaximumWidth(150)
        self.start_btn.setMinimumHeight(16)

        self.login_btn = ControlButton("Login", self)
        self.login_btn.setMaximumWidth(150)
        self.login_btn.setMinimumHeight(16)

        self.logout_btn = ControlButton("Logout", self)
        self.logout_btn.setMaximumWidth(150)
        self.logout_btn.setMinimumHeight(16)

        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setMinimumWidth(150)
        self.pbar.setMaximumHeight(16)
        font = QtGui.QFont("Consolas", 16, 50)
        self.pbar.setFont(font)
        self.pbar.setRange(0, 4)

        self.init_ui()
        self.init_connections()

    def init_ui(self):
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.start_btn)
        hbox.addWidget(self.pbar)
        hbox.addWidget(self.login_btn)
        hbox.addWidget(self.logout_btn)

    def init_connections(self):
        self.start_btn.clicked.connect(self.trigger)
        self.login_btn.clicked.connect(self.login.emit)
        self.logout_btn.clicked.connect(self.logout.emit)

    @QtCore.pyqtSlot()
    def trigger(self):
        self.check = not self.check
        if self.check:
            self.start_btn.setText(self.stop_text)
            self.start_check.emit()
        else:
            self.start_btn.setText(self.start_text)
            self.stop_check.emit()

    @QtCore.pyqtSlot(int)
    def reset(self, count):
        self.pbar.setValue(count)
        self.pbar.setFormat(str(count))

    @QtCore.pyqtSlot()
    def stop(self):
        self.start_btn.setText(self.start_text)
        self.check = False

    @QtCore.pyqtSlot()
    def start(self):
        self.start_btn.setText(self.stop_text)
        self.check = True


class BrowserScreening(QtCore.QObject):
    task_av = QtCore.pyqtSignal(int)

    def __init__(self):
        super(BrowserScreening, self).__init__()
        self.textEngine = TextToSpeech()
        self.count = 0
        self.rescan = 4
        self.monitoring = True

    def timerEvent(self, tme):
        if self.monitoring:
            self.count += 1
            self.task_av.emit(self.count)
            if self.count == self.rescan:
                self.check_task()
                self.count = 0

    def check_task(self):
        box = ag.locateOnScreen(r".\img\no_task.png", region=(0, 90, 90, 210))
        if box is None:
            self.textEngine.say()

    @QtCore.pyqtSlot()
    def start(self):
        self.count = 0
        self.monitoring = True
        self.check_task()

    @QtCore.pyqtSlot()
    def stop(self):
        self.monitoring = False
