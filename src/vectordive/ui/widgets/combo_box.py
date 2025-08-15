from PyQt5.QtWidgets import QComboBox
from vectordive.config.base import MODE_COMBO

class MakeComboBox:
    def __init__(self):
        mode = MODE_COMBO
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(mode)
        
    def get_widget(self, label):
        return (label, self.mode_combo)