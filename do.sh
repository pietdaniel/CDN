#!/bin/bash
# origin ec2-54-164-51-70.compute-1.amazonaws.com
ORIGIN="ec2-54-164-51-70.compute-1.amazonaws.com"
NAME="lol.com"
PORT=54443
USERNAME="pietdan"
KEY=/home/civil/.ssh/id_rsa


echo "Running deployCDN"
echo ""
echo ""
#./deployCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY
echo "Running runCDN"
echo ""
echo ""
./runCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY

echo "Attempting dns resolution"
echo ""
echo ""
#dig @cs5700cdnproject.ccs.neu.edu -p $PORT $NAME
echo "Running stopCDN"
echo ""
echo ""
#./stopCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY


