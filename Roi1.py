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
import math
'''
Requiremnets: This variable shall be initialised with a 3*3 matrix with below values 
[[ 7.04134834e-01,  6.14842373e-01, -3.48447245e+02],
 [-3.30547989e-01,  2.65773939e+00, -6.76140920e+02],
 [-1.47967015e-04,  1.84266520e-03,  1.00000000e+00]]
'''

'''
ch_matrix_2mp = np.array([[ 8.96167841e-01,  8.17383855e-01 ,-5.21845428e+02],
 [-2.21941845e-01,  3.37607691e+00 ,-9.97991383e+02],
 [-2.06176120e-05,  2.45455731e-03 , 1.00000000e+00]])

'''
ch_matrix_2mp = np.array([[8.12229855e-01,7.40351107e-01,-4.72689024e+02],
    [-3.08167433e-01,3.82490166e+00,-1.30695621e+03],
    [-1.18111868e-04,2.25375649e-03,1.00000000e+00]])


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

