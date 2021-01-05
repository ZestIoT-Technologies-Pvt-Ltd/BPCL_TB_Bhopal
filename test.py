import cv2
import os
import time
from datetime import datetime
path = '/media/49AE-64D6/v2/'
pp = str(datetime.now())[0:19].replace('-','')
pp = pp.replace(' ','')
pp = pp.replace(':','')
path = path + pp +'.mp4'
#out = cv2.VideoWriter('a1.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 10,(1280,720))
out = cv2.VideoWriter(path,cv2.VideoWriter_fourcc(*'mp4v'), 3,(1280,720))
cam = cv2.VideoCapture(0)
start = time.time()
while True:
        end = time.time()
        ret,frame = cam.read()
        frame = cv2.resize(frame,(1280,720))
        out.write(frame)
        diff = int(end - start)
        if diff >= 600:
                break
out.release()



