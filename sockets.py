import os
import time
import json
from datetime import datetime
from pynng import Pair1, TLSConfig


class Config(object):
    FILE_DIR = '/home/smartcow/BPCL/BPCL_final/client/files'
    #KEY_PAIR = os.path.join(FILE_DIR, 'key_pair.pem')
    CA_CERT = os.path.join(FILE_DIR, 'ca.crt')
    SOCKET_URL = 'tls+tcp://edgeai:55555'

class ClientSocket:
    """
    Socket(Pair1) class for dialer.
    """

    def __init__(self, device_id):
        """
        function to initialize dialer.
        :param device_id: id to identify the client.
        """
        self.device_id = device_id

        self.tls_config = TLSConfig(mode=TLSConfig.MODE_CLIENT,
                                    ca_files=[str(Config.CA_CERT)])
        self.client = Pair1(polyamorous=True, recv_timeout=5000, send_timeout=5000)
        self.client.tls_config = self.tls_config
        self.client.dial(Config.SOCKET_URL, block=False)

    def receive(self):
        """
        function to receive message on the socket.
        :return: data in json format
        """
        return json.loads(self.client.recv().decode().replace("'", "\""))

    def send(self, message_type, time_stamp=None, data=None):
        """
        function to send message on the socket.
        :param time_stamp: time stamp of message recorded
        :param data: data to send
        :param message_type: message type
        :return: None
        """
        if not time_stamp:
            time_stamp = time.time()
            time_stamp = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        response = {'device_id': self.device_id, 'time_stamp': time_stamp, 'message_type': message_type,
                    'data': data if data else {}}
        self.client.send(str(response).encode())

    def close(self):
        """
        function to close the socket.
        :return: None
        """
        self.client.close()
