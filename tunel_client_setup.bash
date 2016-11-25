#!/bin/bash
#https://aftermanict.blogspot.com.es/2015/11/bash-iptables-iproute2-and-multiple.html
#http://themediaserver.com/bypass-vpn-connections-specifics-ports-ubuntu-kodibuntu/

#echo "1 primary" >> /etc/iproute2/rt_tables
#echo "2 secondary" >> /etc/iproute2/rt_tables


TUNINT=$1

sudo iptables -A OUTPUT -t mangle -p tcp --dport 80 -j MARK --set-mark 1
sudo iptables -A OUTPUT -t mangle -p tcp --dport 8080 -j MARK --set-mark 2
sudo ip rule add from all fwmark 1 table 1
sudo ip rule add from all fwmark 2 table 2
sudo ip route flush cache
# A default route should exist in the main routing table as well
#sudo ip route add default via 127.0.1.1
sudo ip route add table primary  default via 192.168.240.1
sudo ip route add table secondary default via 192.168.10.1
sudo iptables -t nat -A POSTROUTING -o enp0s25 -j MASQUERADE
sudo iptables -t nat -A POSTROUTING -o $TUNINT -j MASQUERADE

#Copy other routes to the new tables
#ip route show table main | grep -Ev ^default | while read ROUTE ; do sudo ip route add table primary $ROUTE; done
#ip route show table main | grep -Ev ^default | while read ROUTE ; do sudo ip route add table secondary $ROUTE; done

