import json
from datetime import datetime
config = "/home/smartcow/BPCL/BPCL_final/error.json"
error_state="/home/smartcow/BPCL/BPCL_final/error_code.txt"
def raised(er,error_string):
	try:
		with open(config) as json_data:
			info = json.load(json_data)
			error_time=str(datetime.now())
			error_string=error_string.replace("'"," ")
			with open(error_state,'w') as f:
				f.write("{} :: {} :: {} ****".format(info["error"][er],error_time,error_string))
				f.close()
			json_data.close()
	except Exception as e:
		print (str(e))
