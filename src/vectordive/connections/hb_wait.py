from pymavlink import mavutil
from vectordive.config import base

class HbWait():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.timeout = base.HB_TIMEOUT
        self.succes = False

    def get_success(self):
        self.connection = mavutil.mavlink_connection(f"udpin:{self.ip}:{self.port}")
        hb = self.connection.wait_heartbeat(timeout=self.timeout)

        if hb is None:
            self.succes = False
        else:
            self.succes = True

        return self.succes
