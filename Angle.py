'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.

Input: Coordinates and Scores of Persons whose view angle is to be plotted and input frame
Output: Input frame with conical shape plotted on it
Requirements:
This function shall perform the following:
1)For each person it will identify to which side the person is looking by considering the below key point coordinates, scores and plots a conical shape on the image.
  keypoints are nose,left ear,right ear,left shoulder,right shoulder
2)The input frame is return by plotting conical shape for each person on it.
'''    
import cv2
import math
import numpy as np
def view_angle(motion_coords,motion_scores,view,overlay_image):
    for person in range(0,view):
        Nose_score = motion_scores[person][0]
        if Nose_score <0.5:
            continue
        else :
            Left_ear_score, Right_ear_score, Nose_X_cood, Nose_Y_cood, Left_ear_X, Left_ear_Y, Right_ear_X, Right_ear_Y, Left_shd_X, Left_shd_Y, Right_shd_X, Right_shd_Y = motion_scores[person][3],motion_scores[person][4],motion_coords[person][0][0],motion_coords[person][0][1],motion_coords[person][3][0],motion_coords[person][3][1],motion_coords[person][4][0],motion_coords[person][4][1],motion_coords[person][5][0],motion_coords[person][5][1],motion_coords[person][6][0],motion_coords[person][6][1]
            index=0
            points= [0, 4, 6, 8, 10, 10, 10, 8, 6, 4, 0, 0]
            curve = []
            #calculating the midpoints between ear and shoulder
            mid1 = ((int(Left_ear_Y)+int(Left_shd_Y))//2, (int(Left_ear_X)+int(Left_shd_X))//2)
            mid2 = ((int(Right_ear_Y)+int(Right_shd_Y))//2, (int(Right_ear_X)+int(Right_shd_X))//2)
            #if person looking totally towards left
            if Left_ear_score <0.1 :
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), (int(Nose_Y_cood+150), int(Nose_X_cood-50)), (255, 0, 0), 2)
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), (int(Nose_Y_cood+150), int(Nose_X_cood+50)), (255, 0, 0), 2)
                for y in range(int(Nose_X_cood-50), int(Nose_X_cood+60), 10):
                    new_point = (int(Nose_Y_cood+150)+points[index], y)
                    curve.append(new_point)
                    index= index+1
                overlay_image= cv2.polylines(overlay_image, np.int32([curve]), True, (255, 0, 0), 2)
            #if person looking totally towards right
            elif Right_ear_score <0.1 :
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), (int(Nose_Y_cood-150), int(Nose_X_cood-50)), (255, 0, 0), 2)
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), (int(Nose_Y_cood-150), int(Nose_X_cood+50)), (255, 0, 0), 2)
                for y in range(int(Nose_X_cood-50), int(Nose_X_cood+60), 10):
                    new_point = (int(Nose_Y_cood-150)-points[index], y)
                    curve.append(new_point)
                    index= index+1
                overlay_image= cv2.polylines(overlay_image, np.int32([curve]), True, (255, 0, 0), 2)
            # the below elif conditions will consider ear landmark scores and plot the conical shape pointing towards required region.
            elif Left_ear_score >0.1 and Left_ear_score <0.3 :
                #adding and substracting 100 and 110 to mid[0] rotates the cone to desired side
                mid1 = (mid1[0]+100, mid1[1]+100)
                mid2 = (mid2[0]+110, mid2[1]+100)
                mid = (mid1[1]+mid2[1])/2
                #step value is considered in for loop which helps in drawing the curved line in few cases where we obtain step value as zero in those cases we set it to one.
                step= math.ceil((mid1[0]-mid2[0])/10)
                if step == 0 :
                    step = step+1
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid1, (255, 0, 0), 2)
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid2, (255, 0, 0), 2)
                for y in range(mid2[0], mid1[0]+step, step):
                    new_point = (y, mid+points[index])
                    print(new_point)
                    curve.append(new_point)
                    index= index+1
                overlay_image= cv2.polylines(overlay_image, np.int32([curve]), False, (255, 0, 0), 2)
                
            elif Left_ear_score >0.3 and Left_ear_score <0.5 :
                #adding and substracting 60 and 70 to mid[0] rotates the cone to desired side
                mid1 = (mid1[0]+60, mid1[1]+100)
                mid2 = (mid2[0]+70, mid2[1]+100)
                mid = (mid1[1]+mid2[1])/2
                step= math.ceil((mid1[0]-mid2[0])/10)
                if step == 0 :
                    step = step+1
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid1, (255, 0, 0), 2)
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid2, (255, 0, 0), 2)
                for y in range(mid2[0], mid1[0]+step, step):
                    new_point = (y, mid+points[index])
                    print(new_point)
                    curve.append(new_point)
                    index= index+1
                overlay_image= cv2.polylines(overlay_image, np.int32([curve]), False, (255, 0, 0), 2)
            
            elif Right_ear_score >0.1 and Right_ear_score <0.3 :
                mid1 = (mid1[0]-110, mid1[1]+100)
                mid2 = (mid2[0]-100, mid2[1]+100)
                mid = (mid1[1]+mid2[1])/2
                step= math.ceil((mid1[0]-mid2[0])/10)
                if step == 0 :
                    step = step+1
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid1, (255, 0, 0), 2)
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid2, (255, 0, 0), 2)               
                for y in range(mid2[0], mid1[0]+step, step):
                    new_point = (y, mid+points[index])
                    print(new_point)
                    curve.append(new_point)
                    index= index+1
                overlay_image= cv2.polylines(overlay_image, np.int32([curve]), False, (255, 0, 0), 2)
            
            elif Right_ear_score >0.3 and Right_ear_score <0.5 :
                mid1 = (mid1[0]-70, mid1[1]+100)
                mid2 = (mid2[0]-60, mid2[1]+100)
                mid = (mid1[1]+mid2[1])/2
                step= math.ceil((mid1[0]-mid2[0])/10)
                if step == 0 :
                    step = step+1               
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid1, (255, 0, 0), 2)
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid2, (255, 0, 0), 2)
                for y in range(mid2[0], mid1[0]+step, step):
                    new_point = (y, mid+points[index])
                    print(new_point)
                    curve.append(new_point)
                    index= index+1
                overlay_image= cv2.polylines(overlay_image, np.int32([curve]), False, (255, 0, 0), 2)
             
            elif Right_ear_score >0.5 and Left_ear_score >0.5:
                mid1 = (mid1[0], mid1[1]+100)
                mid2 = (mid2[0], mid2[1]+100)
                mid = (mid1[1]+mid2[1])/2
                step= math.ceil((mid1[0]-mid2[0])/10)
                if step == 0 :
                    step = step+1                
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid1, (255, 0, 0), 2)
                overlay_image = cv2.line(overlay_image, (int(Nose_Y_cood), int(Nose_X_cood)), mid2, (255, 0, 0), 2)
                for y in range(mid2[0], mid1[0]+step, step):
                    new_point = (y, mid+points[index])
                    print(new_point)
                    curve.append(new_point)
                    index= index+1
                overlay_image= cv2.polylines(overlay_image, np.int32([curve]), False, (255, 0, 0), 2)
                    
    return overlay_image

