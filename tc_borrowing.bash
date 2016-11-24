#!/bin/bash
#
# http://lartc.org/howto/lartc.qdisc.classful.html
# http://www.docum.org/docum.org/tests/cbq/classes.php
# http://lartc.org/howto/lartc.cookbook.ultimate-tc.html
#

TC=/sbin/tc
IF=enx00e04c534458		    # Interface 

DNLD=1.72mbit          # DOWNLOAD Limit
LIM1=1mbit          # for each class
LIM2=1mbit          # for each class
CEIL=2mbit
 
start() {
    #$TC qdisc add dev $IF root handle 1: htb default 30
    #$TC class add dev $IF parent 1: classid 1:1 htb rate $DNLD burst 15k

    $TC class add dev $IF parent 1:1  classid 1:10 htb rate $LIM1 burst 15k
    $TC class add dev $IF parent 1:1 classid 1:20 htb rate $LIM2 ceil $CEIL burst 15k
    $TC class add dev $IF parent 1:1 classid 1:30 htb rate 1kbit ceil $CEIL burst 15k
    #$TC qdisc add dev $IF parent 1:10 handle 10: sfq perturb 10
    #$TC qdisc add dev $IF parent 1:10 handle 10: fq_codel limit 300
    #$TC qdisc add dev $IF parent 1:20 handle 20: sfq perturb 10
    #$TC qdisc add dev $IF parent 1:20 handle 20: fq_codel limit 300
 #   $TC qdisc add dev $IF parent 1:30 handle 30: sfq perturb 10

    U32="tc filter add dev $IF protocol ip parent 1:0 prio 1 u32"
#    $U32 match ip dst 0.0.0.0/0 flowid 1:10
    $U32 match ip sport 80 0xffff flowid 1:10
    $U32 match ip dport 80 0xffff flowid 1:10
#    $U32 match ip dst 0.0.0.0/0 flowid 1:20
    $U32 match ip sport 8080 0xffff flowid 1:20
    $U32 match ip dport 8080 0xffff flowid 1:20
    show
}

stop() {

    #$TC qdisc del dev $IF root
    U32="tc filter del dev $IF protocol ip parent 1:0 prio 1 u32"
#    $U32 match ip dst 0.0.0.0/0 flowid 1:10
    $U32 match ip sport 80 0xffff flowid 1:10
    $U32 match ip dport 80 0xffff flowid 1:10
#    $U32 match ip dst 0.0.0.0/0 flowid 1:20
    $U32 match ip sport 8080 0xffff flowid 1:20
    $U32 match ip dport 8080 0xffff flowid 1:20
    $TC class del dev $IF parent 1:1 classid 1:10 htb rate $LIM1 burst 15k
    $TC class del dev $IF parent 1:1 classid 1:20 htb rate $LIM2 ceil $CEIL burst 15k
    $TC class del dev $IF parent 1:1 classid 1:30 htb rate 1kbit ceil $CEIL burst 15k

    


}

restart() {

    stop
    sleep 1
    start

}

show() {

    $TC -s qdisc ls dev $IF

}

case "$1" in

  start)

    echo -n "Starting: "
    start
    echo "done"
    ;;

  stop)

    echo -n "Stopping: "
    stop
    echo "done"
    ;;

  restart)

    echo -n "Restarting: "
    restart
    echo "done"
    ;;

  show)
    	    	    
    echo "qdisc status for $IF:"
    show
    echo ""
    ;;

  *)

    pwd=$(pwd)
    echo "Usage: $(/usr/bin/dirname $pwd)/tc_borrowing.bash {start|stop|restart|show}"
    ;;

esac

exit 0

