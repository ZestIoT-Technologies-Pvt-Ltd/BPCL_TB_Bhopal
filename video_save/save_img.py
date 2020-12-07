import cv2
import os
import time
from datetime import datetime
cam = cv2.VideoCapture('rtsp://192.168.1.51/av0_0')
while True:
	ret,frame = cam.read()
	frame = cv2.resize(frame,(1280,720))
	cv2.imwrite("a3.jpg",frame)
	print("saved")
