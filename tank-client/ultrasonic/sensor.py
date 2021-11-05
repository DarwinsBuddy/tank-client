import time
from collections import deque

from RPi import GPIO


class Sensor:
    # https://www.amazon.de/gp/product/B07SL5W6VF/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1
    TRIGGER_TIME = 0.06
    WAIT_TIME = 0.06
    AVG_MEASUREMENTS = 5
    # GPIO in use
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24

    speedSound_raw = 340
    temperature = 28
    # Speed of sound in m/s at temperature
    speedSound = speedSound_raw + (0.6 * temperature)

    def __init__(self, n=AVG_MEASUREMENTS):
        self.n = n
        self.storage = deque(maxlen=n)
        # Use BCM GPIO references
        # not physical pin numbering
        GPIO.setmode(GPIO.BCM)

        print("Ultrasonic Measurement")
        print("Speed of sound is", self.speedSound, "m/s")  # at ",temperature,"Celsius")

        # Set pins as output and input
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # Trigger
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # Echo

        # Set trigger to False (Low)
        GPIO.output(self.GPIO_TRIGGER, False)

        # Allow module to settle
        time.sleep(0.7)

    def measure(self):
        # Measure distance once
        GPIO.output(self.GPIO_TRIGGER, True)
        # PIN OUTPUT 1 for TRIGGER_TIME seconds
        time.sleep(self.TRIGGER_TIME)
        # PIN OUTPUT 0
        GPIO.output(self.GPIO_TRIGGER, False)
        # start listening for response
        start = time.time()
        while GPIO.input(self.GPIO_ECHO) == 0:
            start = time.time()

        # as soon as ECHO_INPUT is 1 measure time
        stop = time.time()
        while GPIO.input(self.GPIO_ECHO) == 1:
            stop = time.time()

        # difference in seconds
        elapsed = stop - start
        # times speed of sound divided by 2 (round trip)
        # equals distance of measurement
        distance = (elapsed * self.speedSound) / 2

        return distance

    def deque_measure(self):
        self.storage.append(self.measure())
        ls = list(self.storage)
        return sum(ls) / len(ls)

    def avg_measure(self):
        # Take n measurements, return average
        distances = []
        for i in range(0, self.n):
            distances.append(self.measure())
            time.sleep(self.WAIT_TIME)

        return sum(distances) / self.n

    @staticmethod
    def cleanup():
        # Reset GPIO settings
        GPIO.cleanup()
