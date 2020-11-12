CheckProcess=$(pgrep -f -x "/usr/lib/autossh/autossh -M 10997 -N -i /home/smartcow/BPCL/Utils/device-comms-ssh.pem -R 6696:localhost:22 ubuntu@13.126.111.12")
#if [${CheckProcess:1} -gt 1 ]; then
if [ ! -z "$CheckProcess" -a "$CheckProcess" != " " ]; then
        echo "remote_autossh.sh already running"
else
        echo "Safe to start new remote.sh process"
        autossh -M 10997 -N -i /home/smartcow/BPCL/Utils/device-comms-ssh.pem -R 6696:localhost:22 ubuntu@13.126.111.12 &
fi

