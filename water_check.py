import cv2
from datetime import datetime,timedelta
from sockets import ClientSocket
import numpy as np
import error
import os
wat_check =0
water_path="/media/smartcow/SD/video_storage/"
def water_quality(img1):
	global wat_check
	im = img1[530:561,383:415]
	im1 = cv2.rectangle(img1,(383,530),(415,561),(255,0,0),2)
	img_dir=(datetime.now()).strftime("%Y_%m_%d")
	water_loc=water_path+img_dir+"/"
	if not os.path.isdir(water_loc):
		#print("make directory")
		os.mkdir(water_loc)
	img_name=datetime.now().strftime("%H%M%S")+".jpg"
	cv2.imwrite(water_loc+img_name,im1)
	sum_row = np.sum(im,axis = 0)
	sum_col = np.sum(sum_row,axis = 0)
	sum_total = sum_col[0] + sum_col[1] + sum_col[2]
	blue = sum_col[0]
	green = sum_col[1]
	red = sum_col[2]
	print("Red -> {}   Green -> {}   Blue -> {} ".format(red,green,blue))
	if int(red) > 70000 and int(green) > 70000 and int(blue) > 100000:
		wat_check=wat_check +1
	if wat_check > 5:
		print("***************************** Water Quality not good ***************************")
		try:
			sc=ClientSocket(device_id=str('BPCL_SUR_NX_0001'))
			logdate=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
			data={'event_time':logdate,'event_description':"Water Quality Not Good"}
			sc.send(time_stamp=logdate, message_type="EVENT1_ON", data=data)
			msg = sc.receive()
			print(msg)
			wat_check =0
			if int(msg["data"]["status"]) == 200:
				print("API success")
			else:
				print("API failed please check")
				error.raised("3","API failed")
		except Exception as e:
			print("error in event_call function")
			error.raised("3",str(e))

