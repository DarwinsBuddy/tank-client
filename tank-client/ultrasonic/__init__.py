import threading
import time

from .sensor import Sensor


class ThreadedSensor(threading.Thread):

    def __init__(self, timeout=1):
        super().__init__()
        self.sensor = Sensor()
        self.running = True
        self.timeout = timeout

    def run(self):
        while self.running:
            distance = self.sensor.avg_measure()
            print("Distance : {0:5.1f}m".format(distance))
            time.sleep(self.timeout)
        self.sensor.cleanup()

    def stop(self):
        self.running = False
