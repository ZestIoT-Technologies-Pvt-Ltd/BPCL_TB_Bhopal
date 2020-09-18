import darknet
import cv2
import error
from datetime import datetime, timedelta
import traceback
import numpy as np
font = cv2.FONT_HERSHEY_SIMPLEX
def track(img,darknet_image,network,class_names,track_dict,st_dict,count,cyl,moving):
	try:
		obj=cyl
		cyl_dict={}
		diff_pixel=20
		x_res=int(img.shape[1])
		y_res=int(img.shape[0])
		pts = np.array([[325,300],[300,620],[980,620],[978,300]])
		mask = np.zeros(img.shape[:2], np.uint8)
		cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
		dst = cv2.bitwise_and(img, img, mask=mask)
		frame_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
		frame_resized = cv2.resize(frame_rgb,(darknet.network_width(network),darknet.network_height(network)),interpolation=cv2.INTER_LINEAR)
		darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
		result=darknet.detect_image(network,class_names,darknet_image, thresh=0.25)
		#print(result)
		for i,j in enumerate(result):
			cord=j[2]
			xm=int((cord[0]) * float(x_res/416)) # cent coordinates
			ym=int((cord[1]) * float(y_res/416))
			if cyl > 0:
				for key in track_dict:
					if abs(xm - int(track_dict[key]['xco'])) < diff_pixel:
						cyl_dict={}
						flag=track_dict[key]["flag"]+1
						cyl_dict[key]={'xco':xm,'yco':ym,'flag':flag}
						break
					else:
						obj= cyl+1
						cyl_dict[obj]={'xco':xm,'yco':ym,'flag':0}

				track_dict.update(cyl_dict)
				cyl=obj
				cyl_dict={}

			if cyl == 0:
				track_dict[cyl]={'xco':xm,'yco':ym,'flag':0}
				cyl=cyl+1
		#print(track_dict,count,st_dict,moving,cyl)
		count=count+1
		if count == 1:
			st_dict=len(track_dict)
		if len(track_dict) > st_dict:
			moving = True
			track_dict={}
			cyl=0
			count=0

		if count > 40 and len(track_dict) == st_dict:
			moving = False
			track_dict={}
			cyl=0
			count = 0
		print(moving)
		cv2.putText(dst, "Moving : "+str(moving), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
		return(moving,dst,track_dict,st_dict,count,cyl)
	except Exception as e:
		print(str(e))
		traceback.print_exc()
		error.raised("2",str(e))
