from vectordive.connections.telemetry import GetTelemetry
import numpy as np
import time

# 速度を加速度積分で計算する
# 位置を速度積分で計算する

class GetVelocityData:
    def __init__(self, connection_info, velocity_data=None, position_data=None):
        self.telemetry = GetTelemetry(connection_info)
        self.velocity_data = velocity_data if velocity_data is not None else np.zeros(3)  # [x, y, z]
        self.position_data = position_data if position_data is not None else np.zeros(3)  # [x, y, z]
        
        # データ蓄積用のキュー
        self.velocity_data_queue = []
        self.position_data_queue = []
        self.velocity_data_queue_time = []
        self.position_data_queue_time = []
        
        # 前回のデータ
        self.last_acc_data = None
        self.last_time = None
        
        # 積分用の累積値
        self.velocity_integral = np.zeros(3)  # 速度の積分値
        self.position_integral = np.zeros(3)  # 位置の積分値

    def update_position_from_acc(self):
        """IMUの加速度データを使って二重積分で位置を推定"""
        try:
            # 現在の加速度データと時間を取得
            acc_data_tuple = self.telemetry.get_imu_output_acc_data()
            current_time = time.time()
            
            # タプルをnumpy配列に変換
            if acc_data_tuple is not None:
                current_acc_data = np.array(acc_data_tuple)
            else:
                current_acc_data = self.generate_mock_acc_data(current_time)
            
            # 初回実行時は初期化
            if self.last_acc_data is None:
                self.last_acc_data = current_acc_data
                self.last_time = current_time
                return self.position_data_queue, self.position_data_queue_time
            
            # 時間差分を計算
            delta_time = current_time - self.last_time
            
            if delta_time <= 0:
                return self.position_data_queue, self.position_data_queue_time
            
            # 加速度の平均値を計算（台形積分）
            avg_acc = (current_acc_data + self.last_acc_data) / 2.0
            
            # 速度を積分で更新（v = v0 + a*dt）
            self.velocity_integral += avg_acc * delta_time
            
            # 位置を積分で更新（p = p0 + v*dt）
            # 速度の平均値を使用（台形積分）
            avg_velocity = (self.velocity_integral + self.velocity_data) / 2.0
            self.position_integral += avg_velocity * delta_time
            
            # 現在の値を更新
            self.velocity_data = self.velocity_integral.copy()
            self.position_data = self.position_integral.copy()
            
            # データをキューに追加
            self.velocity_data_queue.append(self.velocity_data.copy())
            self.position_data_queue.append(self.position_data.copy())
            self.velocity_data_queue_time.append(current_time)
            self.position_data_queue_time.append(current_time)
            
            # キューサイズを制限（最新100個のデータを保持）
            max_queue_size = 100
            if len(self.velocity_data_queue) > max_queue_size:
                self.velocity_data_queue.pop(0)
                self.position_data_queue.pop(0)
                self.velocity_data_queue_time.pop(0)
                self.position_data_queue_time.pop(0)
            
            # 前回のデータを更新
            self.last_acc_data = current_acc_data.copy()
            self.last_time = current_time
            
            return self.position_data_queue, self.position_data_queue_time
            
        except Exception as e:
            print(f"Error in update_position_from_acc: {e}")
            return self.position_data_queue, self.position_data_queue_time
            
    def generate_mock_acc_data(self, current_time):
        """テスト用のモック加速度データを生成（MAVLinkデータが取得できない場合のみ使用）"""
        import math
        
        # 時間に基づいて変化する加速度データを生成
        # 正弦波とコサイン波の組み合わせで複雑な動きをシミュレート
        acc_x = 0.5 * math.sin(current_time * 0.5) + 0.2 * math.cos(current_time * 0.3)
        acc_y = 0.3 * math.sin(current_time * 0.4) + 0.1 * math.cos(current_time * 0.6)
        acc_z = 0.1 * math.sin(current_time * 0.2) + 0.05 * math.cos(current_time * 0.8)
        
        return np.array([acc_x, acc_y, acc_z])

    def get_position_data(self):
        """位置データを取得（リアルタイム更新付き）"""
        return self.update_position_from_acc()

    def get_velocity_data(self):
        """速度データを取得"""
        return self.velocity_data_queue, self.velocity_data_queue_time

    def reset_integration(self):
        """積分値をリセット"""
        self.velocity_integral = np.zeros(3)
        self.position_integral = np.zeros(3)
        self.velocity_data = np.zeros(3)
        self.position_data = np.zeros(3)
        self.velocity_data_queue.clear()
        self.position_data_queue.clear()
        self.velocity_data_queue_time.clear()
        self.position_data_queue_time.clear()
        self.last_acc_data = None
        self.last_time = None

    def get_current_position(self):
        """現在の位置を取得"""
        return self.position_data

    def get_current_velocity(self):
        """現在の速度を取得"""
        return self.velocity_data

        
        
        
        
        
