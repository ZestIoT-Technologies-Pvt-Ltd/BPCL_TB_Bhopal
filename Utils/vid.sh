cd /home/smartcow/BPCL/video_save/

Process1=$(pgrep -f -x "python3 video2.py")
if [ ! -z "$Process1" -a "$Process1" != "" ]; then
	echo "BPCL programis running"
else
	kill -9 $Process1
	echo "Starting BPCL process"
	python3 video2.py
fi
