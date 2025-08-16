from PyQt5.QtWidgets import QProgressBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from vectordive.config import base

class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # レイアウトの設定
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # タイトルラベル
        title_label = QLabel("Thruster Output Telemetry")
        title_label.setStyleSheet("font-weight: bold; color: white; font-size: 14px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 6つのスラスター用の縦並びレイアウト
        thruster_layout = QVBoxLayout()
        
        # プログレスバーの初期化
        maximum = base.THRUSTER_MAXIMUM
        minimum = base.THRUSTER_MINIMUM
        default = base.THRUSTER_DEFAULT
        
        # 6つのスラスター用プログレスバーを作成
        self.progress_bars = []
        self.thruster_labels = []
        
        for i in range(6):
            # スラスター番号
            thruster_num = i + 1
            
            # 個別のスラスター用レイアウト
            thruster_item_layout = QVBoxLayout()
            
            # スラスター名ラベル
            thruster_label = QLabel(f"T{thruster_num}")
            thruster_label.setStyleSheet("color: white; font-weight: bold; font-size: 10px;")
            thruster_label.setAlignment(Qt.AlignCenter)
            
            # プログレスバー
            progress_bar = QProgressBar()
            progress_bar.setMinimum(minimum)
            progress_bar.setMaximum(maximum)
            progress_bar.setValue(default)
            progress_bar.setTextVisible(True)
            progress_bar.setFormat("%v")
            
            # マウス操作を無効にする
            progress_bar.setEnabled(False)
            
            # プログレスバーのスタイル設定（細く）
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #555555;
                    border-radius: 3px;
                    text-align: center;
                    background-color: #2b2b2b;
                    color: white;
                    min-height: 15px;
                    max-height: 15px;
                    font-size: 9px;
                }
                QProgressBar::chunk {
                    background-color: #4CAF50;
                    border-radius: 2px;
                }
                QProgressBar:disabled {
                    color: #cccccc;
                }
            """)
            
            # 値を表示するラベル
            value_label = QLabel(f"{default}")
            value_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 9px;")
            value_label.setAlignment(Qt.AlignCenter)
            
            # レイアウトに追加
            thruster_item_layout.addWidget(thruster_label)
            thruster_item_layout.addWidget(progress_bar)
            thruster_item_layout.addWidget(value_label)
            
            # メインレイアウトに追加
            thruster_layout.addLayout(thruster_item_layout)
            
            # リストに保存
            self.progress_bars.append(progress_bar)
            self.thruster_labels.append(value_label)
        
        layout.addLayout(thruster_layout)
        
        # テレメトリ状態表示用ラベル
        self.telemetry_label = QLabel("Telemetry: Waiting for data...")
        self.telemetry_label.setStyleSheet("color: #888888; font-size: 10px;")
        self.telemetry_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.telemetry_label)

    def get_widget(self):
        # 自分自身（QWidget）を返す
        return self

    def set_value(self, thruster_index, value):
        """特定のスラスターの値を設定する"""
        if 0 <= thruster_index < len(self.progress_bars):
            self.progress_bars[thruster_index].setValue(value)
            self.thruster_labels[thruster_index].setText(f"{value}")

    def get_value(self, thruster_index=0):
        """特定のスラスターの値を取得する"""
        if 0 <= thruster_index < len(self.progress_bars):
            return self.progress_bars[thruster_index].value()
        return 0
        
    def update_from_telemetry(self, telemetry_data):
        """テレメトリデータから値を更新する"""
        if telemetry_data:
            # テレメトリデータからスラスター値を取得
            for i in range(6):
                servo_attr = f'servo{i+1}_raw'
                if hasattr(telemetry_data, servo_attr):
                    value = getattr(telemetry_data, servo_attr)
                    self.set_value(i, value)
            self.telemetry_label.setText("Telemetry: Data received")
        else:
            self.telemetry_label.setText("Telemetry: No connection")
            
    def update_from_servo_data(self, servo1_raw, servo2_raw, servo3_raw, servo4_raw, servo5_raw, servo6_raw):
        """6つのスラスター値から更新する"""
        try:
            servo_values = [servo1_raw, servo2_raw, servo3_raw, servo4_raw, servo5_raw, servo6_raw]
            
            for i, value in enumerate(servo_values):
                if value is not None:
                    self.set_value(i, value)
                else:
                    # Noneの場合は0に設定
                    self.set_value(i, 0)
            
            # テレメトリ状態を更新
            if any(v is not None and v != 0 for v in servo_values):
                self.telemetry_label.setText(f"Telemetry: T1={servo1_raw}, T2={servo2_raw}, T3={servo3_raw}, T4={servo4_raw}, T5={servo5_raw}, T6={servo6_raw}")
            else:
                self.telemetry_label.setText("Telemetry: All thrusters at 0")
        except Exception as e:
            self.telemetry_label.setText(f"Telemetry Error: {str(e)}")