from pymavlink import mavutil
from config import timeout  

## mavlink経由で0.0.0.0:14550に接続し、heartbeatを待機する
class WaitHeartbeat:
    master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

    @staticmethod
    def wait_heartbeat(timeout):
        try:
            master = WaitHeartbeat.master
            hb = master.wait_heartbeat(timeout=timeout)
            if hb is not None:
                print("Heartbeat received")
                return True
            else:
                print("Error: Heartbeat not received within timeout")
                return False

        except Exception as e:
            print(f"Error waiting for heartbeat: {e}")
            return False

if __name__ == "__main__":
    heartbeat = WaitHeartbeat()
    heartbeat.wait_heartbeat(timeout)
