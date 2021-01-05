'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Coordinates and Scores of Persons whose view is to be detected and number of persons in ROI.
Output: Coordinates, Scores and number of Persons who are viewing in required direction.
Requirements:
This function shall perform the following:
1)For each person it will identify does the person is looking in required direction by considering the below key points.
  keypoints are nose,left eye,right eye,left ear,right ear,left shoulder
2)A new list of identified person coordinates and scores viewing in required direction is returned
'''    

def view_detection(view_coords,view_scores,roi):
    #Viw_per = [0]*roi
    number_view = 0
    motion_coords = []
    motion_scores = []
    
    for person in range(0,roi):
        nose_score,left_eye_score, right_eye_score, nose_x, nose_y, left_eye_y, right_eye_y, left_ear_score, right_ear_score = view_scores[person][0],view_scores[person][1],view_scores[person][2], view_coords[person][0][0], view_coords[person][0][1], view_coords[person][1][1], view_coords[person][2][1], view_scores[person][3], view_scores[person][4]
        left_shoulder_x, right_shoulder_x = view_coords[person][5][0], view_coords[person][6][0]
        left_ear_y, right_ear_y = view_coords[person][3][1], view_coords[person][4][1]
        '''if (left_eye_score>=0.1 and right_eye_score>=0.1) :
            if (nose_score > 0.4) and (nose_y < left_eye_y) and (nose_y > right_eye_y) and (left_eye_score>=0.4 and right_eye_score>=0.4) and (left_ear_score>0.1 or right_ear_score>0.1):
                if nose_x+60 > left_shoulder_x and nose_x+60 > right_shoulder_x :
                    motion_coords.append(view_coords[person])
                    motion_scores.append(view_scores[person])
                    #Viw_per[person]=1
                    number_view = number_view+1
                    
            elif (nose_score <= 0.4) :
                motion_coords.append(view_coords[person])
                motion_scores.append(view_scores[person])
                #Viw_per[person]=1
                number_view = number_view+1
                (nose_y < left_eye_y) and (nose_y > right_eye_y) and '''
        
        if (nose_x+38 > left_shoulder_x and nose_x+38 > right_shoulder_x) and (right_eye_y > right_ear_y) and (left_eye_y < left_ear_y) :
                #if nose_x+60 > left_shoulder_x and nose_x+60 > right_shoulder_x :
            motion_coords.append(view_coords[person])
            motion_scores.append(view_scores[person])
            #Viw_per[person]=1
            number_view = number_view+1
        ''' elif (nose_y < left_eye_y) and (nose_y > right_eye_y) and (nose_x+35 > left_shoulder_x and nose_x+35 > right_shoulder_x) and (left_ear_score > 0.35 or right_ear_score > 0.35) and (left_eye_score > 0.7 and right_eye_score > 0.7) :
            motion_coords.append(view_coords[person])
            motion_scores.append(view_scores[person])
            #Viw_per[person]=1
            number_view = number_view+1'''
            
        '''elif (nose_x+10 > left_shoulder_x or nose_x+10 > right_shoulder_x) and (left_ear_score>0.1 and right_ear_score>0.1 and nose_score > 0.1) :
            motion_coords.append(view_coords[person])
            motion_scores.append(view_scores[person])
            #Viw_per[person]=1
            number_view = number_view+1'''
      

    return motion_coords,motion_scores,number_view
