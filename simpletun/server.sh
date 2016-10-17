! /bin/bash

sudo ip tuntap add dev tun1 mode tun
sudo ip link set tun1 up
sudo ip addr add 192.168.0.1/24 dev tun1

sudo ./simpletun -i tun1 -s

#sudo route add default gw 10.0.0.2 metric 2 # ensure eth0 is preferred to tap0
