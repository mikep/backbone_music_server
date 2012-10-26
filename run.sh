#!/bin/sh -e
#!/bin/sh -e

NAME=music_server
DAEMON=/usr/bin/$NAME
USER=root
#USER=debian-transmission
# FIXME: no pidfile support; forks, so --make-pidfile doesn't work either
#PIDFILE=/var/run/$NAME.pid
STOP_TIMEOUT=3

. /lib/lsb/init-functions

start_daemon () {
    python manage.py runfcgi method=threaded host=127.0.0.1 port=9002
}

stop_daemon () {
    kill -9 `ps -e | grep manage.p | grep -v grep | awk '{print $1}'`
}

case "$1" in
    start)
        log_daemon_msg "Starting MUSIC_SERVER django app fcgi" "$NAME"
        start_daemon
        log_end_msg 0
        ;;  
    stop)
        log_daemon_msg "Stopping MUSIC_SERVER django app fcgi" "$NAME"
        stop_daemon
        log_end_msg 0
        ;;  
    restart|force-reload)
        log_daemon_msg "Restarting MUSIC_SERVER django app fcgi" "$NAME"
        stop_daemon
        start_daemon
        log_end_msg 0
        ;;  
    *)  
        echo "Usage: $NAME {start|stop|restart}"
        exit 2
        ;;  
esac

exit 0
