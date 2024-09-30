from confluent_kafka import Producer
import socket

class ExpenseProducer:
    def __init__(self, config=None, topic=None):
        if config is None:
            config = {
                'bootstrap.servers': 'localhost:9092',
                'client.id': socket.gethostname()
            }

        if topic is None:
            topic = 'transaction'

        self._topic = topic
        self._config = config
        self._producer = Producer(config)

    @staticmethod
    def acked(err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))

    def produce(self, message):
        self._producer.produce(self._topic, message, callback=ExpenseProducer.acked)
        self._producer.flush(1)


if __name__ == '__main__':
    producer = ExpenseProducer()
    producer.produce('Hello, Kafka! from rejeo')