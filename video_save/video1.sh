cd /home/smartcow/BPCL/video_save/
Process1=$(pgrep -f -x "sudo python3 video1.py")
if [ ! -z "$Process1" -a "$Process1" != "" ]; then
   echo "it is saving video"
else
   kill -9 $Process1
   echo "Going to start capturing video every minute"
   sudo python3 video1.py
fi
