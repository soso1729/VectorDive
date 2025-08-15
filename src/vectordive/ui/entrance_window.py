from ast import main
from tokenize import group
from PyQt5.QtWidgets import QFormLayout, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit
from vectordive.ui.widgets.line_edit import MakeEdit
from vectordive.ui.widgets.combo_box import MakeComboBox
from vectordive.ui.widgets.push_box import GetPushButton
from vectordive.config.base import (
    IP_EDIT_INFO, PORT_EDIT_INFO, MODE_COMBO_LABEL
    )
import sys

class EntranceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent) 
        self.setWindowTitle("VectorDive_Entrance")
        self.setStyleSheet("background-color: #2b2b2b; color: white;")
        self.init_ui()
        
    def init_ui(self):
        self.ip_info = IP_EDIT_INFO
        self.port_info = PORT_EDIT_INFO
       

        def get_form():
            form_layout = QFormLayout()

            combo = MakeComboBox()
            form_layout.addRow(*combo.get_widget(MODE_COMBO_LABEL))

            edit = MakeEdit(self.ip_info[1], self)
            widget = edit.get_widget(self.ip_info[0])
            form_layout.addRow(*widget)

            edit = MakeEdit(self.port_info[1], self)
            widget = edit.get_widget(self.port_info[0])
            form_layout.addRow(*widget)
            
            return form_layout
        
        def get_btn():
            btn_layout = QHBoxLayout()
            btn_layout.addStretch()

            btn = GetPushButton("Connect")
            btn_layout.addWidget(btn.get_widget())
            
            btn = GetPushButton("Cancel")
            btn_layout.addWidget(btn.get_widget())

            return btn_layout
        
        
        def get_group_box():
            group_box = QGroupBox("Connection Settings", self)
            group_box.setStyleSheet("QGroupBox { color: white; }")
            group_box.setLayout(get_form())

            return group_box

        def get_status():
            status_label = QLabel("Status: Disconnected", self)
            status_label.setStyleSheet("color: orange;")
            status_label.setAlignment(Qt.AlignCenter)
            return status_label

        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(get_group_box())
        main_layout.addLayout(get_btn())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EntranceWindow()
    window.show()
    sys.exit(app.exec_())
