cd /home/nvidia/BPCL/BPCL_final/

end_time=$(jq '.Plant_end_time' UI_parameters.json | tr -d \")
start_time=$(jq '.Plant_start_time' UI_parameters.json| tr -d \")
end=$(date -d $end_time +%s)
start=$(date -d $start_time +%s)
now=$(date +%s)
Process1=$(pgrep -f -x "python3 BPCL_ch_final_wq.py")
if [ $now -gt $start -a $now -lt $end ]
then
	echo "start"
	if [ ! -z "$Process1" -a "$Process1" != "" ]; then
		echo "BPCL program is running"
	else
		kill -9 $Process1
		echo "Starting BPCL process"
		python3 BPCL_ch_final_wq.py  >> /media/49AE-64D6/BPCL.log
	fi
else
	echo "stop"
	if [ ! -z "$Process1" -a "$Process1" != "" ]; then
		echo "killing the running process"
		kill -9 $Process1
	fi

fi
