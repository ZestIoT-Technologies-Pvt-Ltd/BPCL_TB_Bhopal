'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the propersonty of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Coordinates and Scores of personsons whose motion is to be detected, number of personsons viewing in required direction
Output: Number of personsons who are in motion
Requirements:
This function shall personform the following:
1)For each personson it will identify whether the personson is in motion or not by considering the below key point coordinates, scores.
  keypoints are nose,left ear,right ear,left wrist,right wrist
2)Returns the number of personsons who are in motion
'''    

import numpy as np

frame_count=[0,0,0,0,0] # To check whether it is first frame of person or not
'''
frame_count: This variable shall be initialised with list of 5 zeros and it is used for checking the person in current frame is also in previous frame
'''
previous_coords = np.zeros([5,5,2], dtype = int) # Storing first frame value of maximum 5 person
'''
previous_coords: This variable shall be initialised with an array of size 5*5*2 with zero values,size represents 5-persons*5-landmarks*2-coordinates. It is used to store coordinate values of persons in previous frame.
'''  
frames_difference= np.zeros([5,8,5], dtype = int)  # TO store 8 frames value of maximum 5
'''
frames_difference: This variable shall be initialised with an array of size 5*8*5 with zero values,size represents 5-persons*8-frames*5-landmarks. It is used to store the difference values of coordinates between current frame and previous frame up to past 8 frames.
'''  
count_check = [0,0,0,0,0]
'''
count_check:  This variable shall be initialised with list of 5 zeros, It is used to find whether a person difference values of coordinates are stored up to last 7 frames, so that we can check for motion detection.
'''
frame_id=[0,0,0,0,0]
'''
frame_id: This variable shall be initialised with list of 5 zeros and it is used as index for storing absolute difference values between frames in frames_difference.
'''

def motion(motion_coords,motion_scores,view):
    global frame_count
    global previous_coords
    global frames_difference
    global frame_id
    global count_check
    #Mot_person = [0]*view
    number_motion=0
    for person in range(0,view):
        present_coords = []
        #for body_point in [0,5,6,9,10]:
        for body_point in [0,3,4,9,10]:
            landmark_coords=[0,0]
            if (body_point > 8 and body_point < 11) and round(motion_scores[person][body_point],1) >= 0.2:
                
                landmark_coords[0]=round(motion_coords[person][body_point][0],1)
                landmark_coords[1]=round(motion_coords[person][body_point][1],1)
            
            elif (body_point < 8 or body_point > 11) and round(motion_scores[person][body_point],1) >= 0.1:
                landmark_coords[0]=round(motion_coords[person][body_point][0],1)
                landmark_coords[1]=round(motion_coords[person][body_point][1],1)
                
            else:
                landmark_coords[0] = -1#if landmark score is lessthan 0.1 we assign -1 to x and y coordinate of that landmark stating we donot consider that landmark for motion detection
                landmark_coords[1] = -1
            present_coords.append(landmark_coords)
        if frame_count[person] == 1:
            absolute_difference = [0,0,0,0,0]
            for i in range(0,5):
                if present_coords[i][0] == -1 or previous_coords[person][i][0] == -1:
                    absolute_difference[i]=-1       # if present or previous coordinates of landmark is -1 then we assign absolute difference to -1
                else :
                    x = int(abs(present_coords[i][0] - previous_coords[person][i][0])) # calculating x-coordinate frames_difference of two frames
                    y = int(abs(present_coords[i][1] - previous_coords[person][i][1])) # calculating y-coordinate frames_difference of two frames
                    if x > y :     # if x-coordinate frames_difference is larger then take x-coordinate
                        absolute_difference[i]=x
                    else:
                        absolute_difference[i]=y   # else take y-coordinate frames_difference value
            print(absolute_difference)
            frame_value = frame_id[person]      # getting the frame_id of person to store absolute difference values in frames_difference
            frames_difference[person][frame_value]=absolute_difference
            frame_value=frame_value+1
            #if frame_value is 8 we set count_check for that person to 1 and reset frame_value to 0
            if frame_value == 8:
                count_check[person] = 1
                frame_value = 0
            frame_id[person]=frame_value
            previous_coords[person][0]=present_coords[0]   # storing current frame value previous_coords
            previous_coords[person][1]=present_coords[1]
            previous_coords[person][2]=present_coords[2]
            previous_coords[person][3]=present_coords[3]
            previous_coords[person][4]=present_coords[4]
            if count_check[person] == 1:
                for j in range(0,5): # checking five body points
                    number_frames_difference=0
                    if j == 1 or j == 2: # for ear landmarks we set threshold to 7
                        pix_frames_difference = 7
                    elif j == 3 or j == 4: # for wrist landmarks we set threshold to 10
                        pix_frames_difference = 10
                    else: # for nose landmark we set threshold to 7
                        pix_frames_difference = 7
    
                    for k in range(0,8): # checking 8 frames values in frames_difference
                        if frames_difference[person][k][j] >= pix_frames_difference: # checking whether frames_difference values of landmarks are greater than or equal to respective threshold values
                            number_frames_difference = number_frames_difference+1
                        if number_frames_difference > 2 :         # if the difference of any landmarks exceeds its threshold 3 times in its previous 8 frames, we can say person is in motion
                            #Mot_person[person]=1
                            number_motion=number_motion+1
                            break;
                    else :
                        continue
                    break


        else:
            frame_count[person]=1
            previous_coords[person][0]=present_coords[0] # updating for first frame
            previous_coords[person][1]=present_coords[1]
            previous_coords[person][2]=present_coords[2]
            previous_coords[person][3]=present_coords[3]
            previous_coords[person][4]=present_coords[4]
        if number_motion ==1:
            break

    return number_motion
