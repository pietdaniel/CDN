import subprocess, re, urllib2

def send_latency_request(host, port, ip):
    request = urllib2.Request("http://%s:%s" % (host, str(port)), headers={"X-Latency-Check":str(ip)})
    contents = urllib2.urlopen(request).read()
    print contents

def recieve_latency_response(request):
    regex = re.compile("{lr:(?P<ip>.*):(?P<latency>[0-9]*\.[0-9]*)")
    r = regex.search(request)
    if r:
        results = r.groupdict()
        return (results['ip'], results['latency'])
    else:
        return False

def send_latency_response(latency, ip, host, port):
    domain = "{lr:%s:%s" % (str(ip),str(latency))
    send_dig(domain, host, port)


def send_dig(domain, host, port):
    command = "dig @%s -p %s %s" % (host, str(port), domain)
    print command
    p = subprocess.Popen(\
            command, shell=True, universal_newlines=True,\
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print p.communicate()

