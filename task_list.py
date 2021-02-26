from PyQt5 import QtGui, QtWidgets


class TaskList(QtWidgets.QGroupBox):
    def __init__(self, title, model, parent=None):
        super().__init__(parent)
        self.setTitle(title)
        self.setMinimumWidth(640)
        self.setMaximumHeight(200)
        self.task_list = QtWidgets.QTreeView(self)
        self.task_list.setModel(model)
        font = QtGui.QFont('Consolas', 16, 50)
        self.setFont(font)
        self.init_ui()

    def init_ui(self, on_start=True):
        if on_start:
            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(self.task_list)
            self.setLayout(vbox)
            self.task_list.setIndentation(25)
            self.task_list.setHeaderHidden(True)
        self.task_list.setExpanded(
            self.task_list.model().index(0, 0),
            True
        )
