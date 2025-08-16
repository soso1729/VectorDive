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
        
        # デフォルトの接続情報を初期化
        self.connection_info = {
            'ip': self.ip_info[1],  # デフォルトIP
            'port': self.port_info[1],  # デフォルトポート
            'mode': 'UDP'  # デフォルトモード
        }
       

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

            # デバッグ用ボタン（隠しボタン）
            self.debug_btn = GetPushButton("Debug Mode")
            self.debug_btn.get_widget().setStyleSheet("""
                QPushButton {
                    background-color: #666666;
                    color: #cccccc;
                    border: 1px solid #888888;
                    border-radius: 3px;
                    padding: 5px 10px;
                    font-size: 10px;
                }
                QPushButton:hover {
                    background-color: #888888;
                }
            """)
            btn_layout.addWidget(self.debug_btn.get_widget())
            
            self.connect_btn = GetPushButton("Connect")
            btn_layout.addWidget(self.connect_btn.get_widget())
            
            self.cancel_btn = GetPushButton("Cancel")
            btn_layout.addWidget(self.cancel_btn.get_widget())

            self.debug_btn.get_widget().clicked.connect(self.debug_btn_clicked)
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
        # フォームの値を取得（安全な方法）
        try:
            ip = self.ip_edit.edit.text().strip()
            port = self.port_edit.edit.text().strip()
            mode = self.mode_combo.mode_combo.currentText()
            
            # 空の値チェック
            if not ip or not port:
                self.update_status("IP address and port are required", "red")
                return
                
        except AttributeError as e:
            self.update_status(f"Form field error: {str(e)}", "red")
            return
        
        # 入力値の検証
        if not re.match(r"^\d{1,3}(?:\.\d{1,3}){3}$", ip):
            self.update_status("Invalid IP address format", "red")
            return
        if not port.isdigit() or int(port) < 1 or int(port) > 65535:
            self.update_status("Invalid port number (1-65535)", "red")
            return
            
        # 接続開始のログを追加
        self.add_log(f"Attempting to connect to {ip}:{port} ({mode})")
        
        # フォームをそれぞれ非アクティブにする
        self.ip_edit.edit.setEnabled(False)
        self.port_edit.edit.setEnabled(False)
        self.mode_combo.mode_combo.setEnabled(False)
        # ボタンを非アクティブにする
        self.connect_btn.get_widget().setEnabled(False)
        self.cancel_btn.get_widget().setEnabled(True)

        try:
            hb_wait = HbWait(ip, port)
            if hb_wait.get_success() is True:
                self.update_status("Connection successful", "green")
                QApplication.processEvents()
                
                # 接続情報を保存（文字列として保存）
                self.connection_info = {
                    'ip': ip,
                    'port': port,
                    'mode': mode
                }
                
                # 接続情報をログに出力
                self.add_log(f"Connection info saved: {self.connection_info}")
                
                # メインウィンドウに遷移
                QTimer.singleShot(1000, self.transition_to_main_window)
                return True
            else:
                self.update_status("Connection failed - no heartbeat received", "red")
                self.enable_form()
        except Exception as e:
            self.update_status(f"Connection error: {str(e)}", "red")
            self.enable_form()
            
    def debug_btn_clicked(self):
        """デバッグボタンのクリック処理"""
        self.add_log("Debug mode activated - bypassing connection check")
        
        # デバッグ用の接続情報を作成
        self.connection_info = {
            'ip': '127.0.0.1',
            'port': '14550',
            'mode': 'UDP',
            'debug': True
        }
        
        self.add_log(f"Debug connection info: {self.connection_info}")
        
        # メインウィンドウに遷移（デバッグモード）
        QTimer.singleShot(500, self.transition_to_main_window_debug)
            
    def enable_form(self):
        """フォームを再度有効にする"""
        self.connect_btn.get_widget().setEnabled(True)
        self.cancel_btn.get_widget().setEnabled(True)
        self.ip_edit.edit.setEnabled(True)
        self.port_edit.edit.setEnabled(True)
        self.mode_combo.mode_combo.setEnabled(True)
        
    def transition_to_main_window(self):
        """メインウィンドウに遷移する"""
        # 接続情報の確認
        if not hasattr(self, 'connection_info') or not self.connection_info:
            self.add_log("Error: No connection info available")
            return
            
        self.add_log(f"Transitioning to main window with connection info: {self.connection_info}")
        
        # メインウィンドウを作成して表示（接続情報を渡す）
        self.main_window = MainWindow(self.connection_info)
        self.main_window.show()
        
        # エントランスウィンドウを閉じる
        self.close()
        
    def transition_to_main_window_debug(self):
        """デバッグモードでメインウィンドウに遷移する"""
        self.add_log("Transitioning to main window in DEBUG mode")
        
        # メインウィンドウを作成して表示（デバッグモード）
        self.main_window = MainWindow(self.connection_info)
        
        # デバッグモードを有効化
        self.main_window.debug_mode = True
        self.main_window.setWindowTitle(self.main_window.windowTitle() + " [DEBUG MODE]")
        
        self.main_window.show()
        
        # エントランスウィンドウを閉じる
        self.close()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EntranceWindow()
    window.show()
    sys.exit(app.exec_())
