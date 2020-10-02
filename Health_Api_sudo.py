import time
from sockets import ClientSocket
from pynng import Timeout
from datetime import datetime, timedelta
from subprocess import Popen, PIPE
import error
"""
Input: error_file,event file
Output: returns Devices Health information including RAM, CPU usage, GPU usage , Temperature of various components, Last error and event ocurred,disk space, external memory, Device uptime and last reboot time.

User Requirements:
1) Send Health information of the Edge device to Pi

Requirements
1) This function reads the last error ocurred and event ocurred from the file.
2) runs tegrastats to capture RAM, CPU/GPU usage and Temperature of various components.
3) captures the Disk space used, left and external memory if the sd card is mounted
4) captures last rebbot time and device uptime.
5) Sends all the information to Pi using sockets.
"""
error_file="/home/smartcow/BPCL/BPCL_final/error_code.txt"
last_event="/home/smartcow/BPCL/BPCL_final/last_event.txt"
er=0
def health():
        try:
                with open(last_event,'r+') as event:
                        j1=event.readline()
                        #print (j1)
                        j1=j1.split(" :: ")
                        event_code=j1[0]
                        event_time=j1[-1].strip()
                        #print(event_code,event_time)
        except Exception as e:
                print(str(e))
        try:
                with open(error_file,'r+') as f:
                        j= f.readlines()
                        #print(j[0])
                        j = j[0].split(" :: ")
                        error =j[-1]
                        error_algo = j[0]
                        error_time = j[1]
                        #print(" Last Error: {} has occured in {} part of the script at {}".format(error,error_algo,error_time))
        except Exception as e:
                print(str(e))
        tegra=Popen(['/home/smartcow/tegrastats'],stdout=PIPE)
        time.sleep(7)
        tegra.kill()
        info=(tegra.communicate()[0]).decode('ascii')
        #print(info.split("\n"),type(info))
        info=(info.split("\n")[-2]).split(" ")
        #print (info)
        t_RAM= info[1].split("/")[1]
        u_RAM= info[1].split("/")[0]
        cpu=info[9].split(",")
        #print(cpu)
        cpu1,cpu2,cpu3,cpu4,cpu5,cpu6=cpu[0][1:],cpu[1],cpu[2],cpu[3],cpu[4],cpu[5][:-1]
        if 'GR3D_FREQ' in info:
                gpu=info[13]
        else:
                gpu ="run the command with sudo to get GPU readings"
        #print("Percentage used and Frquency of different cores\nGPU: {}\nCPU 1: {}\nCPU 2: {}\nCPU 3: {}\nCPU 4: {}\nCPU 5: {}\nCPU 6: {}\n".format(gpu,cpu1,cpu2,cpu3,cpu4,cpu5,cpu6))
        CPU=info[25].split("@")[-1]
        AO=info[21].split("@")[-1]
        GPU_t=info[22].split("@")[-1]
        AUX=info[24].split("@")[-1]
        #Tboard=info[21].split("@")[-1]
        #Tdiode=info[17].split("@")[-1]
        PMIC=info[23].split("@")[-1]
        thermal=info[26].split("@")[-1]

        # Memory left and usage in percentage
        total_memory=Popen(['df','-BM'],stdout=PIPE)
        avail_memory=Popen(['grep','mmc'],stdin=total_memory.stdout,stdout=PIPE)
        avail_memory=(avail_memory.communicate()[0]).decode('ascii')
        avail_memory=avail_memory.split(" ")
        total_memory=avail_memory[4]
        mem_percentage=avail_memory[12]
        mem_left=avail_memory[10]
        #print (avail_memory[7])
        #memory = avail_memory.split(" ")[-2]
        if len(avail_memory) > 15:
                ext_memory =avail_memory[-2]
        else:
                ext_memory="None"
        #print ("Temperature of different components\nBCPU: {}\nMCPU: {}\nGPU: {}\nPLL: {}\nTboard: {}\nTdiode: {}\nPMIC: {}\nthermal: {}\n".format(BCPU,MCPU,GPU_t,PLL_t,Tboard,Tdiode,PMIC,thermal))
        last_start=Popen(['tuptime','--list'],stdout=PIPE)
        last_start=(last_start.communicate()[0]).decode('ascii')
        last_start=last_start.split(": ")
        last_duration= last_start[-1][1:-2]
        last_reboot = last_start[-2].split("\n")[0][6:]
        #print last_start
        #print("\nLast Reboot took place at {}\nDevice has been active for {}".format(last_reboot,last_duration))
        
        data={'Total_RAM':t_RAM,'Used_RAM':u_RAM,"CPU1":cpu1,"CPU2":cpu2,"CPU3":cpu3,"CPU4":cpu4,"CPU5":cpu5,"CPU6":cpu6,"GPU":gpu,"AUX":AUX,"CPU":CPU,"TGPU":GPU_t,"AO":AO,"PMIC":PMIC,"thermal":thermal,"Memory_left":mem_left,"Memory_percentage":mem_percentage,"Total_memory":total_memory,"External_memory":ext_memory,"Last_Reboot":last_reboot,"Up_Time":last_duration,"Last_Event":event_code,"Last_Event_Time":event_time,"Error":error,"Error_Algo":error_algo,"Error_Time":error_time}
        print (data)
        return data

def apicall():
    try:
        sc = ClientSocket(device_id=str('BPCL_BPL_NX_0001'))
    except Exception as e:
        er=er+1
        if er < 4:
            time.sleep(1)
            apicall(event)
        error.raised("7",str(e))

    #while True:
    try:
        #data = {'key': 'value'}
        data =health()
        ts=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        sc.send(time_stamp=ts, message_type="GPU_HEARTBEAT", data=data)
        #time.sleep(2)
        msg = sc.receive()
        print(msg)
        if int(msg["data"]["status"]) == 200:
            print("API success")
        else:
            error.raised("8","API failed")
    except Exception as e:
        error.raised("8",str(e))

