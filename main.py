from PyQt5 import QtWidgets, QtCore
from clock import ClockTable
from task_time import TaskTime
from control_button import ControlButton
from task_list import TaskList
from availability_check import AvailabilityCheck, BrowserScreening
from login import Login
from dbase import Storage
from __init__ import __version__
import sys


class TrackerWindow(QtWidgets.QMainWindow):
    begin_task = QtCore.pyqtSignal()
    cancel_task = QtCore.pyqtSignal()
    complete_task = QtCore.pyqtSignal()

    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.app = application
        self.timer = self.startTimer(1000, QtCore.Qt.PreciseTimer)
        self.clock = ClockTable('America/Los_Angeles')
        self.task_time = TaskTime('Task time')
        self.btn_start = ControlButton('Start')
        self.btn_del = ControlButton('Delete')
        self.task_check = AvailabilityCheck()
        self.db = Storage()
        self.task_list = TaskList(
            'Timing',
            self.db.get_model(self.clock.get_date()[:7]),
            self
        )
        self.b_screening = BrowserScreening()
        self.login = Login(self.app)
        self.init_connections()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Time Tracker {__version__}')
        self.resize(640, 400)
        self.setWindowFlags(
            QtCore.Qt.MSWindowsFixedSizeDialogHint
        )
        content = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(content)
        for item in (self.clock, self.task_time, self.task_list,
                     self.btn_start, self.btn_del, self.task_check,
                     self.login):
            item.setParent(content)

        grid.addWidget(self.clock, 0, 0)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.task_time)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.btn_start)
        hbox.addWidget(self.btn_del)
        vbox.addLayout(hbox)
        grid.addLayout(vbox, 0, 1)
        grid.addWidget(self.task_check, 1, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        grid.addWidget(self.task_list, 2, 0, 1, 2, alignment=QtCore.Qt.AlignCenter)
        self.setCentralWidget(content)

    def init_connections(self):
        self.btn_start.clicked.connect(self.start_task)
        self.btn_del.clicked.connect(self.delete_task)
        self.task_time.endTask.connect(self.add_task)

        self.begin_task.connect(lambda: self.btn_start.setText('Complete'))
        self.begin_task.connect(lambda: self.btn_del.setText('Cancel'))
        self.begin_task.connect(lambda: self.task_time.init_pb(on_start=False))
        self.begin_task.connect(self.task_time.start)
        self.begin_task.connect(self.clock.start)
        self.begin_task.connect(self.b_screening.stop)
        self.begin_task.connect(self.task_check.stop)

        self.complete_task.connect(lambda: self.task_time.init_pb(on_start=False))
        self.complete_task.connect(lambda: self.btn_start.setText('Start'))
        self.complete_task.connect(lambda: self.btn_del.setText('Delete'))

        self.cancel_task.connect(lambda: self.task_time.init_pb(on_start=False))
        self.cancel_task.connect(lambda: self.btn_start.setText('Start'))
        self.cancel_task.connect(lambda: self.btn_del.setText('Delete'))

        self.task_check.start_check.connect(self.b_screening.start)
        self.task_check.stop_check.connect(self.b_screening.stop)
        self.task_check.login.connect(self.login.login)
        self.task_check.logout.connect(self.login.logout)

        self.b_screening.task_av.connect(self.task_check.reset)
        self.login.login_success.connect(self.task_check.stop)
        self.login.login_success.connect(self.b_screening.stop)
        self.login.logout_success.connect(self.task_check.start)
        self.login.logout_success.connect(self.b_screening.start)

    def timerEvent(self, tme):
        self.clock.timerEvent(tme)
        self.task_time.timerEvent(tme)
        self.b_screening.timerEvent(tme)

    @QtCore.pyqtSlot()
    def start_task(self):
        if self.task_time.is_active():
            self.add_task()
        else:
            self.begin_task.emit()

    @QtCore.pyqtSlot()
    def add_task(self):
        self.complete_task.emit()
        self.db.insert(
            self.clock.start_time,
            self.clock.get_time(),
            self.task_time.value
        )
        self.task_list.task_list.setModel(
            self.db.get_model(self.clock.get_date()[:7])
        )
        self.task_list.init_ui(on_start=False)

    @QtCore.pyqtSlot()
    def delete_task(self):
        if self.task_time.is_active():
            self.cancel_task.emit()
        else:
            for index in self.task_list.task_list.selectedIndexes():
                if index.isValid():
                    item_id = index.data(QtCore.Qt.UserRole)
                    try:
                        int(item_id)
                    except ValueError:
                        continue
                    self.db.delete(item_id)
                    self.task_list.task_list.setModel(
                        self.db.get_model(
                            self.clock.get_date()[:7]))
                    self.task_list.init_ui(on_start=False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TrackerWindow(app)
    window.show()
    sys.exit(app.exec())
