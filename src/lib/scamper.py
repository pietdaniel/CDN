import subprocess, re

def trace(ip):
    """
      runs a traceroute to the given ip via scamper
      returns longest known latency as tuple of ip, latency
    """
    # the scamper command prioritized for speed
    command = 'scamper -c "trace -g 2 -w 1 -W 20 -q 1 -f 5" -i %s' % ip
        # -g number of * hops till quit
        # -w time to wait seconds
        # -W time to wait per probe 10s of ms
        # -q number of attempts used
        # -f initial ttl in ms !! cannot be greater then true latency

    p = subprocess.Popen(\
            command, shell=True, universal_newlines=True,\
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # blocking call here
    out, err = p.communicate()

    latency = _parse(out)
    if latency:
        return (ip, latency)
    else:
        print "Unabled to parse out a latency from scamper results\n\n%s" % out
        return False

def _parse(response):
    """
      takes scamper result and parses out latency
    """
    latency = None
    for line in response.split("\n"):
        temp = _extract_latency(line)
        if temp:
            latency = temp
    return latency

def _extract_latency(line):
    """
      returns the floating point number
      represented as a string
      from a given line
      if nothing is found returns false
    """
    g = re.findall("\d+.\d+ ms", line)
    if g and g[0] and type(g[0]) == type(""):
        return g[0].replace(" ms","")
    else:
        return False

