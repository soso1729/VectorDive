from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QGroupBox, QProgressBar, QFrame)
from PyQt5.QtGui import QFont, QPalette, QColor
import numpy as np

class PositionEstimationWidget(QWidget):
    """位置推定データを表示するウィジェット"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """UIを初期化"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # タイトル
        title = QLabel("位置推定 (Position Estimation)")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ffffff; margin: 5px;")
        layout.addWidget(title)
        
        # 位置情報グループ
        self.position_group = self.create_position_group()
        layout.addWidget(self.position_group)
        
        # 速度情報グループ
        self.velocity_group = self.create_velocity_group()
        layout.addWidget(self.velocity_group)
        
        # 状態表示
        self.status_label = QLabel("状態: 待機中")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #888888; font-size: 10px; margin: 5px;")
        layout.addWidget(self.status_label)
        
        # スタイル設定
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #1e1e1e;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 3px;
                text-align: center;
                background-color: #2b2b2b;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 1px;
            }
        """)
        
    def create_position_group(self):
        """位置情報グループを作成"""
        group = QGroupBox("位置 (Position)")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # X軸位置
        x_layout = QHBoxLayout()
        x_label = QLabel("X:")
        x_label.setFixedWidth(20)
        self.x_position_label = QLabel("0.000 m")
        self.x_position_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        x_layout.addWidget(x_label)
        x_layout.addWidget(self.x_position_label)
        x_layout.addStretch()
        layout.addLayout(x_layout)
        
        # Y軸位置
        y_layout = QHBoxLayout()
        y_label = QLabel("Y:")
        y_label.setFixedWidth(20)
        self.y_position_label = QLabel("0.000 m")
        self.y_position_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        y_layout.addWidget(y_label)
        y_layout.addWidget(self.y_position_label)
        y_layout.addStretch()
        layout.addLayout(y_layout)
        
        # Z軸位置
        z_layout = QHBoxLayout()
        z_label = QLabel("Z:")
        z_label.setFixedWidth(20)
        self.z_position_label = QLabel("0.000 m")
        self.z_position_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        z_layout.addWidget(z_label)
        z_layout.addWidget(self.z_position_label)
        z_layout.addStretch()
        layout.addLayout(z_layout)
        
        # 位置の大きさ（距離）
        magnitude_layout = QHBoxLayout()
        magnitude_label = QLabel("距離:")
        magnitude_label.setFixedWidth(30)
        self.magnitude_label = QLabel("0.000 m")
        self.magnitude_label.setStyleSheet("color: #E91E63; font-weight: bold;")
        magnitude_layout.addWidget(magnitude_label)
        magnitude_layout.addWidget(self.magnitude_label)
        magnitude_layout.addStretch()
        layout.addLayout(magnitude_layout)
        
        return group
        
    def create_velocity_group(self):
        """速度情報グループを作成"""
        group = QGroupBox("速度 (Velocity)")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # X軸速度
        x_layout = QHBoxLayout()
        x_label = QLabel("VX:")
        x_label.setFixedWidth(25)
        self.x_velocity_label = QLabel("0.000 m/s")
        self.x_velocity_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        x_layout.addWidget(x_label)
        x_layout.addWidget(self.x_velocity_label)
        x_layout.addStretch()
        layout.addLayout(x_layout)
        
        # Y軸速度
        y_layout = QHBoxLayout()
        y_label = QLabel("VY:")
        y_label.setFixedWidth(25)
        self.y_velocity_label = QLabel("0.000 m/s")
        self.y_velocity_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        y_layout.addWidget(y_label)
        y_layout.addWidget(self.y_velocity_label)
        y_layout.addStretch()
        layout.addLayout(y_layout)
        
        # Z軸速度
        z_layout = QHBoxLayout()
        z_label = QLabel("VZ:")
        z_label.setFixedWidth(25)
        self.z_velocity_label = QLabel("0.000 m/s")
        self.z_velocity_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        z_layout.addWidget(z_label)
        z_layout.addWidget(self.z_velocity_label)
        z_layout.addStretch()
        layout.addLayout(z_layout)
        
        # 速度の大きさ
        speed_layout = QHBoxLayout()
        speed_label = QLabel("速度:")
        speed_label.setFixedWidth(35)
        self.speed_label = QLabel("0.000 m/s")
        self.speed_label.setStyleSheet("color: #E91E63; font-weight: bold;")
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_label)
        speed_layout.addStretch()
        layout.addLayout(speed_layout)
        
        return group
        
    def update_position(self, position):
        """位置データを更新"""
        if position is None or len(position) < 3:
            return
            
        x, y, z = position[0], position[1], position[2]
        
        # 位置ラベルを更新
        self.x_position_label.setText(f"{x:.3f} m")
        self.y_position_label.setText(f"{y:.3f} m")
        self.z_position_label.setText(f"{z:.3f} m")
        
        # 距離を計算
        magnitude = np.sqrt(x**2 + y**2 + z**2)
        self.magnitude_label.setText(f"{magnitude:.3f} m")
        
    def update_velocity(self, velocity):
        """速度データを更新"""
        if velocity is None or len(velocity) < 3:
            return
            
        vx, vy, vz = velocity[0], velocity[1], velocity[2]
        
        # 速度ラベルを更新
        self.x_velocity_label.setText(f"{vx:.3f} m/s")
        self.y_velocity_label.setText(f"{vy:.3f} m/s")
        self.z_velocity_label.setText(f"{vz:.3f} m/s")
        
        # 速度の大きさを計算
        speed = np.sqrt(vx**2 + vy**2 + vz**2)
        self.speed_label.setText(f"{speed:.3f} m/s")
        
    def update_status(self, status, color="#888888"):
        """状態を更新"""
        self.status_label.setText(f"状態: {status}")
        self.status_label.setStyleSheet(f"color: {color}; font-size: 10px; margin: 5px;")
        
    def reset(self):
        """データをリセット"""
        self.x_position_label.setText("0.000 m")
        self.y_position_label.setText("0.000 m")
        self.z_position_label.setText("0.000 m")
        self.magnitude_label.setText("0.000 m")
        
        self.x_velocity_label.setText("0.000 m/s")
        self.y_velocity_label.setText("0.000 m/s")
        self.z_velocity_label.setText("0.000 m/s")
        self.speed_label.setText("0.000 m/s")
        
        self.update_status("リセット済み", "#FF9800")

class PositionEstimationManager:
    """位置推定の管理クラス"""
    
    def __init__(self, connection_info=None, main_window=None):
        self.connection_info = connection_info
        self.main_window = main_window
        self.velocity_calculator = None
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_position_estimation)
        
        # 位置推定ウィジェットを初期化
        self.position_widget = PositionEstimationWidget()
        
        # 接続情報がある場合は位置推定を開始
        if connection_info:
            self.start_position_estimation()
            
    def start_position_estimation(self):
        """位置推定を開始"""
        try:
            from vectordive.workers.telemetry import GetVelocityData
            self.velocity_calculator = GetVelocityData(self.connection_info)
            self.update_timer.start(100)  # 100ms間隔で更新
            self.position_widget.update_status("位置推定実行中", "#4CAF50")
        except Exception as e:
            self.position_widget.update_status(f"エラー: {str(e)}", "#F44336")
            
    def stop_position_estimation(self):
        """位置推定を停止"""
        self.update_timer.stop()
        self.position_widget.update_status("停止中", "#888888")
        
    def update_position_estimation(self):
        """位置推定データを更新"""
        try:
            if self.velocity_calculator:
                # 位置データを取得
                position_queue, time_queue = self.velocity_calculator.get_position_data()
                
                if position_queue and len(position_queue) > 0:
                    # 最新の位置と速度を取得
                    current_position = self.velocity_calculator.get_current_position()
                    current_velocity = self.velocity_calculator.get_current_velocity()
                    
                    # UIを更新
                    self.position_widget.update_position(current_position)
                    self.position_widget.update_velocity(current_velocity)
                    
                    # マップ表示も更新
                    if self.main_window and hasattr(self.main_window, 'update_map_position'):
                        self.main_window.update_map_position(current_position)
                    
                    # MAVLink接続状態を確認
                    if hasattr(self.velocity_calculator, 'telemetry'):
                        if self.velocity_calculator.telemetry.is_connected():
                            self.position_widget.update_status("MAVLink接続済み - 位置推定実行中", "#4CAF50")
                        else:
                            self.position_widget.update_status("MAVLink未接続 - モックデータ使用中", "#FF9800")
                    else:
                        self.position_widget.update_status("位置推定実行中", "#4CAF50")
                else:
                    self.position_widget.update_status("データなし", "#FF9800")
                    
        except Exception as e:
            self.position_widget.update_status(f"更新エラー: {str(e)}", "#F44336")
            
    def reset_position_estimation(self):
        """位置推定をリセット"""
        if self.velocity_calculator:
            self.velocity_calculator.reset_integration()
            self.position_widget.reset()
            self.position_widget.update_status("リセット済み", "#FF9800")
            
    def get_widget(self):
        """ウィジェットを取得"""
        return self.position_widget
