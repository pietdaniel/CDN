#!/bin/bash
# origin ec2-54-164-51-70.compute-1.amazonaws.com

ip_adr() { 
  cat | egrep -o "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*";
}

ORIGIN="ec2-54-164-51-70.compute-1.amazonaws.com"
NAME="lol.com"
PORT=54123
USERNAME="pietdan"
KEY=/home/civil/.ssh/id_rsa


echo "Running deployCDN"

echo ""
../deployCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY

echo ""
echo "Running runCDN"
echo ""

../runCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY

echo ""
echo "Attempting dns resolution"
echo ""

ssh pietdan@`head -n 4 ../ec2-hosts.txt.orig | tail -n 1` dig @cs5700cdnproject.ccs.neu.edu -p $PORT $NAME | ip_adr
echo ""
ssh pietdan@`head -n 5 ../ec2-hosts.txt.orig | tail -n 1` dig @cs5700cdnproject.ccs.neu.edu -p $PORT $NAME | ip_adr
echo ""
ssh pietdan@`head -n 6 ../ec2-hosts.txt.orig | tail -n 1` dig @cs5700cdnproject.ccs.neu.edu -p $PORT $NAME | ip_adr
echo ""

echo "Running stopCDN"
echo ""
../stopCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY
echo ""


