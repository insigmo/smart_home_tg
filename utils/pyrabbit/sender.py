from time import sleep

from py_rabbit import PyRabbit

if __name__ == '__main__':
    r = PyRabbit()
    for _ in range(100):
        r.send_message('Hey there')
        print('Message sent')
        sleep(2)
