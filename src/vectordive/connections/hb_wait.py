from pymavlink import mavutil
from vectordive.config import base

class WaitHeartbeat:
    hb_timeout = base.HB_TIMEOUT  # 
    def __init__(self, mav_connection):
        self.mav_connection = mav_connection

    def wait(self, hb_timeout):
        master = mavutil.mavlink_connection(self.mav_connection)
        
        try:
            self.mav_connection.wait_heartbeat(timeout=hb_timeout)
            return True
        except mavutil.MAVError as e:
            print(f"Heartbeat wait failed: {e}")
            return False
        
if __name__ == "__main__":
    # Example usage
    connection = mavutil.mavlink_connection('udpin:localhost:14550')
    hb_waiter = WaitHeartbeat(connection)
    if hb_waiter.wait(hb_waiter.hb_timeout):
        print("Heartbeat received successfully.")
    else:
        print("Failed to receive heartbeat within timeout.")