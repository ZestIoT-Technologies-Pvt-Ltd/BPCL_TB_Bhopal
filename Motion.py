import numpy as np

countt=[0,0,0,0,0] # To check whether it is first frame of person or not
list2 = np.zeros([5,5,2], dtype = int) # Storing first frame value of maximum 10 person
diff= np.zeros([5,8,5], dtype = int)  # TO store 8 frames value of maximum 10
mon = 0
temp1=[0,0,0,0,0,0,0,0,0,0]
def motion(list1,per):
    global countt
    global list2
    global diff
    global temp1
    global mon
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
            if mon == 0:
                mon = 1
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
        if mon == 1:
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
                        return True
                        break;
            if j == 4:
                return False
    else:
        countt[per]=2
        list2[per][0]=list1[0] # updating for first frame
        list2[per][1]=list1[1]
        list2[per][2]=list1[2]
        list2[per][3]=list1[3]
        list2[per][4]=list1[4]
