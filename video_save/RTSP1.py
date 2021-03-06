import cv2
import time
from datetime import datetime
import multiprocessing as mp

class camera():

    def __init__(self,rtsp_url):        
        #load pipe for data transmittion to the process
        self.parent_conn, child_conn = mp.Pipe()
        #load process
        self.p = mp.Process(target=self.update, args=(child_conn,rtsp_url))        
        #start process
        self.p.daemon = True
        self.p.start()

    def end(self):
        #send closure request to process

        self.parent_conn.send(2)

    def update(self,conn,rtsp_url):
        #load cam into seperate process

        print("Cam Loading...")
        cap = cv2.VideoCapture(rtsp_url,cv2.CAP_FFMPEG)   
        print("Cam Loaded...")
        run = True

        while run:

            #grab frames from the buffer
            cap.grab()

            #recieve input data
            rec_dat = conn.recv()


            if rec_dat == 1:
                #if frame requested
                ret,frame = cap.read()
                conn.send(frame)

            elif rec_dat ==2:
                #if close requested
                cap.release()
                run = False

        print("Camera Connection Closed")        
        conn.close()

    def get_frame(self,resize=None):
        ###used to grab frames from the cam connection process

        ##[resize] param : % of size reduction or increase i.e 0.65 for 35% reduction  or 1.5 for a 50% increase

        #send request
        self.parent_conn.send(1)
        frame = self.parent_conn.recv()

        #reset request 
        self.parent_conn.send(0)

        #resize if needed
        if resize == None:            
            return frame
        else:
            return self.rescale_frame(frame,resize)

    def rescale_frame(self,frame, percent=65):
        return cv2.resize(frame,None,fx=percent,fy=percent) 



cam = camera('rtsp://192.168.1.51/av0_0')
#p1.update('rtsp://192.168.29.51/ch01.264')
#cam = camera('rtsp://192.168.1.51/av0_0')
#cam = camera('rtsp://192.168.1.21/ch01.264')
#cam = camera('rtsp://192.168.1.21/ch01.264')

print(f"Camera is alive?: {cam.p.is_alive()}")
path = '/media/8FC7-267D/'
pp = str(datetime.now())[0:19].replace('-','')
pp = pp.replace(' ','')
pp = pp.replace(':','')
path = path + pp +'.mp4'
out = cv2.VideoWriter('aa.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 5,(1536,864))
#out = cv2.VideoWriter('/media/8FC7-267D/aa.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 2,(1280,720))
cam = cv2.VideoCapture('rtsp://192.168.29.21/ch01.264')
start = time.time()

while(1):
    end = time.time()
    frame = cam.get_frame(0.80)
    #out.write(frame)

    #cv2.imshow("Feed",frame)
    cv2.imwrite("aa1.jpg",frame)

    key = cv2.waitKey(1)

    if key == 13: #13 is the Enter Key
        break

cv2.destroyAllWindows()     

cam.end()
