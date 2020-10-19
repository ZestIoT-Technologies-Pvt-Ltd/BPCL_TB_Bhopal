import json
from datetime import datetime
config = "/home/smartcow/BPCL/BPCL_final/error.json"
error_state="/home/smartcow/BPCL/BPCL_final/error_code.txt"
def raised(error_code,error_string):
	try:
		with open(config) as json_data:
			info = json.load(json_data)
			error_time=str(datetime.now())
			error_string=error_string.replace("'"," ")
			with open(error_state,'w') as f:
				f.write("{} :: {} :: {} ****".format(info["error"][error_code],error_time,error_string))
				f.close()
				#error_call(error_code)
			json_data.close()
	except Exception as e:
		print (str(e))

def error_call(error_code):
	global er
	try:
		sc = ClientSocket(device_id=str('BPCL_BPL_NX_0001'))
	except Exception as e:
		er=er+1
		if er < 4:
			time.sleep(1)
			apicall(event)
			break
		error.raised("3",str(e))

	try:
		logdate=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
		data ={'error_time':logdate,'error_code':error_code}
		ts=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
		sc.send(time_stamp=ts, message_type="GPU_ERROR", data=data)
		#time.sleep(2)
		msg = sc.receive()
		print(msg)
		if int(msg["data"]["status"]) == 200:
			print("API success")
		else:
			error.raised("3","API failed")
	except Exception as e:
		error.raised("3",str(e))
