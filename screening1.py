'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Takes the input frame from the camera
Output: Streams the frame using Raspberrypi on the screen
Requirements:
This function shall perform the following:
1) The socket makes the connection between NX device and Raspberrypi
2)Streams the frames on the web application
'''    
import cv2
import socket
import struct
import time
import pickle
import error
'''
client_socket = This variable shall create a socket pair and connect IP address and port.
encode_param = This variable shall be used to change the quality of the frame

'''
def create():
	global client_socket
	try:
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except Exception as e:
		error.raised("8",str(e))
		print("Not able to create client socket")
		time.sleep(1)
		create()

def connect(ip,port1):
	global client_socket, encode_param
	try:
		client_socket.connect((ip, port1))
		connection = client_socket.makefile('wb')
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
	except Exception as e:
		error.raised("8",str(e))
		print("Not able to connect to pi, will try again")
		time.sleep(1)
		connect()

def screening(frame):
	global client_socket, encode_param
	try:		
		result, frame = cv2.imencode('.jpg', frame, encode_param)
		data = pickle.dumps(frame, 0)
		size = len(data)  # size of the frame
		client_socket.sendall(struct.pack(">L", size) + data)
		# img_counter += 1
		time.sleep(0.1)
		#print("s")
	except Exception as e:
		print(e.__str__())
		error.raised("9",str(e))