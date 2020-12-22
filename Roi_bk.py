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
[[ 1.12956964e+00, -2.96722771e+00,  1.12395551e+03],
 [ 1.42265577e+00,  2.55581764e+00, -1.21486532e+03],
 [-3.96099049e-05,  4.73503961e-03,  1.00000000e+00]]
'''
ch_matrix_2mp = np.array([[ 1.12956964e+00, -2.96722771e+00,  1.12395551e+03],
 [ 1.42265577e+00,  2.55581764e+00, -1.21486532e+03],
 [-3.96099049e-05,  4.73503961e-03,  1.00000000e+00]])

def roi_fun(coordinates,scores):
    view_coords = []
    view_scores = []
    number_roi = 0
    for person in range(0,5):
        list_roi=[]
        for body_point in [5,6,7,8,9,10,13,14,15,16]:
            landmark_coords=[0,0]
            if round(scores[person][body_point],1) >= 0.1:
                landmark_coords[0]=round(coordinates[person][body_point][0],1)
                landmark_coords[1]=round(coordinates[person][body_point][1],1)
            else:
                landmark_coords[0] = -1
                landmark_coords[1] = -1
            list_roi.append(landmark_coords)		

        for i in range(9,-1,-1):
            x_coordinate = list_roi[i][1]
            y_coordinate = list_roi[i][0]
            a1 = np.array([[x_coordinate,y_coordinate]],dtype='float32')
              #print("a1--->",a1)
            a1 = np.array([a1])
            output1 = cv2.perspectiveTransform(a1,ch_matrix_2mp)
            if((output1[0][0][0] >= 0.0 and output1[0][0][0] <=400) and (output1[0][0][1] >= 0.0 and output1[0][0][1] <=400)):
                view_coords.append(coordinates[person])
                view_scores.append(scores[person])
                number_roi = number_roi+1
                break
                   
    return view_coords,view_scores,number_roi
