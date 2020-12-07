CheckProcess=$(pgrep -f -x "/usr/lib/autossh/autossh -M 10991 -N -i /home/smartcow/BPCL/Utils/jan-test.pem -R 6696:localhost:22 avileap@34.216.237.202")
#if [${CheckProcess:1} -gt 1 ]; then
if [ ! -z "$CheckProcess" -a "$CheckProcess" != " " ]; then
        echo "remote_autossh.sh already running"
else
        echo "Safe to start new remote.sh process"
        autossh -M 10991 -N -i /home/smartcow/BPCL/Utils/jan-test.pem -R 6696:localhost:22 avileap@34.216.237.202 &
fi

