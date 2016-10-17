#! /bin/bash

#
# https://wiki.linuxfoundation.org/networking/tunneling
#

modprobe ipip

sudo ip tunnel add ipiptun1 mode ipip local 147.83.118.124 remote 147.83.118.24 ttl 64
sudo ip link set dev ipiptun1 up
sudo ip addr add 192.168.0.1/24 dev ipiptun1



