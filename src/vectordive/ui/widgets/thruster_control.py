from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

class ThrusterControl(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # タイトル
        title_label = QLabel("Thruster Control")
        title_label.setStyleSheet("font-weight: bold; color: white; font-size: 14px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # スラスター1
        self.create_thruster_control(layout, "Thruster 1", 1)
        
        # スラスター2
        self.create_thruster_control(layout, "Thruster 2", 2)
        
        # スラスター3
        self.create_thruster_control(layout, "Thruster 3", 3)
        
        # スラスター4
        self.create_thruster_control(layout, "Thruster 4", 4)
        
        # スラスター5
        self.create_thruster_control(layout, "Thruster 5", 5)
        
        # スラスター6
        self.create_thruster_control(layout, "Thruster 6", 6)
        
        # 緊急停止ボタン
        emergency_btn = QPushButton("EMERGENCY STOP")
        emergency_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                font-weight: bold;
                border: 2px solid #cc0000;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QPushButton:pressed {
                background-color: #aa0000;
            }
        """)
        emergency_btn.clicked.connect(self.emergency_stop)
        layout.addWidget(emergency_btn)
        
    def create_thruster_control(self, parent_layout, name, thruster_id):
        """個別のスラスター制御を作成"""
        # スラスター名
        name_label = QLabel(name)
        name_label.setStyleSheet("color: white; font-weight: bold;")
        parent_layout.addWidget(name_label)
        
        # スライダーとラベルのレイアウト
        slider_layout = QHBoxLayout()
        
        # 値表示ラベル
        value_label = QLabel("0%")
        value_label.setStyleSheet("color: white; min-width: 40px;")
        value_label.setAlignment(Qt.AlignCenter)
        slider_layout.addWidget(value_label)
        
        # スライダー
        slider = QSlider(Qt.Horizontal)
        slider.setRange(-100, 100)
        slider.setValue(0)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 8px;
                background: #2b2b2b;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                border: 1px solid #45a049;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #45a049;
            }
        """)
        
        # スライダーの値変更をラベルに反映
        slider.valueChanged.connect(lambda value: value_label.setText(f"{value}%"))
        slider.valueChanged.connect(lambda value: self.thruster_value_changed(thruster_id, value))
        
        slider_layout.addWidget(slider)
        
        # 中央位置ボタン
        center_btn = QPushButton("0")
        center_btn.setStyleSheet("""
            QPushButton {
                background-color: #555555;
                color: white;
                border: 1px solid #777777;
                border-radius: 3px;
                padding: 5px;
                min-width: 30px;
            }
            QPushButton:hover {
                background-color: #777777;
            }
        """)
        center_btn.clicked.connect(lambda: slider.setValue(0))
        slider_layout.addWidget(center_btn)
        
        parent_layout.addLayout(slider_layout)
        
        # スラスターIDとスライダーを保存
        setattr(self, f"slider_{thruster_id}", slider)
        setattr(self, f"value_label_{thruster_id}", value_label)
        
    def thruster_value_changed(self, thruster_id, value):
        """スラスター値が変更された時の処理"""
        # ここで実際のスラスター制御処理を実装
        
    def emergency_stop(self):
        """緊急停止処理"""
        # 全てのスラスターを0に設定
        for i in range(1, 7):  # 6つのスラスター
            slider = getattr(self, f"slider_{i}", None)
            if slider:
                slider.setValue(0)
        
    def get_widget(self):
        """ウィジェットを返す"""
        return self
