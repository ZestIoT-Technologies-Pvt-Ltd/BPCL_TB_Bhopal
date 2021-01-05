#   Copyright (C) 2020 by ZestIOT. All rights reserved. The information in this 
#   document is the property of ZestIOT. Except as specifically authorized in 
#   writing by ZestIOT, the receiver of this document shall keep the information
#   contained herein confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and disseminations to 
#   the receiver's employees shall only be made on a strict need to know basis.
"""
timer function
Input: algo(which event is being considered Person in ROI, view direction, motion of the person),
       flag(if the event is true in the particular frame or not), cam(cv2 camera feed object)
variables: Pdetect(it increments when flag is true in the frame),Pcheck(flag to start buffer time when flag is False),
           Ptimer(flag to start Actual Alert timer),Pst_time(start time for buffer time),Ptrigger(start time for Alert Timer).
           Palert_frame(number of false positives to be considered before resetting the Timer),
           Palert_time(duration of the timer),Pflag(if the erue or false for the particular frame)
Note: variables are similar for all three events

User Requirements:
1} Start Timer and Raise Alarm when person is not attentive.

Requirements:
1) check if the flag is true or false for the given event/algo
2) If the flag is false for continuosly for buffer time(2 seconds or more) then initiate the timer
3) I fthe flag is still false for the Timer period(Palert_time) than we call the event function
4) In between if the person comes back then we restart the process

Start_video function
Input: event name and cam (cv2 camera feed object),
variable: vid_path(path of the video on device to sent with event api call),
Requirement: 
1) start saving camera feed into a video when timer has started for any event upto video duration time

event_call function
Input: event name
Requirements
1) it create a Clientsocket object with unique device id
2) sends the Event information with Timestamp and the path of the video to the Pi device

video_trigger function
Input: cam(cv2 camera feed object)
Requirements:
1)It checks if the Timer for any event Alert has been started.
2) Checks if a folder has been created  for today or not.
3) If not it creates a folder 
4) if the Timer has started then it create a thread for saving a video(Start_video)

"""

from datetime import datetime,timedelta
from sockets import ClientSocket
import json
import cv2
from threading import Thread
import error
import shutil
import time
import os
er =0
config1="/home/nvidia/BPCL/BPCL_final/UI_parameters.json"
config="/home/nvidia/BPCL/BPCL_final/BPCL_config.json"
with open(config) as json_data:
	info=json.load(json_data)
	Palert_frame,Dalert_frame,Malert_frame= info["Palert_frame"],info["Dalert_frame"],info['Malert_frame']
	event_file,gpu_path,temp_folder = info["event_file"],info["gpu_path"],info["temp_folder"]

with open(config1) as json_data:
	info =json.load(json_data)
	Palert_time,Dalert_time=int(info["Person_ROI_unavailable"]), int(info["Person_not_attentive"])
	Roi_rectify,attentive_rectify=int(info["Person_ROI_rectify"]),int(info["Person_attentive_rectify"])
	Malert_time=Dalert_time
print("Palert -> ", Palert_time, Dalert_time, Malert_time)
Ptimer,Pdetect,Pcheck,Pst_time,Ptrigger,Prectify,Pback,Pfp_time,Pvideo,Ppath,Pvend_time = 0,0,0,0,0,0,0,0,0,0,0
Dtimer,Ddetect,Dcheck,Dst_time,Dtrigger,Drectify,Dback,Dfp_time,Dvideo,Dpath,Dvend_time = 0,0,0,0,0,0,0,0,0,0,0
Mtimer,Mdetect,Mcheck,Mst_time,Mtrigger,Mrectify,Mback,Mfp_time,Mvideo,Mpath,Mvend_time = 0,0,0,0,0,0,0,0,0,0,0
vid_path="/media/49AE-64D6/"
video_flag =0
temp_file="/media/49AE-64D6/"
fourcc = cv2.VideoWriter_fourcc(*'XVID')

