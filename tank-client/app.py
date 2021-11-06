import os
import random

from apscheduler.schedulers.background import BlockingScheduler

from .config import AppConfig
from .zeromq import ZMQPublisher


class App:

    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self.publisher = ZMQPublisher("depth", address=self.app_config.zmq_addr, port=self.app_config.zmq_port)
        if self.is_raspberry():
            from .ultrasonic import Sensor
            self.sensor = Sensor(app_config.sma)
        else:
            self.sensor = None
        self.scheduler = BlockingScheduler(
            job_executors=self.app_config.SCHEDULER_EXECUTORS,
            job_defaults=self.app_config.SCHEDULER_JOB_DEFAULTS,
            paused=self.app_config.SCHEDULER_PAUSED
        )

    @staticmethod
    def is_raspberry():
        (sysname, nodename, release, version, machine) = os.uname()
        return sysname == 'Linux' and machine == 'armv6l'

    def broadcast(self):
        self.publish_depth(self.sensor.current_depth())

    def publish_depth(self, depth):
        if self.publisher is not None and depth is not None:
            print(f"[Broadcasting] {depth}")
            self.publisher.send(f'{depth}')
        else:
            print(f"Skipping broadcast depth={depth}")

    def mock_measure_depth(self, min_depth=0, max_depth=165):
        # mocked measuring
        depth = random.randint(min_depth, max_depth) / 100
        self.publish_depth(depth)

    def avg_measure_depth(self):
        if self.sensor is not None:
            # print("[MEASURING]")
            self.sensor.measure()
        else:
            print("Unable to measure depth - sensor not initialized")

    def add_jobs(self):
        if self.app_config.args.mock or not self.is_raspberry():
            print("Mocking measurements (either mock mode activated, or not a raspberry pi)")
            self.scheduler.add_job(func=self.mock_measure_depth,
                                   args=[0, 165],
                                   trigger='interval',
                                   seconds=self.app_config.measurement_interval,
                                   id='mock_measure_depth',
                                   name='measuring depth',
                                   replace_existing=True
                                   )
        else:
            self.scheduler.add_job(func=self.broadcast,
                                   args=[],
                                   trigger='interval',
                                   seconds=self.app_config.broadcast_interval,
                                   id='broadcast_depth',
                                   name='broadcast depth',
                                   replace_existing=True
                                   )
            self.scheduler.add_job(func=self.avg_measure_depth,
                                   args=[],
                                   trigger='interval',
                                   seconds=self.app_config.measurement_interval,
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
