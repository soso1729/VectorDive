from PyQt5.QtWidgets import QPushButton

class GetPushButton:
    def __init__(self, label):
        self.button = QPushButton(label)

    def get_widget(self):
        return self.button


