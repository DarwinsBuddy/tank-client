import argparse
import configparser

from . import get_data


class AppConfig:
    ZMQ_RECV_TIMEOUT = 1000
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
        'max_instances': 2
    }
    SCHEDULER_PAUSED = True

    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description='Tank Client')
        parser.add_argument('-m', '--mock', action='store_true', help='Start with mocked measurements', default=False)
        parser.add_argument('-o', '---mode', type=str,
                            help='Choose broadcasting mode. "ha" for homeassistant, "server" for tankserver',
                            choices=['ha', 'server'], default='ha')
        parser.add_argument('-s', '--sma', type=int,
                            help='How many measurements for forming an SMA. i.e. SMA(n)',
                            default=None
                            )
        parser.add_argument('-mb', '--mqtt-broker', type=str,
                            help='IP address of MQTT broker ("ha" mode)',
                            default=None
                            )
        parser.add_argument('-mu', '--mqtt-username', type=str,
                            help='username MQTT ("ha" mode)',
                            default=None
                            )
        parser.add_argument('-mp', '--mqtt-password', type=str,
                            help='password MQTT ("ha" mode)',
                            default=None
                            )
        parser.add_argument('-mt', '--mqtt-topic', type=str,
                            help='MQTT topic ("ha" mode)',
                            default=None
                            )
        parser.add_argument('-a', '--zmq-address', type=str,
                            help='IP address of tank server ("server" mode)',
                            default=None
                            )
        parser.add_argument('-p', '--zmq-port', type=int,
                            help='ZMQ port of tank server ("server" mode)',
                            default=None
                            )
        parser.add_argument('-i', '--measurement-interval', type=int,
                            help='Interval in seconds between depth measurements ("server" mode)',
                            default=None
                            )
        parser.add_argument('-b', '--broadcast-interval', type=int,
                            help='Interval in seconds between depth broadcasts ("server" mode)',
                            default=None
                            )
        parser.add_argument('-q', '--quiet', type=bool, help='Quiet mode', default=None)
        parser.add_argument('-c', '--config', type=str,
                            help='Path to config file',
                            default=get_data('tank-client.conf')
                            )

        return parser.parse_args()

    @staticmethod
    def read_config(path):
        # print(f"Reading config file '{path}'")
        config = configparser.ConfigParser()
        with open(path, 'r') as configfile:
            config.read_file(configfile)
        return config

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.config = self.read_config(args.config)

        if self.config.has_section("Server"):
            if self.args.zmq_address is not None:
                self.zmq_addr = self.args.zmq_address
            else:
                self.zmq_addr = self.config['Server']['address'] or '127.0.0.1'
            if self.args.zmq_port is not None:
                self.zmq_port = self.args.zmq_port
            else:
                self.zmq_port = self.config['Server']['zmq-port'] or 5555
        if self.config.has_section("General"):
            if self.args.mode is not None:
                self.mode = self.args.mode
            else:
                self.mode = self.config['General']['mode'] or None
            if self.args.quiet is not None:
                self.quiet = self.args.quiet
            else:
                self.quiet = self.config['General']['quiet'] or False
            if self.args.sma is not None:
                self.sma = self.args.sma
            else:
                self.sma = int(self.config['General']['sma']) or 5
            if self.args.measurement_interval is not None:
                self.measurement_interval = self.args.measurement_interval
            else:
                self.measurement_interval = int(self.config['General']['measurement-interval']) or 10
            if self.args.broadcast_interval is not None:
                self.broadcast_interval = self.args.broadcast_interval
            else:
                self.broadcast_interval = int(self.config['General']['broadcast-interval']) or 6
        if self.config.has_section("HA"):
            if self.args.mqtt_broker is not None:
                self.mqtt_broker = self.args.mqtt_broker
            else:
                self.mqtt_broker = self.config['HA']['broker'] or '127.0.0.1'
            if self.args.mqtt_topic is not None:
                self.mqtt_topic = self.args.mqtt_topic
            else:
                self.mqtt_topic = self.config['HA']['topic'] or 'home-assistant/tank'
            if self.args.mqtt_username is not None:
                self.mqtt_username = self.args.mqtt_username
            else:
                self.mqtt_username = self.config['HA']['username'] or 'mqtt'
            if self.args.mqtt_password is not None:
                self.mqtt_password = self.args.mqtt_password
            else:
                self.mqtt_password = self.config['HA']['password'] or ''
