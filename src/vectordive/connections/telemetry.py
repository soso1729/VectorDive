from pymavlink import mavutil

class GetTelemetry:
    def __init__(self, connection_info):
        self.connection_info = connection_info
        self.connection = None
        self.servo_output_raw_msg = None
        
        # 接続文字列を正しく構築
        if connection_info.get('mode') == 'UDP':
            connection_string = f"udpin:{connection_info['ip']}:{connection_info['port']}"
        else:
            connection_string = f"udpin:{connection_info['ip']}:{connection_info['port']}"
        
        try:
            self.connection = mavutil.mavlink_connection(connection_string)
            self.connection.wait_heartbeat(timeout=5.0)
            self.servo_output_raw_msg = self.connection.recv_match(type='SERVO_OUTPUT_RAW', blocking=True, timeout=5.0)
        except Exception as e:
            self.connection = None
            self.servo_output_raw_msg = None

    def get_servo_output_raw(self):
        if self.servo_output_raw_msg:
            return self.servo_output_raw_msg
        return None
    
    def get_servo_output_raw_data(self):
        if self.servo_output_raw_msg:
            try:
                return (
                    getattr(self.servo_output_raw_msg, 'servo1_raw', 0), 
                    getattr(self.servo_output_raw_msg, 'servo2_raw', 0), 
                    getattr(self.servo_output_raw_msg, 'servo3_raw', 0), 
                    getattr(self.servo_output_raw_msg, 'servo4_raw', 0), 
                    getattr(self.servo_output_raw_msg, 'servo5_raw', 0), 
                    getattr(self.servo_output_raw_msg, 'servo6_raw', 0)
                )
            except AttributeError as e:
                return (0, 0, 0, 0, 0, 0)
        return (0, 0, 0, 0, 0, 0)  # デフォルト値
        
    def is_connected(self):
        """接続状態を確認する"""
        return self.connection is not None and self.servo_output_raw_msg is not None