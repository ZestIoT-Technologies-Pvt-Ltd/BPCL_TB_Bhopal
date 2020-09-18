import cv2
import io
import socket
import struct
import time
import pickle
#import zlib
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.132', 8097))
connection = client_socket.makefile('wb')
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
def screening(frame):
	try:
		result, frame = cv2.imencode('.jpg', frame, encode_param)
		data = pickle.dumps(frame, 0)
		size = len(data)  # size of the frame
		client_socket.sendall(struct.pack(">L", size) + data)
		# img_counter += 1
		time.sleep(0.1)
		#print("s")
	except KeyboardInterrupt:
		cam.release()
		sys.exit(1)
	except Exception as e:
		print(e.__str__())

