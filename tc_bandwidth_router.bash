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
IF=enx00e04c534458		    # Interface 

# Modelado basado en [10]
# Download throughput (Mbps), Upload throughput (Mbps) andLatency - RTT (ms)
# guifi.net 9.78, 7.82, 14
# Telefonica 1.72, 0.54, 74

DNLD=1.72mbit          # DOWNLOAD Limit
LATENCY=36ms      # RTT / 2

start() {

# https://linux.die.net/man/8/tc-tbf

# Thoughtput
#	$TC qdisc add dev $IF root tbf rate $DNLD latency 50ms burst 1540

# Thoughtput and delay
#   $TC qdisc add dev $IF root handle 1:0 tbf rate $DNLD latency 50ms burst 1540
#   $TC qdisc add dev $IF parent 1:1 handle 10:0 netem delay $LATENCY


# https://linux.die.net/man/8/tc-htb

# Thoughtput and delay
   $TC qdisc add dev $IF root handle 1: htb
   $TC class add dev $IF parent 1:0 classid 1:1 htb  rate $DNLD
   $TC qdisc add dev $IF parent 1:1 handle 10:0 netem  delay $LATENCY
   $TC filter add dev $IF parent 1: protocol ip prio 1 u32 match ip dst 0.0.0.0/0 flowid 1:1
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

