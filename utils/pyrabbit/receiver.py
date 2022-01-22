from py_rabbit import PyRabbit


def callback(channel, method, properties, body):
    print(body.decode('utf-8'))


if __name__ == '__main__':
    r = PyRabbit()
    r.get_message(callback)