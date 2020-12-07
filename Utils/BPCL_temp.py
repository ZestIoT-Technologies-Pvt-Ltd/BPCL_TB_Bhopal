'''
#   Copyright (C) 2020 by ZestIOT. All rights reserved. The
#   information in this document is the property of ZestIOT. Except
#   as specifically authorized in writing by ZestIOT, the receiver
#   of this document shall keep the information contained herein
#   confidential and shall protect the same in whole or in part from
#   disclosure and dissemination to third parties. Disclosure and
#   disseminations to the receiver's employees shall only be made on
#   a strict need to know basis.
Input: Takes temperature of different components of the device as Input
Output: Gives if the Temperature of the components is in Critical range or not.
1. The Function checks if the Temperature of different components of the device is not within Critical Temperature or not.
2. If temperature is in  Critical Temperature then we shut off all processes on the device.
3. If temperature of all components is below critical temperature than we let the processes run or start if not already runnning.'''

from subprocess import Popen, PIPE
import time
from datetime import datetime

try:
        tegra=Popen(['/home/smartcow/tegrastats'],stdout=PIPE)
        time.sleep(7)
        tegra.kill()
        high_temp=70
        low_temp=65
        temp_check = 0
        info=(tegra.communicate()[0]).decode('ascii')
        info=(info.split("\n")[-2]).split(" ")
        #print(info)
        CPU=int(float(info[18].split("@")[-1][:-1]))
        AO=int(float(info[14].split("@")[-1][:-1]))
        GPU_t=int(float(info[15].split("@")[-1][:-1]))
        AUX=int(float(info[17].split("@")[-1][:-1]))
        thermal=int(float(info[19].split("@")[-1][:-1]))
        if CPU >= high_temp or AUX >= high_temp or AO >= high_temp or GPU_t>= high_temp or thermal >= high_temp:
                temp_check=1
        if CPU <= low_temp and AO <= low_temp and AUX <= low_temp and thermal <= low_temp and GPU_t <= low_temp:
                temp_check =0

        file1= open('/media/smartcow/LFS/ch.txt',"a")
        file1.write(str(datetime.now())+"---"+"\tCPU:"+str(CPU)+"\tAO:"+str(AO)+"\tGPU:"+str(GPU_t)+"\tAUX:"+str(AUX)+"\tthermal:"+str(thermal)+"\n")
        file1.close()

        print (temp_check)

except Exception as e:
        print (1)

