#! /bin/bash
vim /etc/sysconfig/network-scripts/$(ls /etc/sysconfig/network-scripts)

# OR 
ifconfig -a 
ifconfig ethX 10.180.117.0 netmask 255.255.255.0