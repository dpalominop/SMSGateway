#!/bin/bash
# chkconfig: 123456 90 10

PATH_PROG=/home/dpalominop/campaign_sms/sms_web/demonio

start() {
    cd $PATH_PROG
    echo $PWD
    python conexion_db.py &
    echo "Servidor de campanias conectado"
}

stop() {
    pid=`ps -ef | grep 'python conexion_db.py' | awk '{ print $2 }'`
    pid=`echo $pid | awk '{$NF = ""; print}'`
    echo $pid
    kill $pid
    sleep 2
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
        echo "Uso: bash /daemon_conexion_db.sh {start|stop|restart}"
        exit 1
esac
exit 0
