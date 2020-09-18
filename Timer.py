from datetime import datetime,timedelta
from sockets import ClientSocket
import json
from pynng import Timeout
import cv2
from threading import Thread
import error
import os
config="/home/smartcow/BPCL/BPCL_final/BPCL_config.json"
with open(config) as json_data:
	info=json.load(json_data)
	Palert_frame,Palert_time,Dalert_frame,Dalert_time,Malert_frame,Malert_time = info["Palert_frame"],info["Palert_time"],info["Dalert_frame"], info["Dalert_time"],info['Malert_frame'],info["Malert_time"]
	vid_duration,event_file,gpu_path= info["vid_duration"], info["event_file"],info["gpu_path"]

Ptimer,Pdetect,Pcheck,Pst_time,Ptrigger = 0,0,0,0,0
Dtimer,Ddetect,Dcheck,Dst_time,Dtrigger = 0,0,0,0,0
Mtimer,Mdetect,Mcheck,Mst_time,Mtrigger = 0,0,0,0,0
vid_path="/home/"
fourcc = cv2.VideoWriter_fourcc(*'XVID')

def start_video(event,cam):
	global Dtimer,Ptimer,Mtimer,vid_path
	event_out=cv2.VideoWriter(vid_path,fourcc, 10, (1280,720), True)
	vid_end_time=datetime.now()+timedelta(seconds=vid_duration)
	while (Dtimer > 0 or Ptimer > 0 or Mtimer > 0) and datetime.now() < vid_end_time:
		img=cam.get_frame()
		encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50] # Giving required quility
		result, encimg = cv2.imencode('.jpg',img, encode_param) #Encoding frame
		img = cv2.imdecode(encimg, 1)
		event_out.write(img)

def event_call(event):
	global vid_path
	sc=ClientSocket(device_id=str('BPCL_BPL_NX_0001'))
	try:
		logdate=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
		print("video Path {}".format(vid_path))
		data={'event_time':logdate}
		sc.send(time_stamp=logdate, message_type=event, data=data)
		msg = sc.receive()
		print(msg)
		try:
			print("Event call before success check",msg["data"]["status"])
			print(type(int(msg["data"]["status"])))

			if int(msg["data"]["status"]) == 200:
				print("API success")
		except Exception as e:
			print("Error while calling API")
			#error("7",str(e))
			return  loc
	except KeyboardInterrupt:
		sc.close()
	except Timeout:
		pass


