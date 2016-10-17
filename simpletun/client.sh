#! /bin/bash

server_address=147.83.118.125

sudo tunctl -t tun0
ip link set tun0 up
ip addr add 192.168.0.2/24 dev tun0

./simpletun -i tun0 -c $server_address

#alternative
#sudo ifconfig tap0 10.0.0.1 netmask 255.255.255.0 up
#sudo ifconfig tap0 mtu 1420
#sudo route add default gw 10.0.0.2 metric 2 # ensure eth0 is preferred to tap0
