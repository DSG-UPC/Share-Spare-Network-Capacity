#!/bin/bash
#https://aftermanict.blogspot.com.es/2015/11/bash-iptables-iproute2-and-multiple.html
#http://themediaserver.com/bypass-vpn-connections-specifics-ports-ubuntu-kodibuntu/



TUNINT=$1

sudo iptables -D OUTPUT -t mangle -p tcp --dport 80 -j MARK --set-mark 1
sudo iptables -D OUTPUT -t mangle -p tcp --dport 8080 -j MARK --set-mark 2
sudo ip rule del from all fwmark 1 table 1
sudo ip rule del from all fwmark 2 table 2
sudo ip route flush cache
# A default route should exist in the main routing table as well
#sudo ip route add default via 127.0.1.1
sudo ip route flush table primary
sudo ip route flush table secondary
sudo iptables -t nat -D POSTROUTING -o enp0s25 -j MASQUERADE
sudo iptables -t nat -D POSTROUTING -o $TUNINT -j MASQUERADE

