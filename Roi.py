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
[[ 1.82020856e+00 , 1.33171809e+00, -1.06587459e+03],
 [ 1.05003074e-01,  5.11284201e+00, -2.09603906e+03],
 [ 2.62507686e-04 , 4.07903994e-03,  1.00000000e+00]]
'''
ch_matrix_2mp = np.array([[ 1.82020856e+00 , 1.33171809e+00, -1.06587459e+03],
 [ 1.05003074e-01,  5.11284201e+00, -2.09603906e+03],
 [ 2.62507686e-04 , 4.07903994e-03,  1.00000000e+00]])

def roi_fun(coordinates,scores):
    #ROI_per = [0,0,0,0,0]
    view_coords = []
    view_scores = []
    number_roi = 0
    for person in range(0,5):
        list_roi=[]
        for body_point in [5,6,13,14,15,16]:
            landmark_coords=[0,0]
            if round(scores[person][body_point],1) >= 0.1:
                landmark_coords[0]=round(coordinates[person][body_point][0],1)
                landmark_coords[1]=round(coordinates[person][body_point][1],1)
            else:
                landmark_coords[0] = -1
                landmark_coords[1] = -1
            list_roi.append(landmark_coords)		

        for i in range(5,-1,-1):
            x_coordinate = list_roi[i][1]
            y_coordinate = list_roi[i][0]
            a1 = np.array([[x_coordinate,y_coordinate]],dtype='float32')
              #print("a1--->",a1)
            a1 = np.array([a1])
              #print("a1--below-->",a1)
 				#temp = 0
            output1 = cv2.perspectiveTransform(a1,ch_matrix_2mp)
            if((output1[0][0][0] >= 0.0 and output1[0][0][0] <=400) and (output1[0][0][1] >= 0.0 and output1[0][0][1] <=400)):
 			#if((output1[0][0][0] < 0.0) or (output1[0][0][1] < 0.0) or (output1[0][0][0] > 400.0) or (output1[0][0][1] > 400.0)):       
 					#temp = 1
 					#ROI_per[person] = 1
                view_coords.append(coordinates[person])
                view_scores.append(scores[person])
                number_roi = number_roi+1
                break
                   
    return view_coords,view_scores,number_roi