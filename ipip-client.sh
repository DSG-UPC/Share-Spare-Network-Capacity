#! /bin/bash

modprobe ipip

sudo ip tunnel add ipiptun1 mode ipip 147.83.118.24 remote 147.83.118.124 ttl 64
sudo ip link set dev ipiptun1 up
sudo ip addr add 192.168.0.2/24 dev ipiptun1


