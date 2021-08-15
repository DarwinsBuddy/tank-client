import argparse

parser = argparse.ArgumentParser(description='Tank Client')
parser.add_argument('-m', '--mock', action='store_true', help='Start with mocked measurements', default=False)
parser.add_argument('-zp', '--zmq-port', type=int, nargs=1, help='Listen port for zmq subscriber', default=5555)
parser.add_argument('-za', '--zmq-addr', type=str, nargs=1, help='Listen address for zmq subscriber',
                    default='0.0.0.0')

args = parser.parse_args()
ZMQ_RECV_TIMEOUT = 1000
MEASURING_INTERVAL = 5


class AppConfig:

    def __init__(self):
        # self.SCHEDULER_JOBSTORES = {
        #    'mongo': {
        #        'type': 'mongodb'
        #    },
        #    'default': {
        #        'type': 'sqlalchemy',
        #        'url': 'sqlite:///jobs.sqlite'
        #    }
        # }
        # Set the actuator, and the number of threads
        self.SCHEDULER_EXECUTORS = {
            'default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': 20
            },
            # 'processpool': {
            #    'class': 'apscheduler.executors.pool:ProcessPoolExecutor',
            #    'max_workers': 5
            # }
        }
        self.SCHEDULER_JOB_DEFAULTS = {
            'coalesce': False,  # Close the new job by default at #
            # 3 set maximum number of instances running simultaneously scheduler particular job
            'max_instances': 3
        }
        self.SCHEDULER_PAUSED = True
