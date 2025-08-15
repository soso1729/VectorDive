from pymavlink import mavutil
##後で修正
from vectordive.config import base

class WaitHeartbeat:
    def __init__(self):
        self.master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
        self.hb_timeout = base.HB_TIMEOUT

    def wait_heartbeat(self, hbtimeout=None):
        timeout = hbtimeout if hbtimeout is not None else self.hb_timeout
        try:
            hb = self.master.wait_heartbeat(timeout=timeout)
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
    heartbeat.wait_heartbeat()
