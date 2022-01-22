from py_rabbit import PyRabbit

if __name__ == '__main__':
    r = PyRabbit(hostname='192.168.1.5')
    r.send_message('Hey there')
