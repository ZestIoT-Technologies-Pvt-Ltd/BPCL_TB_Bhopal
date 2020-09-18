import cv2
import numpy as np

ch_matrix = np.array([[-1.01474155e+00,  8.38264757e-01, -1.50711179e+02],
 [-6.61831262e-01, -5.62556573e+00,  3.71618254e+03],
 [ 2.22220176e-04, -3.14094803e-03,  1.00000000e+00]])

def roi_fun(list_roi):

    for ii in range(3,-1,-1):
        b1 = list_roi[ii][1]
        b2 = list_roi[ii][0]
        a1 = np.array([[b1,b2]],dtype='float32')
        #print("a1--->",a1)
        a1 = np.array([a1])
        #print("a1--below-->",a1)
        temp = 0
        output1 = cv2.perspectiveTransform(a1,ch_matrix)
        if((output1[0][0][0] >= 0.0 and output1[0][0][0] <=400) and (output1[0][0][1] >= 0.0 and output1[0][0][1] <=400)):
#       if((output1[0][0][0] < 0.0) or (output1[0][0][1] < 0.0) or (output1[0][0][0] > 400.0) or (output1[0][0][1] > 400.0)):
            temp = 1
            break
    return temp
