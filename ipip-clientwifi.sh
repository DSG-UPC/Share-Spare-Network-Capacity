#! /bin/bash

#
# https://wiki.linuxfoundation.org/networking/tunneling
#

modprobe ipip

sudo ip tunnel add ipiptun1 mode ipip local 192.168.200.1 remote 192.168.200.2 ttl 64
sudo ip link set dev ipiptun1 up
sudo ip addr add 192.168.10.1/24 dev ipiptun1


