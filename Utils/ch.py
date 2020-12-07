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

        file1= open('/media/smartcow/LFS/ch.txt',"a")
        file1.write(str(datetime.now())+"---"+"\tCPU:"+str(CPU)+"\tAO:"+str(AO)+"\tGPU:"+str(GPU_t)+"\tAUX:"+str(AUX)+"\tthermal:"+str(thermal)+"\n")
        file1.close()
except Exception as e:
    print ("exception")

