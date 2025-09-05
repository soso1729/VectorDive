from pymavlink import mavutil

class GetTelemetry:
    def __init__(self, connection_info):
        self.connection_info = connection_info
        self.connection = None
        self.servo_output_raw_msg = None
        self.imu_output_raw_msg = None
        self.connection_established = False
        
        # 接続文字列を正しく構築
        if connection_info.get('mode') == 'UDP':
            connection_string = f"udpin:{connection_info['ip']}:{connection_info['port']}"
        else:
            connection_string = f"udpin:{connection_info['ip']}:{connection_info['port']}"
        
        try:
            print(f"MAVLink接続を試行中: {connection_string}")
            self.connection = mavutil.mavlink_connection(connection_string)
            self.connection.wait_heartbeat(timeout=5.0)
            print("MAVLink接続が確立されました")
            
            # 初期データを取得
            self.servo_output_raw_msg = self.connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=False, timeout=1.0)
            self.imu_output_raw_msg = self.connection.recv_match(type='RAW_IMU', blocking=False, timeout=1.0)
            
            self.connection_established = True
            print("MAVLinkデータ取得を開始しました")
            
        except Exception as e:
            print(f"MAVLink接続エラー: {e}")
            self.connection = None
            self.servo_output_raw_msg = None
            self.imu_output_raw_msg = None
            self.connection_established = False

    def get_servo_output_raw(self):
        if self.servo_output_raw_msg:
            return self.servo_output_raw_msg
        return None
    
    def get_servo_output_raw_data(self):
        # 実際のMAVLinkデータを取得しようとする
        try:
            if self.connection:
                # 最新のサーボデータを取得
                self.servo_output_raw_msg = self.connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=False, timeout=0.1)
                if self.servo_output_raw_msg:
                    return (
                        getattr(self.servo_output_raw_msg, 'servo1_raw', 0), 
                        getattr(self.servo_output_raw_msg, 'servo2_raw', 0), 
                        getattr(self.servo_output_raw_msg, 'servo3_raw', 0), 
                        getattr(self.servo_output_raw_msg, 'servo4_raw', 0), 
                        getattr(self.servo_output_raw_msg, 'servo5_raw', 0), 
                        getattr(self.servo_output_raw_msg, 'servo6_raw', 0)
                    )
        except Exception as e:
            print(f"MAVLink servo data error: {e}")
        
        # データが取得できない場合はデフォルト値を返す
        return (0, 0, 0, 0, 0, 0)
    
    def get_imu_output_acc_data(self):
        if self.imu_output_raw_msg:
            # MAVLinkのRAW_IMUデータは通常ミリG単位なので、m/s²に変換
            # 1 G = 9.81 m/s², 1 milliG = 0.00981 m/s²
            acc_x = self.imu_output_raw_msg.xacc * 0.00981
            acc_y = self.imu_output_raw_msg.yacc * 0.00981
            acc_z = self.imu_output_raw_msg.zacc * 0.00981
            return acc_x, acc_y, acc_z
        else:
            # 実際のMAVLinkデータを取得しようとする
            try:
                if self.connection:
                    # 最新のIMUデータを取得
                    self.imu_output_raw_msg = self.connection.recv_match(type='RAW_IMU', blocking=False, timeout=0.1)
                    if self.imu_output_raw_msg:
                        # MAVLinkのRAW_IMUデータは通常ミリG単位なので、m/s²に変換
                        acc_x = self.imu_output_raw_msg.xacc * 0.00981
                        acc_y = self.imu_output_raw_msg.yacc * 0.00981
                        acc_z = self.imu_output_raw_msg.zacc * 0.00981
                        return acc_x, acc_y, acc_z
            except Exception as e:
                print(f"MAVLink IMU data error: {e}")
            
            # データが取得できない場合はモックデータを返す
            import time
            import math
            current_time = time.time()
            
            # 時間に基づいて変化する加速度データを生成
            acc_x = 0.5 * math.sin(current_time * 0.5) + 0.2 * math.cos(current_time * 0.3)
            acc_y = 0.3 * math.sin(current_time * 0.4) + 0.1 * math.cos(current_time * 0.6)
            acc_z = 0.1 * math.sin(current_time * 0.2) + 0.05 * math.cos(current_time * 0.8)
            
            return (acc_x, acc_y, acc_z)
    
    def get_imu_output_gyro_data(self):
        if self.imu_output_raw_msg:
            return self.imu_output_raw_msg.xgyro, self.imu_output_raw_msg.ygyro, self.imu_output_raw_msg.zgyro
        return (0, 0, 0)

    def get_imu_output_mag_data(self):
        if self.imu_output_raw_msg:
            return self.imu_output_raw_msg.xmag, self.imu_output_raw_msg.ymag, self.imu_output_raw_msg.zmag
        return (0, 0, 0)

    def get_delta_time(self):
        if self.imu_output_raw_msg:
            return self.imu_output_raw_msg.time_usec
        return 0
        
    def is_connected(self):
        """接続状態を確認"""
        return self.connection_established and self.connection is not None
        

if __name__ == "__main__":
    telemetry = GetTelemetry(connection_info={
        'mode': 'UDP',
        'ip': '0.0.0.0',
        'port': 14550
    })
    print(telemetry.get_imu_output_mag_data())