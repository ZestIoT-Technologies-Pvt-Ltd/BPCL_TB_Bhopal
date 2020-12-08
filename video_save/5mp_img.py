import cv2
import os
import time
from datetime import datetime
cam = cv2.VideoCapture('rtsp://192.168.1.51/av0_0')
path = '/media/8FC7-267D/5mp_img/'
pp = str(datetime.now())[0:19].replace('-','')
pp = pp.replace(' ','')
pp = pp.replace(':','')
path = path + pp +'.jpg'
while True:
	ret,frame =cam.read()
	frame=cv2.resize(frame,(1280,720))
	cv2.imwrite(path, frame)
	break
