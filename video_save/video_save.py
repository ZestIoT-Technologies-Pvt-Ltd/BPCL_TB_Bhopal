import cv2
import os
import time
from datetime import datetime
pp = str(datetime.now())[0:19].replace('-','')
pp = pp.replace(' ','')
pp = pp.replace(':','')
path = pp +'.mp4'
#out = cv2.VideoWriter('a1.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 10,(1280,720))
out = cv2.VideoWriter(path,cv2.VideoWriter_fourcc(*'mp4v'), 3,(1280,720))
cam = cv2.VideoCapture('rtsp://192.168.1.51/av0_0')
#cam = cv2.VideoCapture('rtsp://192.168.1.21/ch01.264')
start = time.time()
while True:
	end = time.time()
	ret,frame = cam.read()
	frame = cv2.resize(frame,(1280,720))
	#cv2.imwrite("test9333.png",frame)
	out.write(frame)
	diff = int(end - start)
	print("running")
out.release()
