import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

AVAILABILITY = "availability"

DEFAULT_TOPIC_PREFIX = 'home-assistant/tank'


class MQTTClient:
    def __init__(self, broker='127.0.0.1', mqtt_auth=None, topic_prefix=DEFAULT_TOPIC_PREFIX):
        self.topic_prefix = topic_prefix
        self.broker = broker
        self.mqtt_auth = mqtt_auth
        self.client = mqtt.Client("tank-client")
        self.client.username_pw_set(**mqtt_auth)
        self.client.will_set(f'{self.topic_prefix}/{AVAILABILITY}', 'offline', 1, True)
        print(f"Publishing {DEFAULT_TOPIC_PREFIX} on {self.broker}")
        self.connect()

    def connect(self):
        self.client.connect(self.broker)
        self.client.loop_start()
        self.pub("online", topic=AVAILABILITY)

    def pub(self, value, topic=None):
        t = f"/{topic}" if topic is not None else ''
        try:
            # print(f"{self.broker} -> {self.topic_prefix}{t}", value)
            self.client.publish(f'{self.topic_prefix}{t}', value)
        except Exception as e:
            print("ERROR - Unable to send MQTT msg", e)
            self.client.loop_stop(force=True)
            self.client.disconnect()
            self.connect()

    def send(self, value):
        self.pub("online", topic=AVAILABILITY)
        v = int(float(value) * 100) if type(value) == float else value
        self.pub(v)

    def close(self):
        self.pub("offline", topic=AVAILABILITY)
        time.sleep(1)
        self.client.disconnect()


def pub(value, topic_prefix=DEFAULT_TOPIC_PREFIX, broker='127.0.0.1', mqtt_auth=None, topic=None):
    t = f"/{topic}" if topic is not None else ''
    try:
        # print(f"{broker} -> {topic_prefix}{t}", value)
        publish.single(f'{topic_prefix}{t}', value, hostname=broker, auth=mqtt_auth)
    except Exception as e:
        print("ERROR - Unable to send MQTT msg", e)
