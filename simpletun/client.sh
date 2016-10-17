#! /bin/bash

server_address=147.83.118.124

sudo ip tuntap add dev tun0 mode tun
sudo ip link set tun0 up
sudo ip addr add 192.168.0.2/24 dev tun0

sudo ./simpletun -i tun0 -c $server_address

#sudo route add default gw 10.0.0.2 metric 2 # ensure eth0 is preferred to tap0
