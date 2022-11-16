#!/bin/bash
LIST_NAT=`cat nat.txt | grep IP_NAT | awk -F '[][]' '{print $2}'`

for IP_NAT in $LIST_NAT
do

export ${IP_NAT}_PORT_DESTINATION=$(cat nat.txt | awk "/\<$IP_NAT\>/" RS= nat.txt | grep PORT_DESTINATION | cut -d "=" -f 2)
export ${IP_NAT}_IP_TARGET=$(cat nat.txt | awk "/\<$IP_NAT\>/" RS= nat.txt | grep IP_TARGET | cut -d "=" -f 2)
export ${IP_NAT}_PORT_TARGET=$(cat nat.txt | awk "/\<$IP_NAT\>/" RS= nat.txt| grep PORT_TARGET | cut -d "=" -f 2)

echo ${IP_NAT}_PORT_DESTINATION
echo ${IP_NAT}_IP_TARGET
echo ${IP_NAT}_PORT_TARGET
done
