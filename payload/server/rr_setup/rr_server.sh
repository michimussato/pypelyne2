#!/usr/bin/sh
# chkconfig: 123456 90 10
# TTS Server for Speech Synthesis
# https://wolfpaulus.com/journal/software/pythonlauncher/

pypelyne_share=/pypelyne

rr_src=${pypelyne_share}/royalrender_src/

pypelyne_root=${pypelyne_share}/pypelyne
rr_root=${pypelyne_share}/royalrender_repository
log_dir=${pypelyne_share}/logs


start() {
    if [ -z ${RR_ROOT} ]; 
        then {
        export RR_ROOT=${rr_root}
        echo 'RR_ROOT successfully exported'
        }
    fi
    if [ ! -d ${log_dir} ]; then
        mkdir ${log_dir}
        chown nobody:nobody ${log_dir}
        chmod 777 ${log_dir}
        echo 'log_dir created'
    fi
#    cd ${workdir}
    ${rr_root}/bin/lx64/rrServerconsole >> ${log_dir}/rr-server.log 2>&1 &
#    /pypelyne/royalrender_repository/bin/lx64/rrServerconsole >> /pypelyne/logs/rr-server.log 2>&1 &
    echo "Server started."
}
 
stop() {
    pid=$(ps -ef | grep "rrServerconsole" | awk '{ print $2 }')
#    pid=`ps -ef | grep 'rrServerconsole' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 10
    echo "Server killed."
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: /etc/init.d/rr-server {start|stop|restart}"
    exit 1
esac
exit 0