def start_video(event):
	global Pvideo,Mvideo,Dvideo,Ppath,Dpath,Mpath,Pevent_out,Mevent_out,Devent_out,Pvend_time,Mvend_time,Dvend_time,Palert_time,Dalert_time,Malert_time
	vid_dir=(datetime.now()).strftime("%Y_%m_%d")
	loc=gpu_path+vid_dir+"/"
	if not os.path.isdir(loc):
		#print("make directory")
		os.mkdir(loc)
	if event == "EVENT21_ON":
		description = "PERSON_NOT_IN_ROI"
	elif event == "EVENT22_ON" or event == "EVENT23_ON":
		description = "PERSON_NOT_ATTENTIVE"
	vid_name="JALGAON_BPCL_NX1_"+description+"_"+event+"_"+(datetime.now()).strftime("%Y-%m-%dT%H-%M-%S")+".avi"
	if event == "EVENT21_ON":
		Ppath = loc+vid_name
		Pvideo = temp_folder+vid_name
		Pevent_out=cv2.VideoWriter(Pvideo,fourcc, 3, (1280,720), True)
		Pvend_time=datetime.now()+timedelta(seconds=Palert_time)
	elif event == "EVENT22_ON":
		Dpath = loc+vid_name
		Dvideo = temp_folder+vid_name
		Devent_out=cv2.VideoWriter(Dvideo,fourcc, 3, (1280,720), True)
		Dvend_time=datetime.now()+timedelta(seconds=Dalert_time)
	elif event == "EVENT23_ON":
		Mpath = loc+vid_name
		Mvideo = temp_folder+vid_name
		Mevent_out=cv2.VideoWriter(Mvideo,fourcc, 3, (1280,720), True)
		Mvend_time=datetime.now()+timedelta(seconds=Malert_time)

def video_function(event,cam):
	global Pvend_time,Dvend_time,Mvend_time,Ptimer,Dtimer,Mtimer,Pevent_out,Devent_out,Mevent_out
	while True:
		if (Dtimer > 0 or Mtimer > 0 or Ptimer >0):
			img = cam.get_frame()
			#img = cam.read()
			#print (img)
			#cv2.imwrite("check.jpg",img)
			img = cv2.resize(img,(1280,720))
			encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50] # Giving required quility
			result, encimg = cv2.imencode('.jpg',img, encode_param) #Encoding frame
			img = cv2.imdecode(encimg, 1)
			ls_time = datetime.now()
			#print (Pvend_time)
			if Pvend_time != 0:
				if datetime.now()>Pvend_time:
					#print ("******************* breaking **********************")
					Pvend_time=0
					Pevent_out.release()
				Pevent_out.write(img)
				#print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&writen&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
			if Dvend_time != 0:
				if datetime.now()>Dvend_time:
					Dvend_time = 0
					Devent_out.release()
				Devent_out.write(img)
			if Mvend_time != 0:
				if datetime.now()>Mvend_time:
					Mvend_time=0
					Mevent_out.release()
				Mevent_out.write(img)
			le_time = datetime.now()
			while(int((le_time -ls_time).total_seconds()*1000) < 300 ):
					le_time = datetime.now()

def event_call(event,temp,path):
	global er
	try:
		sc=ClientSocket(device_id=str('BPCL_JAL_NX_0001'))
	except Exception as e:
		print("Client socket error")
		er=er+1
		if er < 4:
			time.sleep(1)
			event_call(event,path)
		error.raised("3",str(e))

	try:
		logdate=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
		#print("video Path {}".format(vid_path))
		if path  == None:
			if event == "Reset":
				data={'event_time':logdate,'event_description':"Reset function"}
			elif event == "EVENT21_OFF":
				data={'event_time':logdate,'event_description':"Person not in ROI Rectified"}
			elif event == "EVENT22_OFF" or event == "EVENT23_OFF":
				data={'event_time':logdate,'event_description':"Person not attentive Rectified"}
		else:
			shutil.move(temp,path)
			print("file moved from {} to {}".format(temp,path))
			if event == "EVENT21_ON":
				data={'event_time':logdate,'path':path,'event_description':"Person not in ROI"}
			elif event == "EVENT22_ON" or event == "EVENT23_ON":
				data={'event_time':logdate,'path':path,'event_description':"Person not attentive"}
		print(data)
		if event == "Reset":
			event = "EVENT21_OFF"
		sc.send(time_stamp=logdate, message_type=event, data=data)
		msg = sc.receive()
		print(msg)
		if int(msg["data"]["status"]) == 200:
			print("API success")
		else:
			print("API failed please check")
			error.raised("3","API failed")
	except Exception as e:
		print(str(e))
		print("error in event_call function")
		error.raised("3",str(e))


