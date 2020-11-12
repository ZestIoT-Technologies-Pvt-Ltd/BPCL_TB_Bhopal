import subprocess
import re
import sys
import requests
from datetime import datetime
temp_flag=0
temp_check=0
max=0

def get_sensor_data():
    sensors_out = subprocess.run(['sensors'], stdout=subprocess.PIPE)
    return sensors_out.stdout.decode('utf-8')

def parse_temps(sensor_data):
    temps = re.findall('\d+(?:\.\d+)?°C ', sensor_data, re.MULTILINE)
    return [x[:-3] for x in temps]



data= get_sensor_data()
temp = parse_temps(data)
for i in temp:
        if float(i) > 66.0:
                temp_flag=1
        if float(i) < 60.0:
                temp_check = temp_check +1
        if max < float(i):
                max=float(i)

print (temp_flag)
