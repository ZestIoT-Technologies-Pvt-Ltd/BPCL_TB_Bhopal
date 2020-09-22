'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Coordinates and Scores of Persons whose motion is to be detected, number of persons viewing in required direction
Output: Number of persons who are in motion
Requirements:
This function shall perform the following:
1)For each person it will identify whether the person is in motion or not by considering the below key point coordinates, scores.
  keypoints are nose,left shoulder,right shoulder,left wrist,right wrist
2)Returns the number of persons who are in motion
'''    

import numpy as np
'''
Requirements:
countt:This variable shall be initialised with list of 5 zeros and it is used for checking the preson in current frame is also in previous frame
list2: This variable shall be initialised with an array of size 5*5*2 with zero values, It is used to store coordinate values of persons in previous frame.
diff: This variable shall be initialised with an array of size 5*8*5 with zero values, It is used to store the absolute difference values of coordinates between current frame and previous frame.
count_check: This variable shall be initialised with zero, It is used to find whether a person coordinates are read in previous 7 frames.
temp1: This variable shall be initialised with list of 10 zeros and it is used as count for a person present in how many previous frames.
'''
countt=[0,0,0,0,0] # To check whether it is first frame of person or not
list2 = np.zeros([5,5,2], dtype = int) # Storing first frame value of maximum 5 person
diff= np.zeros([5,8,5], dtype = int)  # TO store 8 frames value of maximum 5
count_check = 0
temp1=[0,0,0,0,0,0,0,0,0,0]
def motion(motion_coords,motion_scores,view):
    global countt
    global list2
    global diff
    global temp1
    global count_check
    #Mot_per = [0]*view
    number_motion=0
    for per in range(0,view):
        list1 = []
        for body_point in [0,5,6,9,10]:
            ll=[0,0]
            if round(motion_scores[per][body_point],4) >= 0.1:
                ll[0]=round(motion_coords[per][body_point][0],4)
                ll[1]=round(motion_coords[per][body_point][1],4)
            else:
                ll[0] = -1
                ll[1] = -1
            list1.append(ll)
        if countt[per] == 2:
            t1 = [0,0,0,0,0]
            for i in range(0,5):
                if list1[i][0] == -1 or list1[i][1] == -1 or list2[per][i][0] == -1 or list2[per][i][1] == -1:
                    t1[i]=-1       # checking value with less than 0.1 threshold or not if value is -1 then it is less than 0.1 threshold value
                else:
                    a = int(abs(list1[i][0] - list2[per][i][0])) # calculating x-coordinate differenece of two frames
                    b = int(abs(list1[i][1] - list2[per][i][1])) # calculating y-coordinate differernce of two frames
                    if a > b :     # if x-coordinate difference is larger then take x-coordinate
                        t1[i]=a
                    else:
                        t1[i]=b   # else take y-coordinate difference value
            temp = temp1[per]      # getting last frame updated value
            diff[per][temp]=t1
            if temp < 8:           # if last frame updated value is less than 8 increament temp value
                temp=temp+1
                if count_check == 0:
                    count_check = 1
            if temp == 8:  
                temp = 0
            #print("diff-->",diff[per])
            temp1[per]=temp
            #print("tempppp-->",temp)
            list2[per][0]=list1[0]   # storing current frame value of next time use
            list2[per][1]=list1[1]
            list2[per][2]=list1[2]
            list2[per][3]=list1[3]
            list2[per][4]=list1[4]
            if count_check == 1:
                for j in range(0,5): # checking five body points
                    mm=0
                    if j == 1 or j == 2:
                        pix_diff = 9
                    elif j == 3 or j == 4:
                        pix_diff = 11
                    else:
                        pix_diff = 7
    
                    for k in range(0,8): # checking 8 frames values
                        if diff[per][k][j] >= pix_diff: # checking whether values are greater than equal to 8 or not
                            mm=mm+1
                        if mm >= 5:         # checking more than 3 frames values are greater  than 8 or not
                            #Mot_per[per]=1
                            number_motion=number_motion+1
                            return number_motion
                            break;

                #if j == 4 and Mot_per[per] !=1:
                    #Mot_per[per]=0
        else:
            countt[per]=2
            list2[per][0]=list1[0] # updating for first frame
            list2[per][1]=list1[1]
            list2[per][2]=list1[2]
            list2[per][3]=list1[3]
            list2[per][4]=list1[4]
    return number_motion