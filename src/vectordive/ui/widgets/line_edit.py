from PyQt5.QtWidgets import QLineEdit


class MakeEdit:
    def __init__(self, default_value = "", parent=None):
        self.edit = QLineEdit(default_value, parent)
        
    
    def get_widget(self, label):
        return (label, self.edit) 
    