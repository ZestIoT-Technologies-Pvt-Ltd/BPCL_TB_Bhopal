import json
from datetime import datetime
config = "/home/smartcow/BPCL/BPCL_final/error.json"
error_state="/home/smartcow/BPCL/BPCL_final/error_code.txt"
error_code = 0
def raised(er,error_string):
	try:
		error_code = error_code | er
		with open(error_state,'w') as f:
			logdate=(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
			f.write(str({"error_code":error_code,"error_algo":er_string,"error_time":logdate}))
			f.close()
	except Exception as e:
		print (str(e))