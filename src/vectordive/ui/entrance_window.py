from os import wait
from PyQt5.QtWidgets import QFormLayout, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QGroupBox, QLineEdit, QLabel, QMessageBox, QTextEdit
from PyQt5.QtCore import QTime, Qt, QTimer
from vectordive.ui.widgets.line_edit import MakeEdit
from vectordive.ui.widgets.combo_box import MakeComboBox
from vectordive.ui.widgets.push_box import GetPushButton
from vectordive.connections.hb_wait import HbWait
from vectordive.ui.main_window import MainWindow
from vectordive.config.base import (
    IP_EDIT_INFO, PORT_EDIT_INFO, MODE_COMBO_LABEL
    )

import sys
import re

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

            self.mode_combo = MakeComboBox()
            form_layout.addRow(*self.mode_combo.get_widget(MODE_COMBO_LABEL))

            self.ip_edit = MakeEdit(self.ip_info[1], self)
            widget = self.ip_edit.get_widget(self.ip_info[0])
            form_layout.addRow(*widget)

            self.port_edit = MakeEdit(self.port_info[1], self)
            widget = self.port_edit.get_widget(self.port_info[0])
            form_layout.addRow(*widget)
            
            return form_layout
        
        def get_btn():
            btn_layout = QHBoxLayout()
            btn_layout.addStretch()

            self.connect_btn = GetPushButton("Connect")
            btn_layout.addWidget(self.connect_btn.get_widget())
            
            self.cancel_btn = GetPushButton("Cancel")
            btn_layout.addWidget(self.cancel_btn.get_widget())

            self.connect_btn.get_widget().clicked.connect(self.connect_btn_clicked)
            self.cancel_btn.get_widget().clicked.connect(self.close)


            return btn_layout

        def get_group_box():
            group_box = QGroupBox("Connection Settings", self)
            group_box.setStyleSheet("QGroupBox { color: white; }")
            group_box.setLayout(get_form())

            return group_box

        def get_status():
            # Status用のグループボックスを作成
            status_group_box = QGroupBox("Status", self)
            status_group_box.setStyleSheet("QGroupBox { color: white; }")
            
            # ステータスレイアウトを作成
            status_layout = QVBoxLayout()
            
            # ログを表示するテキストエリア
            self.log_text = QTextEdit(self)
            self.log_text.setMaximumHeight(100)
            self.log_text.setStyleSheet("QTextEdit { background-color: #1e1e1e; color: #cccccc; border: 1px solid #555555; }")
            self.log_text.setReadOnly(True)
            self.log_text.append("System initialized...")
            status_layout.addWidget(self.log_text)
            
            status_group_box.setLayout(status_layout)
            return status_group_box

        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(get_group_box())
        main_layout.addLayout(get_btn())
        main_layout.addWidget(get_status())
        
    def add_log(self, message):
        """ログメッセージを追加する"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
    def update_status(self, status, color="orange"):
        self.add_log(status)

    def connect_btn_clicked(self):
        # フォームの値を取得
        ip = self.ip_edit.edit.text().strip()
        port = self.port_edit.edit.text().strip()
        if not re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", ip) or not port.isdigit():
            self.update_status("Invalid IP or Port", "red")
            return
        # 接続開始のログを追加
        self.add_log(f"Attempting to connect to {ip}:{port}")
        
        #フォームをそれぞれ非アクティブにする
        self.ip_edit.edit.setEnabled(False)
        self.port_edit.edit.setEnabled(False)
        self.mode_combo.mode_combo.setEnabled(False)
        #ボタンを非アクティブにする
        self.connect_btn.get_widget().setEnabled(False)
        self.cancel_btn.get_widget().setEnabled(False)

        hb_wait = HbWait(ip, port)
        if hb_wait.get_success() is True:
            self.update_status("Connection successful", "green")
            QApplication.processEvents()
            
            # 接続情報を保存
            self.connection_info = {
                'ip': ip,
                'port': port,
                'mode': self.mode_combo.mode_combo.currentText()
            }
            
            # メインウィンドウに遷移
            QTimer.singleShot(1000, self.transition_to_main_window)
            return True

        else:
            self.update_status("Connection failed", "red")
            self.connect_btn.get_widget().setEnabled(True)
            self.cancel_btn.get_widget().setEnabled(True)
            self.ip_edit.edit.setEnabled(True)
            self.port_edit.edit.setEnabled(True)
            self.mode_combo.mode_combo.setEnabled(True)
        
    def transition_to_main_window(self):
        """メインウィンドウに遷移する"""
        # メインウィンドウを作成して表示（接続情報を渡す）
        self.main_window = MainWindow(self.connection_info)
        self.main_window.show()
        
        # エントランスウィンドウを閉じる
        self.close()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EntranceWindow()
    window.show()
    sys.exit(app.exec_())