def timer(algo,flag,cam):
	try:
		global vid_path,Ptimer,Pdetect,Palert_frame,Palert_time,Pcheck,Pst_time,Ptrigger, Dtimer,Ddetect,Dcheck,Dst_time,Dtrigger,Dalert_frame,Dalert_time,Mtimer,Mdetect,Mcheck,Mst_time,Mtrigger,Malert_frame,Malert_time
		if algo == "person" :
			Pflag = flag
			if Pflag == True:
				print("person pflag",Pflag,Ptimer)
				Pcheck = 0
				Pdetect = Pdetect +1
				if Ptimer != 0 and Pdetect > Palert_frame:
					with open(event_file,'w') as efile:
						#efile.write("EVENT21_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT21_OFF")
					if Ptimer == 2 :
						vid_file=event_call("EVENT21_OFF")
						current_time = datetime.now()
						current_time = str(current_time)[10:]
						print("*********  Rectification!!! Person in ROI  ******* Time : " , current_time)
					Ptimer = 0
			else:
				print("ptimer",Ptimer,Pcheck,Pdetect, Palert_frame)
				if Pcheck == 0 and Ptimer == 0:
					Pst_time =datetime.now()
					Pcheck = 1
				if datetime.now() > Pst_time + timedelta(seconds=2) and Ptimer == 0 and Pcheck == 1:
					Pflag = False
					Ptimer=1
					video_trigger(cam)
					Pdetect=0
					Ptrigger=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********** Person Timer Started ******* Time : ", current_time)

				elif Ptimer ==1 and Pdetect <= Palert_frame and datetime.now() > Ptrigger + timedelta(seconds=Palert_time):
					with open(event_file,'w') as efile:
						#efile.write("EVENT21_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT21_ON")
					event_call("EVENT21_ON")
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********  ALERT!!! Person not in ROI  ******* Time : " , current_time)
					Ptimer = 2
					
			return(Pflag)

		if algo == "direction":
			Dflag = flag
			if Dflag ==True:
				Dcheck = 0
				Ddetect = Ddetect +1
				
				if Dtimer != 0 and Ddetect >= Dalert_frame:
					with open(event_file,'w') as efile:
						#efile.write("EVENT21_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT22_OFF")
					if Dtimer == 2 :		
						vid_file=event_call("EVENT22_OFF")
						current_time = datetime.now()
						current_time = str(current_time)[10:]
						print("*********  Rectification!!! Person is attentive  ******* Time : " , current_time)
					Dtimer = 0
			else:
				if Dcheck == 0 and Dtimer == 0:
					Dst_time =datetime.now()
					Dcheck = 1
				if datetime.now() > Dst_time + timedelta(seconds=2) and Dtimer == 0 and Dcheck == 1:
					flag = False
					Dtimer=1
					video_trigger(cam)
					Ddetect=0
					Dtrigger=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********** Direction Timer Started ***** Time : ", current_time)

				elif Dtimer ==1 and Ddetect <= Dalert_frame and datetime.now() > Dtrigger + timedelta(seconds=Dalert_time):
					with open(event_file,'w') as efile:
						#efile.write("EVENT22_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT22_ON")
					event_call("EVENT22_ON")
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********  ALERT!!!   not looking in that direction ***** Time : ", current_time)
					Dtimer = 2		
			return(Dflag)

		if algo == "motion":
			Mflag = flag
			if Mflag == True:
				Mcheck = 0
				Mdetect = Mdetect +1
				
				if Mtimer != 0 and Mdetect >= Malert_frame:
					with open(event_file,'w') as efile:
						#efile.write("EVENT21_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT23_OFF")
					if Mtimer == 2 :				
						vid_file=event_call("EVENT23_OFF")
						current_time = datetime.now()
						current_time = str(current_time)[10:]
						print("*********  Rectification!!! Person is attentive  ******* Time : " , current_time)
					Mtimer = 0
			else:
				if Mcheck == 0 and Mtimer == 0:
					Mst_time =datetime.now()
					Mcheck = 1
				if datetime.now() > Mst_time + timedelta(seconds=5) and Mtimer == 0 and Mcheck == 1:
					flag = False
					Mtimer=1
					video_trigger(cam)
					Mdetect=0
					Mtrigger=datetime.now()
					timer5 = "Motion Timer Started"
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********** Motion Timer Started *** Time : ", current_time)

				if Mtimer ==1 and Mdetect <= Malert_frame and datetime.now() > Mtrigger + timedelta(seconds=Malert_time):
					with open(event_file,'w') as efile:
						#efile.write("EVENT23_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT23_ON")
					event_call("EVENT23_ON")
					timer6 = "ALERT!!! Motion is not detected"
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********  ALERT!!!   Motion is not detected *** Time :", current_time)
					Mtimer = 2
			return(Mflag)
	except Exception as e:
		print (str(e),"error in timer")
		#error("7",str(e))

def video_trigger(cam):
	global vid_path
	try:
		if (Dtimer > 0 or Mtimer > 0 or Ptimer > 0):
			vid_dir=(datetime.now()).strftime("%Y_%m_%d")
			loc=gpu_path+vid_dir+"/"
			vid_name="BHOPAL_BPCL_NX1_"+(datetime.now()).strftime("%Y-%m-%dT%H-%M-%S")+".avi"
			vid_path = loc+vid_name
			#print("Path to the video {}".format(vid_path))
			if not os.path.isdir(loc):
				#print("make directory")
				os.mkdir(loc)
			if Ptimer == 1:
				event = "EVENT21_OFF"
			elif Dtimer == 1:
				event = "EVENT22_OFF"
			elif Mtimer == 1:
				event = "EVENT23_OFF"
			video=Thread(target=start_video,args=(event,cam))
			video.start()
	except Exception as e:
		print (str(e),"error in timer")
		#error("7",str(e))
