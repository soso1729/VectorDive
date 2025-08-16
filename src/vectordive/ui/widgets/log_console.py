from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtCore import Qt

class LogConsole(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # ログ表示用テキストエリア（高さ制限付き）
        self.log_text = QTextEdit()
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #555555;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(60)  # 高さをさらに制限
        layout.addWidget(self.log_text)
        
        # 初期メッセージを追加
        self.add_log("Log console initialized")
        
    def add_log(self, message):
        """ログメッセージを追加する"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
        # スクロールを最下部に移動
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def clear_log(self):
        """ログをクリアする"""
        self.log_text.clear()
        
    def get_widget(self):
        """ウィジェットを返す"""
        return self
