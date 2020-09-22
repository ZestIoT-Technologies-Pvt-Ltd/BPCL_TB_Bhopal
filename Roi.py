'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Coordinates and Scores of 5 Persons 
Output: Coordinates and Scores of Persons who are in ROI
Requirements:
This function shall perform the following:
1)For each person it will identify the presence of any one of the below key points in ROI
  keypoints are left knee,left ankle, Right ankle, Right knee
2)A new list of identified person coordinates and scores in ROI is returned
'''    
    
import cv2
import numpy as np
'''
Requiremnets: This variable shall be initialised with a 3*3 matrix with below values 
[[-1.01474155e+00,  8.38264757e-01, -1.50711179e+02],
 [-6.61831262e-01, -5.62556573e+00,  3.71618254e+03],
 [ 2.22220176e-04, -3.14094803e-03,  1.00000000e+00]]
'''
ch_matrix = np.array([[-1.01474155e+00,  8.38264757e-01, -1.50711179e+02],
 [-6.61831262e-01, -5.62556573e+00,  3.71618254e+03],
 [ 2.22220176e-04, -3.14094803e-03,  1.00000000e+00]])

def roi_fun(coordinates,scores):
    #ROI_per = [0,0,0,0,0]
    view_coords = []
    view_scores = []
    number_roi = 0
    for person in range(0,5):
   		confdnc = round(scores[person][0],4)
   		if confdnc > 0.1:
   			list_roi=[]
   			for body_point in [13,14,15,16]:
   				ll=[0,0]
   				if round(scores[person][body_point],4) >= 0.1:
   					ll[0]=round(coordinates[person][body_point][0],4)
   					ll[1]=round(coordinates[person][body_point][1],4)
   				else:
   					ll[0] = -1
   					ll[1] = -1
   				list_roi.append(ll)		

   			for ii in range(3,-1,-1):
   				b1 = list_roi[ii][0]
   				b2 = list_roi[ii][1]
   				a1 = np.array([[b1,b2]],dtype='float32')
                #print("a1--->",a1)
   				a1 = np.array([a1])
                #print("a1--below-->",a1)
   				temp = 0
   				output1 = cv2.perspectiveTransform(a1,ch_matrix)
   				if((output1[0][0][0] < 0.0) or (output1[0][0][1] < 0.0) or (output1[0][0][0] > 400.0) or (output1[0][0][1] > 600.0)):
   					temp = 1
   			if ii == 0 and temp == 1:
   				continue
   			else:
   				view_coords.append(coordinates[person])
   				view_scores.append(scores[person])
   				number_roi = number_roi+1
                
    return view_coords,view_scores,number_roi

   				
                