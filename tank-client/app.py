import os
import random

from apscheduler.schedulers.background import BlockingScheduler

from .config import args, MEASURING_INTERVAL
from .zeromq import ZMQPublisher


class App:

    def __init__(self, app_config):
        self.publisher = ZMQPublisher("depth", address=args.zmq_addr, port=args.zmq_port)
        if self.is_raspberry():
            from .ultrasonic import Sensor
            self.sensor = Sensor()
        else:
            self.sensor = None
        self.app_config = app_config
        self.scheduler = BlockingScheduler(
            job_executors=self.app_config.SCHEDULER_EXECUTORS,
            job_defaults=self.app_config.SCHEDULER_JOB_DEFAULTS,
            paused=self.app_config.SCHEDULER_PAUSED
        )

    @staticmethod
    def is_raspberry():
        (sysname, nodename, release, version, machine) = os.uname()
        return sysname == 'Linux' and machine == 'armv6l'

    def publish_depth(self, depth):
        print("[MEASURING] ", depth)
        if self.publisher is not None:
            self.publisher.send(f'{depth}')

    def mock_measure_depth(self, min_depth=100, max_depth=250):
        # mocked measuring
        depth = random.randint(min_depth, max_depth) / 100
        self.publish_depth(depth)

    def avg_measure_depth(self, n=5):
        if self.sensor is not None:
            depth = self.sensor.avg_measure(n)
            self.publish_depth(depth)
        else:
            print("Unable to measure depth - sensor not initialized")

    def add_jobs(self):
        if args.mock or not self.is_raspberry():
            print("Mocking measurements (either mock mode activated, or not a raspberry pi)")
            self.scheduler.add_job(func=self.mock_measure_depth,
                                   args=[100, 250],
                                   trigger='interval',
                                   seconds=MEASURING_INTERVAL,
                                   id='mock_measure_depth',
                                   name='measuring depth',
                                   replace_existing=True
                                   )
        else:
            self.scheduler.add_job(func=self.avg_measure_depth,
                                   args=[5],
                                   trigger='interval',
                                   seconds=MEASURING_INTERVAL,
                                   id='measure_depth',
                                   name='measuring depth',
                                   replace_existing=True
                                   )

    def stop(self):
        if self.scheduler is not None and self.scheduler.running:
            self.scheduler.shutdown(wait=False)
        print("shutdown zmq")
        if self.publisher is not None:
            print('shutdown zmq pub')
            self.publisher.close()
        if self.sensor is not None:
            print("Reset GPIO")
            self.sensor.cleanup()

    def start(self):
        print("Adding jobs")
        self.add_jobs()
        print("___________________")
        print(self.app_config)
        print("___________________")
        print("Starting Scheduler")
        self.scheduler.start()
        print("END")