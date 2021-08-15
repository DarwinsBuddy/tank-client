import zmq


class ZMQPublisher:

    def __init__(self, topic, address='localhost', port=5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.setsockopt(zmq.LINGER, 0)  # discard unsent messages on close
        self.target = f'tcp://{address}:{port}'
        print(f"Publishing {topic} on {self.target}")
        self.socket.connect(self.target)
        self.topic = topic

    def send(self, msg):
        self.socket.send(bytes(f'{self.topic} {msg}', encoding='utf-8'))

    def close(self):
        self.socket.close(0)
