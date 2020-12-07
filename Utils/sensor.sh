cd /home/smartcow/BPCL/Utils

temp=$(python3 BPCL_temp.py)
echo $temp
if (( $temp==1 ))
then
        echo "temperature is high stopping all applications"
        crontab high_temp.txt
	Process1=$(pgrep -f -x "python3 BPCL_ch_final.py")
	kill -9 $Process1
else
        echo "temperature is normal restarting all applications"
        crontab low_temp.txt
fi

