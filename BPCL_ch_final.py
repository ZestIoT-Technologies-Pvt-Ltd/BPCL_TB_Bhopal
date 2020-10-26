'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: The model takes input from two cameras, one camera is used to find whether the cylinder bed is moving or not and the other one is used to find person attentiveness
Output: The model sends the alarm values to the timer function based on person attentiveness
Requirements:
This function shall perform the following:
1)This function calls the track method passing the input feed of camera located over the cylinder bed, the track function returns whether the cylinder bed is moving or not.
2)If the cylinder bed is moving, the input feed of camera contains the person who needs to look after the cylinders is sent to posenet model.
3)From posenet model the person pose is estimated and the person landmark coordinates and their respective scores are returned.
4)The roi_fun returns the coordinates of persons who are in ROI,those coordinates are sent to view_detection and the method returns the coordinates of persons who are viewing in required direction.
5)The view_angle method plots the conical shape stating which side they were looking and the coordinates are passed to motion function which return whether the person whos is in ROI and viewing in required direction is in motion or not.
6)Based on the output of the ROI,view,motion methods the respective flags are sent to timer function.
7)The Diagnostics methods finds the devices are in proper working condition or not.
'''
import cv2
from queue import Queue
import traceback
import numpy as np
from threading import Thread
import os
import json
import time
from datetime import datetime,timedelta
import tensorflow as tf
import Roi1 as Roi
import Motion
import View
import posenet
#import RTSP
import tracker_model
import XY_frame as XY_track
import Timer_single_1 as Timer
#import Angle
import error
import Health_Api
import screening2
import screening1

screening1.create()
screening2.create()
screening1.connect()
screening2.connect()
config="/home/smartcow/BPCL/BPCL_final/BPCL_config.json"
with open(config) as json_data:
	info=json.load(json_data)
	cam1,cam2= info["camera1"],info["camera2"]
# initializing tracker variables
count,prev_moving,moving,track_dict,st_dict,cyl = 0,False, False, {},0,0

def Diagnostics():
	try:
		print("Inside Diagnostics function")
		Health_Api.apicall()
	except Exception as e:
		print(str(e))
		error("6",str(e))

class camera():

	def __init__(self, src=0):
		# Create a VideoCapture object
		self.capture = cv2.VideoCapture(src)

		# Take screenshot every x seconds
		self.screenshot_interval = 1

		# Default resolutions of the frame are obtained (system dependent)
		self.frame_width = int(self.capture.get(3))
		self.frame_height = int(self.capture.get(4))

		# Start the thread to read frames from the video stream
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()

	def update(self):
		# Read the next frame from the stream in a different thread
		while True:
			if self.capture.isOpened():
				(self.status, self.frame) = self.capture.read()

	def get_frame(self):
		# Display frames in main program
		if self.status:
			self.frame = cv2.resize(self.frame, (1280,720))
			return self.frame

if __name__ == '__main__':
	try:
		#cam = cv2.VideoCapture("/media/smartcow/LFS/temp/20201010183402.mp4")
		sess=tf.compat.v1.Session()
		model_cfg, model_outputs = posenet.load_model(101, sess)
		output_stride = model_cfg['output_stride']
		darknet_image_T,network_T,class_names_T=tracker_model.load_model()
		Timer.reset()
		print("Tracker model loaded")
		cam1 = camera(cam1)
		time.sleep(1)
		cam2 = camera(cam2)
		time.sleep(1)
		ht_time=datetime.now()
		#kk = 0
		while True:
			loop_start_time = datetime.now()
			#print("loop start",loop_start_time)
			img1 = cam1.get_frame()
			img1 = cv2.resize(img1,(1280,720))
			img2 = cam2.get_frame()
			img2 = cv2.resize(img2,(1280,720))
			#ret,img1 = cam.read()
			moving,img2,track_dict,st_dict,count,cyl = XY_track.track(img2,darknet_image_T,network_T,class_names_T,track_dict,st_dict,count,cyl,moving)
			#moving =True
			if moving == True:
				input_image, draw_image, output_scale = posenet.read_imgfile(img1, scale_factor=0.7125, output_stride=output_stride)
				heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(model_outputs,feed_dict={'image:0': input_image})
				pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
					heatmaps_result.squeeze(axis=0),
					offsets_result.squeeze(axis=0),
					displacement_fwd_result.squeeze(axis=0),
					displacement_bwd_result.squeeze(axis=0),
					output_stride=output_stride,
					max_pose_detections=5,
					min_pose_score=0.2)
				keypoint_coords *= output_scale
                
				view_coords,view_scores,number_roi=Roi.roi_fun(keypoint_coords,keypoint_scores)
				motion_coords,motion_scores,number_view=View.view_detection(view_coords,view_scores,number_roi)
				#img1 = Angle.view_angle(motion_coords,motion_scores,number_view,img1)
				number_motion=Motion.motion(motion_coords,motion_scores,number_view)
                
				if number_roi >= 1:
					Timer.timer("person",True,cam1)
					Roi_draw =  True
				if number_roi == 0:
					Timer.timer("person",False,cam1)
					Roi_draw = False
				if number_roi >= 1 and number_view >= 1:
					Timer.timer("direction",True,cam1)
					View_draw =  True
				if number_roi >= 1 and number_view == 0:
					Timer.timer("direction",False,cam1)
					View_draw =  False
				if number_roi >= 1 and number_view >= 1 and number_motion == 1:
					Timer.timer("motion",True,cam1)
					Motion_draw = True
				if number_roi >= 1 and number_view >=  1 and number_motion == 0:
					Timer.timer("motion", False,cam1)
					Motion_draw = False
				img1 = cv2.putText(img1, "Person in ROI: True" , (20,70), cv2.FONT_HERSHEY_SIMPLEX , 1,  (255, 0, 0) , 2, cv2.LINE_AA)
				if number_view >= 1 and number_motion ==1:
					img1 = cv2.putText(img1, "Person Attentiveness: True" , (20,120), cv2.FONT_HERSHEY_SIMPLEX , 1,  (255, 0, 0) , 2, cv2.LINE_AA)
				else:
					img1 = cv2.putText(img1, "Person Attentiveness: False" , (20,120), cv2.FONT_HERSHEY_SIMPLEX , 1,  (255, 0, 0) , 2, cv2.LINE_AA)
				
				'''Roi_draw = " Person in ROI " + str(number_roi)
				View_draw = " Person View " + str(number_view)
				Motion_draw = " Person Motion " + str(number_motion)
				current_time = datetime.now()
				current_time = str(current_time)[10:]
				print(current_time)
				img1 = posenet.draw_skel_and_kp(
					img1, pose_scores, keypoint_scores, keypoint_coords,
					min_pose_score=0.1, min_part_score=0.1)
				
				
				pts = np.array([[103,418],[412,240],[951,373],[807,686]], np.int32)
				pts = pts.reshape((-1,1,2))
				cv2.polylines(img1,[pts],True,(0,255,255))
				overlay_image = cv2.putText(img1, Roi_draw , (20,70), cv2.FONT_HERSHEY_SIMPLEX , 1,  (255, 0, 0) , 2, cv2.LINE_AA)
				overlay_image = cv2.putText(img1, View_draw , (20,120), cv2.FONT_HERSHEY_SIMPLEX , 1,  (255, 0, 0) , 2, cv2.LINE_AA)
				overlay_image = cv2.putText(img1, Motion_draw , (20,170), cv2.FONT_HERSHEY_SIMPLEX , 1,  (255, 0, 0) , 2, cv2.LINE_AA)
				
				path = "/media/smartcow/LFS/output/"
				path = path + str(kk) + ".jpg"
				cv2.imwrite(path,img2)
				kk = kk + 1
				
				overlay_image = cv2.resize(overlay_image,(640,480))
				#check1.screening(overlay_image)
				#check2.screening(img2) 
				cv2.imshow("frame",overlay_image)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break'''
			elif moving == False and prev_moving == True:
				Timer.reset()
			if ht_time < datetime.now():
				health = Thread(target=Diagnostics,args=())
				health.start()
				ht_time=datetime.now()+timedelta(minutes=5)
			screening1.screening(img1)
			screening2.screening(img2)
			tf.keras.backend.clear_session()
			loop_end_time = datetime.now()
			while(int((loop_end_time - loop_start_time).total_seconds()*1000) < 300 ):
				loop_end_time = datetime.now()
				#print("inside while loop")
			#print("end_time",loop_end_time)
			#print(str(datetime.now()))
			prev_moving == moving
	except Exception as e:
		print(str(e))
		traceback.print_exc()
		error.raised("1",str(e))
