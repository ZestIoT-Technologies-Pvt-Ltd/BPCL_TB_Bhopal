# Documentation to initialize client socket

This document provides the steps to init the client socket for nng pair communication.

## To init the socket

1. import Client socket class `from sockets import ClientSocket`. 
2. To create the client object `sc = ClientSocket(client_id=str('ABC01'))`. It takes argument `client_id` as client(node) ID. 

## Send message on socket

use  `sc.send(status='SYS_INFO', data=data)` to send. `status` can be any protocol code or topic name and `data` is the data we want to send.

## receive msg on socket

use  `sc.receive()` to receive msg on socket, returns the msg.

## msg(request or response) structure

response/msg: `{'status'='SYS_INFO', 'data=data'}`

## sample code
```sc = ClientSocket(client_id=str('ABC01'))
    while True:
        try:
            data = {'key': 'value'}  # data in any format such as dict or list
            sc.send(status='SYS_INFO', data=data)
            time.sleep(5)
            msg = sc.receive()
            print(msg)
        except KeyboardInterrupt:
            sc.close()
        except Timeout:
            pass
        time.sleep(300)
```
