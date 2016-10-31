#!/bin/bash
#
#  tc uses the following units when passed as a parameter.
#  kbps: Kilobytes per second 
#  mbps: Megabytes per second
#  kbit: Kilobits per second
#  mbit: Megabits per second
#  bps: Bytes per second 
#       Amounts of data can be specified in:
#       kb or k: Kilobytes
#       mb or m: Megabytes
#       mbit: Megabits
#       kbit: Kilobits
#  To get the byte figure from bits, divide the number by 8 bit
#
TC=/sbin/tc
IF=eno1		    # Interface 
IP=216.3.128.12     # Host IP

# Modelado basado en [10]
# Download throughput (Mbps), Upload throughput (Mbps) andLatency - RTT (ms)
# guifi.net 9.78, 7.82, 14
# Telefonica 1.72, 0.54, 74

DNLD=1.72mbps          # DOWNLOAD Limit
LATENCY=74ms

start() {

# https://linux.die.net/man/8/tc-tbf
#	$TC qdisc add dev $IF root tbf rate $DNLD latency 50ms burst 1540

# https://linux.die.net/man/8/tc-cbq
#   $TC qdisc add $IF root cbq bandwidth $DNLD avpkt 1000
    $TC qdisc add dev $IF root handle 1:0 netem delay $LATENCY
	$TC qdisc add dev $IF parent 1:1 handle 10: cbq bandwidth $DNLD avpkt 1000
}

stop() {

    $TC qdisc del dev $IF root

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

    echo -n "Starting bandwidth shaping: "
    start
    echo "done"
    ;;

  stop)

    echo -n "Stopping bandwidth shaping: "
    stop
    echo "done"
    ;;

  restart)

    echo -n "Restarting bandwidth shaping: "
    restart
    echo "done"
    ;;

  show)
    	    	    
    echo "Bandwidth shaping status for $IF:\n"
    show
    echo ""
    ;;

  *)

    pwd=$(pwd)
    echo "Usage: $(/usr/bin/dirname $pwd)/tc_bandwidth.bash {start|stop|restart|show}"
    ;;

esac

exit 0

