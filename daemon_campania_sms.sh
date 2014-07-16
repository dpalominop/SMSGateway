#!/bin/bash
# chkconfig: 123456 90 10

PATH_PROG=/home/dpalominop/campaign_sms/sms_web

start() {
    cd $PATH_PROG
    echo $PWD
    nohup python manage.py runserver 8080 &
    echo "Servidor web conectado"

    cd $PATH_PROG/demonio
    echo $PWD
    nohup python conexion_db.py &
    echo "Servidor de campanias conectado"
}

stop() {
    echo "Finalizando servidor web ..."
    pid=`ps -ef | grep 'python manage.py runserver 8080' | awk '{ print $2 }'`
    pid=`echo $pid | awk '{$NF = ""; print}'`
    echo $pid
    kill $pid
    sleep 2

    echo "Finalizando conexion con base de datos ..."
    pid=`ps -ef | grep 'python conexion_db.py' | awk '{ print $2 }'`
    pid=`echo $pid | awk '{$NF = ""; print}'`
    echo $pid
    kill $pid
    sleep 2

    echo "Servers killed."
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
        echo "Uso: bash /daemon_campania_sms.sh {start|stop|restart}"
        exit 1
esac
exit 0
