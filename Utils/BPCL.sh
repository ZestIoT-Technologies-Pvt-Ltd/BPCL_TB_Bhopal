cd /home/smartcow/BPCL/BPCL_final/

Process1=$(pgrep -f -x "python3 BPCL_vid.py")
if [ ! -z "$Process1" -a "$Process1" != "" ]; then
	echo "BPCL programis running"
else
	kill -9 $Process1
	echo "Starting BPCL process"
	python3 BPCL_vid.py
fi
