#   Copyright (C) 2020 by ZestIOT. All rights reserved. The information in this 
#   document is the property of ZestIOT. Except as specifically authorized in 
#   writing by ZestIOT, the receiver of this document shall keep the information
#   contained herein confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and disseminations to 
#   the receiver's employees shall only be made on a strict need to know basis.
"""
Input: image from camera, darknet image object, loaded network (darknet object), class_name 
       (darknet object), trck_dict(dictionary with number of cylinders and their respective centroid 
       coordinates),st_dict(number of cylinders in the first frame), count (number of frames),
       cyl(cylinder number), moving(if cylinder is moving then True else False) 

Output: trck_dict(dictionary with number of cylinders and their respective centroid coordinates),
        st_dict(number of cylinders in the first frame), count (number of frames),
        cyl(cylinder number), moving(if cylinder is moving then True else False) 

User Requirement:
1) Detecting if the cylinder are moving or not


Requirements:
1) This function takes the darknet image object, loaded network(darknet object), class name(darknet onject),
   and image from the camera  which is first cropped in Region of inetrest(ROI) and then it is converted to 
   the darknet image object which is passed to the loaded model with class names. The result is the detection 
   of cylinder in each ROI, which basically provides the central coordinates of the bounding box detection of 
   the respective object.
2) Then we need to check if the cylinders are moving or not by the monement of coordinates of the detection over some frames.
3) If there is no movement for certain frames then we know the cylinfers are not moving.
"""


import darknet
import cv2
import error
from datetime import datetime, timedelta
import traceback
import numpy as np
is_first,total_count,count_frame, = 1,0,0
current_dict,prev_dict,current_len,prev_len = {},{},0,0
font = cv2.FONT_HERSHEY_SIMPLEX
line1 = 1100
line2 = 1140
line3 = 1160

def get_input_data(result,img,x_res,y_res):
  list1,cyl,cyl_dict = {},0,{}
  for i,j in enumerate(result):
    if float(j[1]) < 80 :
      continue
    cord=j[2]
    xm=int((cord[0]) * float(x_res/416)) # cent coordinates
    ym=int((cord[1]) * float(y_res/416))
    #xco=int(float(cord[0]-cord[2]/2) * float(x_res/416)) # bounding box coordinates
    #yco=int(float(cord[1]-cord[3]/2) * float(y_res/416))
    #xExt=int(float(cord[2]) * float(x_res/416))
    #yExt=int(float(cord[3]) * float(y_res/416)) 
    #img=cv2.rectangle(img,(xco,yco),(xco+xExt,yco+yExt),(0,0,255),2)
    #img=cv2.rectangle(img,(xm-2,ym-2),(xm+2,ym+2),(0,255,0),2)
  
    if (xm >= line1) and (xm <=line3+15):
      print("xm, ym",xm,ym)
      #state = "Initialized"		
      cyl_dict[cyl]={'xco':xm,'yco':ym,'state':"Initialized"}
      list1.update(cyl_dict)
      cyl=cyl+1
  return list1,cyl

def update_counter():
	global total_count,current_dict,prev_dict
	#global total_count
	#This can be optimized further as there will be single cylinder crossing the line 2 at any instant
	for key in current_dict:
		if current_dict[key]['state'] == 'moving right':
			if current_dict[key]['xco'] > line2 and prev_dict[key]['xco'] <= line2 and prev_dict[key]['state'] != 'counted':
				total_count = total_count + 1
				print("in update_counter",total_count)
				break

def update_list():
	global current_dict,prev_dict
	global prev_len,total_count
	for key in current_dict:
	#Ignoring the crossed line 3 ones here

		if int(current_dict[key]['xco']) > int(prev_dict[key]['xco']): #and int(current_dict[key]['xco']) < 335:
			if(current_dict[key]['xco'] < line3):
				current_dict[key]['state']='moving right'
			else:
				current_dict[key]['state']='counted'

		elif int(current_dict[key]['xco']) == int(prev_dict[key]['xco']):
			current_dict[key]['state']='non moving'
		elif (int(prev_dict[key]['xco']) - int(current_dict[key]['xco']))<20:
			current_dict[key]['xco']=prev_dict[key]['xco']
			current_dict[key]['yco']=prev_dict[key]['yco']
			current_dict[key]['state']='moving left'
		else:
			current_dict[key]['state'] == 'moving right'
			total_count=total_count+1
			break
		


	update_counter()

	print("current_dict",current_dict)
	print("prev_dict",prev_dict)


	for key in current_dict:
		if int(current_dict[key]['xco']) >= line3:
			prev_dict[key]['xco']= line1
		else:
			prev_dict[key]['xco'] = current_dict[key]['xco']
		prev_dict[key]['state'] = current_dict[key]['state']
		prev_dict[key]['yco'] = current_dict[key]['yco']
	prev_len = len(current_dict)

def track(img,darknet_image,network,class_names,moving):
	global total_count,count_frame,current_dict,prev_dict,current_len,prev_len,is_first
	try:
		print (total_count)
		x_res=int(img.shape[1])
		y_res=int(img.shape[0])
		pts = np.array([[855,505],[855,720],[1230,720],[1230,505]])
		mask = np.zeros(img.shape[:2], np.uint8)
		cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
		dst = cv2.bitwise_and(img, img, mask=mask)
		frame_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
		frame_resized = cv2.resize(frame_rgb,(darknet.network_width(network),darknet.network_height(network)),interpolation=cv2.INTER_LINEAR)
		darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
		result=darknet.detect_image(network,class_names,darknet_image, thresh=0.25)
		#print(result)
		
		current_dict,current_len = get_input_data(result,img,x_res,y_res)

		#img = cv2.line(img, (line1,555), (line1,700), (0, 255, 0),2)
		#img = cv2.line(img, (line3,700), (line3,555), (0, 255, 0),2)
		#img = cv2.line(img, (line2,700), (line2,555), (255, 0, 0),2)
		if is_first == 1:
			#current_dict,current_len = update_current_list(input_data,img)
			prev_dict = current_dict
			prev_len  = current_len
			print("in first")
			if (current_len != 0):
				is_first = 0
		else:
			if (prev_len == current_len):
				update_list()
		print("here ->"+str(total_count))
		count_frame = count_frame +1
		if total_count >0:
			moving = True
			count_frame =0
			total_count =0
		if count_frame > 5 and total_count ==0 :
			moving = False
			count_frame = 0
			total_count = 0

		cv2.putText(img, "Moving : "+str(moving), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
		print("moving - > "+str(moving))
		return(img,moving)
	except Exception as e:
		print(str(e))
		traceback.print_exc()
		error.raised("2",str(e))

def move_call():
	global moving
	return moving

