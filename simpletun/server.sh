! /bin/bash

sudo tunctl -t tun1
ip link set tun1 up
ip addr add 192.168.0.1/24 dev tun0

./simpletun -i tun1 -s

#alternative
#sudo ifconfig tap0 10.0.0.1 netmask 255.255.255.0 up
#sudo ifconfig tap0 mtu 1420
#sudo route add default gw 10.0.0.2 metric 2 # ensure eth0 is preferred to tap0
