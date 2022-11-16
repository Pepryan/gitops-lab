#!/bin/bash
LIST_IP=`cat $1 | grep IP1 | awk '{print $2}'`
LIST_NAT_IP=`cat $2 | grep IP_TARGET | cut -d "=" -f 2`
for ip in $LIST_NAT_IP;
do

IP_TARGET=`cat $2 | grep IP_TARGET | cut -d "=" -f 2`
if [[ "$LIST_IP" == *"$NAT_IP"* ]];then
    echo "IP EXISTS, adding rules ..."
echo $IP_TARGET
echo $IP_LIST

IP_TARGET2=$IP_TARGET
#PROTOCOL=`cat $2 | grep PROTOCOL | cut -d "=" -f 2`
PORT_DESTINATION=`cat $2 | grep PORT_DESTINATION | cut -d "=" -f 2`
PORT_TARGET=`cat $2 | grep PORT_TARGET | cut -d "=" -f 2`

sudo iptables -t nat -A PREROUTING -p tcp --dport $PORT_DESTINATION -j DNAT --to-destination $IP_TARGET:$PORT_TARGET

LIST=`sudo iptables -t nat -v -L PREROUTING -n --line-number | grep $ip`
echo "Done added $LIST"
else
    echo "IP NOT EXISTS!"
fi
done
