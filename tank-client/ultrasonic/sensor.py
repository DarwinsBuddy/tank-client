import time
from collections import deque

import pigpio
from RPi import GPIO


class Sensor:
    # https://www.amazon.de/gp/product/B07SL5W6VF/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1
    TRIGGER_TIME = 0.06
    WAIT_TIME = 0.06
    # GPIO in use
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24

    speedSound_raw = 340
    temperature = 28
    # Speed of sound in m/s at temperature
    speedSound = speedSound_raw + (0.6 * temperature)

    def __init__(self, n):
        self.n = n
        self.storage = deque(maxlen=n)
        self.start = None
        self.end = None
        # Use BCM GPIO references
        # not physical pin numbering
        GPIO.setmode(GPIO.BCM)

        print("Ultrasonic Measurement")
        print("Speed of sound is", self.speedSound, "m/s")  # at ",temperature,"Celsius")

        # Set pins as output and input
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # Echo

        # try to connect to pigpio
        self.pi = pigpio.pi()
        if self.pi.connected:
            print("Activating pigpio measurement")
            self.pi_signal = self.pi.callback(self.GPIO_ECHO, pigpio.EITHER_EDGE, self.signal_echo)
        # Set trigger to False (Low)
        GPIO.output(self.GPIO_TRIGGER, False)

        # Allow module to settle
        time.sleep(0.7)

    def signal_echo(self, gpio, level, tick):
        # WARNING: tick wraps around from
        #          4294967295 to 0 roughly every 72 minutes
        if gpio == self.GPIO_ECHO:
            if level == 1:
                self.start = tick/10**6  # sec to ms
            elif level == 0:
                self.end = tick/10**6  # sec to ms
                self.store_current_distance(self.start, self.end)

    def store_current_distance(self, start, end):
        if start is not None and end is not None and end > start:
            # difference in seconds
            elapsed = end - start
            # times speed of sound divided by 2 (round trip)
            # equals distance of measurement
            distance = (elapsed * self.speedSound) / 2
            self.storage.append(distance)
        else:
            print(f"Faulty measurement: end={end} start={start}")

    def measure(self):
        # Measure distance once
        GPIO.output(self.GPIO_TRIGGER, True)
        # PIN OUTPUT 1 for TRIGGER_TIME seconds
        time.sleep(self.TRIGGER_TIME)
        # PIN OUTPUT 0
        GPIO.output(self.GPIO_TRIGGER, False)

        if not self.pi.connected:
            print("[unstable measurement]")
            self.unstable_measure()

    def unstable_measure(self):
        # start listening for response
        self.start = time.time()
        while GPIO.input(self.GPIO_ECHO) == 0:
            self.start = time.time()

        # as soon as ECHO_INPUT is 1 measure time
        self.end = time.time()
        while GPIO.input(self.GPIO_ECHO) == 1:
            self.end = time.time()
        self.store_current_distance(self.start, self.end)

    def current_depth(self):
        if self.storage is not None and len(self.storage) > 0:
            ls = list(self.storage)
            return sum(ls) / len(ls)
        else:
            return None

    @staticmethod
    def cleanup():
        # Reset GPIO settings
        GPIO.cleanup()
