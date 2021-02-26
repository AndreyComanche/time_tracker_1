from PyQt5 import QtGui, QtCore, QtWidgets
from decimal import Decimal


class TaskTime(QtWidgets.QGroupBox):
    endTask = QtCore.pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(320)
        font = QtGui.QFont('Consolas', 16, 4)
        self.setFont(font)
        self.setTitle(text)
        self.value = Decimal('1.00')
        self.cb = QtWidgets.QComboBox(self)
        self.cb_values = []
        self.pbar = QtWidgets.QProgressBar(self)
        self.__pbar_active = False
        self.init_ui()

    def init_ui(self):
        self.init_cb()
        self.init_pb()
        vbox = QtWidgets.QHBoxLayout(self)
        vbox.addWidget(self.cb, alignment=QtCore.Qt.AlignCenter)
        vbox.addWidget(self.pbar, alignment=QtCore.Qt.AlignCenter)

    def init_cb(self):
        self.cb_values = [
            '1.00', '1.50', '2.00', '2.50', '3.00',
            '4.00', '4.50', '5.00', '5.80', '6.00',
            '6.30', '7.00', '7.50', '8.00', '9.00'
        ]
        font = QtGui.QFont('Consolas', 16, 4)
        self.cb.setFont(font)
        self.cb.setEditable(True)
        self.cb.setValidator(
            QtGui.QRegExpValidator(
                QtCore.QRegExp(r'^\d{1,2}(\.\d[05]{0,1})?$')
            )
        )
        self.cb.addItems(self.cb_values)
        self.cb.editTextChanged[str].connect(self.__set_value)
        self.cb.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.cb.setInsertPolicy(QtWidgets.QComboBox.InsertAtTop)

    def init_pb(self, on_start=True):
        if on_start:
            self.pbar.setMinimumWidth(200)
            self.pbar.setMaximumHeight(16)
            font = QtGui.QFont('Consolas', 16, 50)
            self.pbar.setFont(font)
        self.stop()
        self.pbar.reset()
        self.pbar.setRange(0, int(self.value * 60) - 1)

    def timerEvent(self, evt):
        if self.__pbar_active:
            if self.pbar.value() < self.pbar.maximum():
                self.pbar.setValue(self.pbar.value() + 1)
                minutes = str(self.pbar.value() // 60)
                seconds = str(self.pbar.value() % 60)
                seconds = seconds if len(seconds) > 1 else f'0{seconds}'
                self.pbar.setFormat(f'{minutes}:{seconds}')
            else:
                self.cb.setEnabled(True)
                self.endTask.emit()

    def event(self, evt):
        if evt.type() == QtCore.QEvent.Leave:
            self.cb.setEditText(str(self.value))
            self.add_value(self.value)
        return QtWidgets.QWidget.event(self, evt)

    def add_value(self, v):
        for i in range(self.cb.count()):
            if str(v) == self.cb.itemText(i):
                return
            if v < Decimal(self.cb.itemText(i)):
                self.cb.insertItem(i, str(v))
                return
        else:
            if v > Decimal(self.cb.itemText(self.cb.count() - 1)):
                self.cb.addItem(str(v))

    def is_active(self):
        return self.__pbar_active

    @QtCore.pyqtSlot(str)
    def __set_value(self, value):
        self.value = Decimal(value).quantize(Decimal('0.01'))

    @QtCore.pyqtSlot()
    def stop(self):
        self.cb.setEnabled(True)
        self.__pbar_active = False

    @QtCore.pyqtSlot()
    def start(self):
        self.__pbar_active = True
        self.cb.setEnabled(False)
