echo "copying id to hosts"
while read host; do
  echo $host
  ssh-copy-id pietdan@$host
done <../ec2-hosts.txt
