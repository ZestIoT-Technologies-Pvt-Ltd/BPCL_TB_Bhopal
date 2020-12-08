import time
from pynng import Timeout
from sockets import ClientSocket


def main():
    sc = ClientSocket(client_id=str('GPU_001'))
    
    while True:
        try:
            data = {'key': 'value'}
            sc.send(status='SYS_INFO', data=data)
            time.sleep(5)
            msg = sc.receive()
            print(msg)
        except KeyboardInterrupt:
            sc.close()
        except Timeout:
            pass
        time.sleep(30)  # wait time (in Seconds) to send next msg

if __name__ == '__main__':
    main()
