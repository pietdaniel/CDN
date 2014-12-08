import socket, sys, os, re
from query import Query
import src.dns.lib.location as location

def run(port, name, config):
    STUB_RESPONSE = '0.0.0.0'

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('',port))
    except Exception as e:
        print 'failed to create socket %s' % e
        sys.exit(1)

    print 'Running dns server'

    try:
        while 1:
            data, addr = s.recvfrom(1024)
            p=Query(data)
            # if host is our cdn target
            if name in p.domain:
                response = handle_response(addr[0], config)
            else:
                response = p.question(p.domain)
                if not response: # couldn't find host
                    response = STUB_RESPONSE
            s.sendto(p.answer(response), addr)
            print '%s -> %s' % (p.domain, response)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt'
        s.close()

def handle_response(ip_address, config):
    response = config.replica_map['us-east'][0]
    closest = location.get_closest(ip_address)
    if closest:
        response = closest.pop()[2]
    return response

