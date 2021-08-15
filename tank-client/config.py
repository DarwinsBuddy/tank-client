import argparse
import configparser

import pkg_resources


class AppConfig:
    ZMQ_RECV_TIMEOUT = 1000
    MEASURING_INTERVAL = 5
    # SCHEDULER_JOBSTORES = {
    #    'mongo': {
    #        'type': 'mongodb'
    #    },
    #    'default': {
    #        'type': 'sqlalchemy',
    #        'url': 'sqlite:///jobs.sqlite'
    #    }
    # }
    # Set the actuator, and the number of threads
    SCHEDULER_EXECUTORS = {
        'default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': 20
        },
        # 'processpool': {
        #    'class': 'apscheduler.executors.pool:ProcessPoolExecutor',
        #    'max_workers': 5
        # }
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,  # Close the new job by default at #
        # 3 set maximum number of instances running simultaneously scheduler particular job
        'max_instances': 3
    }
    SCHEDULER_PAUSED = True

    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Tank Client')
        parser.add_argument('-m', '--mock', action='store_true', help='Start with mocked measurements', default=False)
        parser.add_argument('-c', '--config', type=str,
                            help='Path to config file',
                            default=pkg_resources.resource_filename('tank-client', 'resources/tank-client.conf')
                            )

        return parser.parse_args()

    @staticmethod
    def read_config(path):
        config = configparser.ConfigParser()
        with open(path, 'r') as configfile:
            config.read_file(configfile)
        return config

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.config = self.read_config(args.config)
        self.zmq_addr = self.config['Server']['address'] or '127.0.0.1'
        self.zmq_port = self.config['Server']['zmq-port'] or 5555
