from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtMultimedia import QSoundEffect


class TextToSpeech(QObject):
    def __init__(self):
        super(TextToSpeech, self).__init__()

        url = QUrl.fromLocalFile(r"./sound/message.wav")
        self.player = QSoundEffect()
        self.player.setSource(url)

    def say(self):
        self.player.play()
