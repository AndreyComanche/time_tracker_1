from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import pyautogui as ag
from datetime import datetime
from time import sleep
from PIL import Image
import keyring
import json


class Login(QObject):
    login_success = pyqtSignal()
    logout_success = pyqtSignal()

    def __init__(self, application, parent=None):
        super(Login, self).__init__(parent)

        self.arpe_icon = Image.open(r".\img\arpe.png")
        self.arpe_stop = Image.open(r".\img\arpe_stop.png")
        self.arpe_off = Image.open(r".\img\arpe_off.png")
        self.arpe_start = Image.open(r".\img\arpe_start.png")

        self.yukon_icon = Image.open(r".\img\yukon_off.png")
        self.yukon_logo = Image.open(r".\img\yukon_logo.png")
        self.yukon_on = Image.open(r".\img\yukon_on.png")
        self.paste_pw = Image.open(r".\img\paste.png")
        self.login_btn = Image.open(r".\img\login_btn.png")

        self.login_sc = Image.open(r".\img\login_success.png")
        self.rh_page = Image.open(r".\img\rh_page.png")

        self.log_data = ''
        with open("./login_data.json", 'r') as file:
            self.log_data = tuple(json.loads(file.read()).values())
        self.cb = application.clipboard()

        self.conf = 0.8

    @pyqtSlot()
    def login(self):
        start = datetime.utcnow()
        print("login start:", start)
        point = ag.locateCenterOnScreen(self.arpe_icon,
                                        confidence=self.conf)
        if point is not None:
            print("open popup auto refresh plus:", datetime.utcnow() - start)
            ag.leftClick(point.x, point.y)
            sleep(1)
        point = ag.locateCenterOnScreen(self.arpe_stop,
                                        confidence=self.conf)
        if point is not None:
            print("press stop auto refresh plus:", datetime.utcnow() - start)
            ag.leftClick(point.x, point.y)
        point = ag.locateCenterOnScreen(self.yukon_icon,
                                        confidence=self.conf)
        if point is not None:
            print("open popup yukon:", datetime.utcnow() - start)
            self.login_success.emit()
            ag.leftClick(point.x, point.y)
            sleep(1)
            print("paste password yukon:", datetime.utcnow() - start)
            passwd = keyring.get_password(*self.log_data)
            self.cb.setText(passwd)
            ag.leftClick(518, 228)
            ag.hotkey('ctrl', 'shift', 'v', interval=0.25)
            self.cb.setText('')
            point = ag.locateCenterOnScreen(self.login_btn,
                                            confidence=self.conf)
            if point is not None:
                ag.leftClick(point, interval=0.25)
        print(datetime.utcnow() - start)

    @pyqtSlot()
    def logout(self):
        start = datetime.utcnow()
        print("logout start:", start)
        point = ag.locateCenterOnScreen(self.yukon_on,
                                        confidence=self.conf)
        if point is not None:
            ag.leftClick(point.x, point.y)
            sleep(1)
        print("logout yukon:", datetime.utcnow() - start)
        point = ag.locateCenterOnScreen(self.arpe_off)
        if point is not None:
            ag.leftClick(point.x, point.y)
            sleep(1)
        print("start arpe:", datetime.utcnow() - start)
        point = ag.locateCenterOnScreen(self.arpe_start)
        if point is not None:
            ag.leftClick(point.x, point.y)
            sleep(0.25)
            self.logout_success.emit()
        point = ag.locateCenterOnScreen(self.rh_page,
                                        confidence=self.conf)
        if point is not None:
            ag.leftClick(point.x, point.y)
        print("logout complete:", datetime.utcnow() - start)