def timer(algo,flag,cam):
	try:
		global Pvideo,Mvideo,Dvideo,Ppath,Dpath,Mpath,Pfp_time,Mfp_time,Dfp_time,Prectify,Drectify,Mrectify,Pback,Mback,Dback,vid_path,Ptimer,Pdetect,Palert_frame,Palert_time,Pcheck,Pst_time,Ptrigger, Dtimer,Ddetect,Dcheck,Dst_time,Dtrigger,Dalert_frame,Dalert_time,Mtimer,Mdetect,Mcheck,Mst_time,Mtrigger,Malert_frame,Malert_time
		if algo == "person" :
			Pflag = flag
			if Pflag == True:
				#print("person pflag",Pflag,Ptimer,Pdetect, Palert_frame)
				Pcheck = 0
				Pdetect = Pdetect +1
				if Ptimer != 0 and  Pdetect > Palert_frame:
					if Ptimer ==1:
						Ptimer=0
						if Mtimer ==1:
							Mtimer=0
						if Dtimer==1:
							Dtimer=0
					if Ptimer == 2 and Pback ==0:
						Prectify =datetime.now()
						#Ptimer=0
						Pback =1
						#print("AFter Ptimer2",Pdetect, Ptimer)
					if Pback == 1 and datetime.now() > Prectify + timedelta(seconds=Roi_rectify):
						with open(event_file,'w') as efile:
							efile.write("EVENT21_OFF :: "+ datetime.now().strftime("%Y_%m_%dT%H-%M-%S"))
						event_call("EVENT21_OFF",None,None)
						current_time = datetime.now()
						current_time = str(current_time)[10:]
						print("*********  Rectification!!! Person in ROI  ******* Time : " , current_time)
						Ptimer=0
			else:
				print("ptimer",Ptimer,Pcheck,Pdetect, Palert_frame)
				if Pcheck == 0 and Ptimer == 0:
					Pst_time =datetime.now()
					Pcheck = 1
				if datetime.now() > Pst_time + timedelta(seconds=3) and Ptimer == 0 and Pcheck == 1:
					Pflag = False
					if Mtimer == 1:
						Mtimer =0
					if Dtimer == 1:
						Dtimer =0
					Ptimer=1
					Pback=0
					video_trigger(cam,"EVENT21_ON")
					Pdetect=0
					Ptrigger=datetime.now()
					Pfp_time=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********** Person Timer Started ******* Time : ", current_time)

				elif Ptimer ==1 and Pdetect <= Palert_frame and datetime.now() > Ptrigger + timedelta(seconds=Palert_time):
					with open(event_file,'w') as efile:
						#efile.write("EVENT21_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT21_ON :: "+ datetime.now().strftime("%Y_%m_%dT%H-%M-%S"))
					event_call("EVENT21_ON",Pvideo,Ppath)
					Pfp_time=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********  ALERT!!! Person not in ROI  ******* Time : " , current_time)
					Ptimer = 2
					Dtimer,Mtimer = 0,0

				elif Ptimer != 0 and datetime.now() > Pfp_time + timedelta(seconds=15):
					Pdetect=0
					Pfp_time=datetime.now()

		if algo == "direction":
			Dflag = flag
			if Dflag ==True:
				Dcheck = 0
				Ddetect = Ddetect +1
				
				if Dtimer != 0 and Ddetect > Dalert_frame:
					if Dtimer ==1:
						Dtimer=0
						if Mtimer ==1:
							Mtimer=0
					elif Dtimer == 2 and Dback==0:
						Dback=1
						Drectify=datetime.now()
						#Dtimer=0
					elif Dback ==1 and datetime.now() > Drectify +timedelta(seconds=attentive_rectify):
						with open(event_file,'w') as efile:
							efile.write("EVENT22_OFF :: "+ datetime.now().strftime("%Y_%m_%dT%H-%M-%S"))		
						event_call("EVENT22_OFF",None,None)
						current_time = datetime.now()
						current_time = str(current_time)[10:]
						print("*********  Rectification!!! Person is attentive  ******* Time : " , current_time)
						Dtimer = 0
				print("Ddetect - {} , Dflag - {}, dtimer -{}".format(Ddetect,Dflag,Dtimer))
			else:
				if Dcheck == 0 and Dtimer == 0:
					Dst_time =datetime.now()
					Dcheck = 1
				if datetime.now() > Dst_time + timedelta(seconds=3) and Dtimer == 0 and Dcheck == 1:
					Dflag = False
					if Mtimer == 1:
						Mtimer=0
					Dtimer=1
					Dback=0
					video_trigger(cam,"EVENT22_ON")
					Ddetect=0
					Dtrigger=datetime.now()
					Dfp_time=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********** Direction Timer Started ***** Time : ", current_time)

				elif Dtimer ==1 and Ddetect <= Dalert_frame and datetime.now() > Dtrigger + timedelta(seconds=Dalert_time):
					with open(event_file,'w') as efile:
						#efile.write("EVENT22_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT22_ON :: "+ datetime.now().strftime("%Y_%m_%dT%H-%M-%S"))
					event_call("EVENT22_ON",Dvideo,Dpath)
					Dfp_time=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********  ALERT!!!   not looking in that direction ***** Time : ", current_time)
					Dtimer = 2
					Mtimer = 0

				elif Dtimer != 0 and datetime.now() > Dfp_time + timedelta(seconds=15):
					Ddetect=0
					Dfp_time = datetime.now()
					print("else Ddetect - {} , Dflag - {}, dtimer -{}".format(Ddetect,Dflag,Dtimer))


		if algo == "motion":
			Mflag = flag
			if Mflag == True:
				Mcheck = 0
				Mdetect = Mdetect +1
				
				if Mtimer != 0 and Mdetect > Malert_frame:
					if Mtimer == 1:
						Mtimer=0
					elif Mtimer == 2 and Mback==0:
						Mback =1
						Mrectify=datetime.now()
						#Mtimer=0
					elif Mback ==1 and datetime.now() > Mrectify +timedelta(seconds=4):
						with open(event_file,'w') as efile:
							efile.write("EVENT23_OFF :: "+ datetime.now().strftime("%Y_%m_%dT%H-%M-%S"))			
						event_call("EVENT23_OFF",None,None)
						current_time = datetime.now()
						current_time = str(current_time)[10:]
						print("*********  Rectification!!! Person is attentive  ******* Time : " , current_time)
						Mtimer = 0
			else:
				if Mcheck == 0 and Mtimer == 0:
					Mst_time =datetime.now()
					Mcheck = 1
				if datetime.now() > Mst_time + timedelta(seconds=3) and Mtimer == 0 and Mcheck == 1:
					Mflag = False
					Mtimer=1
					Mback=0
					video_trigger(cam,"EVENT23_ON")
					Mdetect=0
					Mtrigger=datetime.now()
					Mfp_time=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********** Motion Timer Started *** Time : ", current_time)

				elif Mtimer ==1 and Mdetect <= Malert_frame and datetime.now() > Mtrigger + timedelta(seconds=Malert_time):
					with open(event_file,'w') as efile:
						#efile.write("EVENT23_OFF",(datetime.now()).strftime("%Y_%m_%dT%H-%M-%S"))
						efile.write("EVENT23_ON :: "+ datetime.now().strftime("%Y_%m_%dT%H-%M-%S"))
					event_call("EVENT23_ON",Mvideo,Mpath)
					Mfp_time=datetime.now()
					current_time = datetime.now()
					current_time = str(current_time)[10:]
					print("*********  ALERT!!!   Motion is not detected *** Time :", current_time)
					Mtimer = 2
				elif Mtimer != 0 and datetime.now() > Mfp_time + timedelta(seconds=15):
					Mdetect=0
					Mfp_time=datetime.now()

	except Exception as e:
		print (str(e),"error in timer")
		error.raised("7",str(e))

def video_trigger(cam,event):
	global video_flag
	try:
		start_video(event)
		time.sleep(1)
		if video_flag == 0:
			video=Thread(target=video_function,args=(event,cam))
			video.start()
			video_flag =1

	except Exception as e:
		print (str(e),"error in timer")
		error.raised("7",str(e))

def reset():
	global Ptimer,Mtimer,Dtimer
	print("Resetting timers in reset")
	with open(event_file, 'w') as efile:
		efile.write("EVENT_ALL_OFF ::"+ datetime.now().strftime("%Y_%m_%dT%H-%M-%S"))
		event_call("Reset",None,None)
	Ptimer,Dtimer,Mtimer=0,0,0



