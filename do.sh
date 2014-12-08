#!/bin/bash
# origin ec2-54-164-51-70.compute-1.amazonaws.com
ORIGIN="ec2-54-164-51-70.compute-1.amazonaws.com"
NAME="lol.com"
PORT=54443
USERNAME="pietdan"
KEY=/home/civil/.ssh/id_rsa


./deployCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY
#./runCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY

#dig @cs5700cdnproject.ccs.neu.edu -p $PORT $NAME

#./stopCDN -p $PORT -o $ORIGIN -n $NAME -u $USERNAME -i $KEY


