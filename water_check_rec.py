import cv2
import shutil
from datetime import datetime,timedelta
from sockets import ClientSocket
import numpy as np
import error
import os
wat_check =0
wat_rectify =0
wat_quality =0
water_path="/media/smartcow/LFS/video_storage/"
water_temp="/media/smartcow/LFS/temp_video_storage/"
def water_quality(img1):
	global wat_check
	global wat_quality
	global wat_rectify
	im = img1[580:611,383:415]
	im1 = cv2.rectangle(img1,(383,580),(415,580),(255,0,0),2)
	img_name=datetime.now().strftime("%H%M%S")+".jpg"
	#cv2.imwrite(water_temp+img_name,im1)
	sum_row = np.sum(im,axis = 0)
	sum_col = np.sum(sum_row,axis = 0)
	sum_total = sum_col[0] + sum_col[1] + sum_col[2]
	blue = sum_col[0]
	green = sum_col[1]
	red = sum_col[2]
	string = "R :"+ str(red)+" G : "+ str(green)+" B : "+str(blue)
	#im1 = cv2.putText(im1, string, (20,100), cv2.FONT_HERSHEY_SIMPLEX , 1,  (255, 0, 255) , 2, cv2.LINE_AA)
	cv2.imwrite(water_temp+img_name,im1)
	print("Red -> {}   Green -> {}   Blue -> {} ".format(red,green,blue))
	if wat_quality == 0 :
		if int(red) > 105000 and int(green) > 105000 and int(blue) > 140000 :
			print("******************* Warning ********************")
			wat_check=wat_check +1


		if wat_check > 4:
			img_dir=(datetime.now()).strftime("%Y_%m_%d")
			wat_quality =1
			wat_path = water_path+img_dir+"/BHOPAL_EVENT1_ON_"+img_name
			shutil.move(water_temp+img_name,wat_path)
			print("***************************** Water Quality not good ***************************")
			try:
				sc=ClientSocket(device_id=str('BPCL_BPL_NX_0001'))
				logdate=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
				data={'event_time':logdate,'path':wat_path,'event_description':"Water Quality Not Good"}
				sc.send(time_stamp=logdate, message_type="EVENT1_ON", data=data)
				msg = sc.receive()
				print(msg)
				wat_check =0
				if int(msg["data"]["status"]) == 200:
					print("API success")
				else:
					print("API failed please check")
					error.raised(516,"Error in water function")
			except Exception as e:
				print("error in event_call function")
				error.raised(8,"Error in API")

	if wat_quality ==1:
		if int(red) < 65000 and int(green) < 65000 and int(blue) < 85000 :
			wat_rectify=wat_rectify+1
			print("********************* Restored *******************")
		if wat_rectify >4 :
			wat_quality =0
			img_dir=(datetime.now()).strftime("%Y_%m_%d")
			shutil.move(water_temp+img_name,water_path+img_dir+"/BHOPAL_EVENT1_OFF_"+img_name)
			water_rectify()
			wat_rectify=0
			print("***************************** Water Qualit Restored ***************************")

def water_rectify():
	try:
		sc=ClientSocket(device_id=str('BPCL_BPL_NX_0001'))
		logdate=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
		data={'event_time':logdate,'event_description':"Water Quality Restored"}
		sc.send(time_stamp=logdate, message_type="EVENT1_OFF", data=data)
		msg = sc.receive()
		print(msg)
		#wat_rectify =0
		if int(msg["data"]["status"]) == 200:
			print("API success")
		else:
			print("API failed please check")
			error.raised(516,"Error in water function")
	except Exception as e:
		print("error in event_call function")
		error.raised(8,"Error in API")


