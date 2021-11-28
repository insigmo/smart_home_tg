import pika


class PyRabbit:
    def __init__(self, **kwargs):
        self.hostname = kwargs.pop('hostname', 'localhost')
        self.port = kwargs.pop('port', 5672)
        self.key = kwargs.pop('key', 'key*')  # key.example.* or key.example.#
        self.queue_name = kwargs.pop('queue_name', 'first-queue')
        self.exchange_name = kwargs.pop('exchange_name', 'first_exchange')
        self.exchange_type = 'topic'

        self.connection = self.create_connection(self.hostname, self.port)
        self.channel = self.connection.channel()
        self.exchange = self.create_exchange(self.exchange_name, exchange_type=self.exchange_type)
        self.queue = self.create_queue(self.queue_name)

        self.queue_bind()

    @classmethod
    def create_connection(cls, hostname: str, port: int):
        conn_params = pika.ConnectionParameters(hostname, port)
        return pika.BlockingConnection(conn_params)

    def create_queue(self, queue_name: str):
        return self.channel.queue_declare(queue_name)

    def create_exchange(self, exchange_name: str, exchange_type: str):
        return self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    def queue_bind(self):
        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name, routing_key=self.key)

    def send_message(self, text: str, **kwargs):
        exchange: str = kwargs.pop('exchange', self.exchange_name)
        key: str = kwargs.pop('key', self.key)

        self.channel.basic_publish(exchange=exchange, routing_key=key, body=text)

    def get_message(self, callback, **kwargs):
        queue_name = kwargs.pop('queue_name', self.queue_name)
        auto_ack = kwargs.pop('auto_ack', True)
        self.channel.basic_consume(queue_name, callback, auto_ack=auto_ack)

        try:
            self.channel.start_consuming()

        except KeyboardInterrupt:
            self.channel.stop_consuming()

        except Exception:
            self.channel.stop_consuming()

    @staticmethod
    def callback(channel, method, properties, body):
        print(body)

    def queue_unbind(self, queue_name: str) -> None:
        self.channel.queue_unbind(queue=queue_name, exchange=self.exchange_name, routing_key=self.key)

    def queue_delete(self, queue_name: str) -> None:
        self.channel.queue_delete(queue_name)

    def exchange_delete(self, exchange_name: str) -> None:
        self.channel.exchange_delete(exchange_name)

    def __del__(self):
        self.connection.close()
