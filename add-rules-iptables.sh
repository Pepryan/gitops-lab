#!/bin/bash
LIST_NAT=$(cat $1 | grep IP_NAT | awk -F '[][]' '{print $2}')
for IP_NAT in $LIST_NAT; do
    PORT_DESTINATION=$(cat $1 | awk "/\<$IP_NAT\>/" RS= $1 | grep PORT_DESTINATION | cut -d "=" -f 2)
    IP_TARGET=$(cat $1 | awk "/\<$IP_NAT\>/" RS= $1 | grep IP_TARGET | cut -d "=" -f 2)
    PORT_TARGET=$(cat $1 | awk "/\<$IP_NAT\>/" RS= $1 | grep PORT_TARGET | cut -d "=" -f 2)

    sudo iptables -t nat -A PREROUTING -p tcp --dport $PORT_DESTINATION -j DNAT --to-destination $IP_TARGET:$PORT_TARGET

    # echo $PORT_DESTINATION
    echo $IP_TARGET
    # echo $PORT_TARGET

    LIST=$(sudo iptables -t nat -v -L PREROUTING -n --line-number | grep $IP_TARGET)
    echo "Done added $LIST"
done
