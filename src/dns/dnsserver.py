import socket, sys, os, re
from query import Query

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
            if p.domain == name:
                response = config.replice_map['us-east']
            else:
                response = p.question(p.domain)
                if not response: # couldn't find host
                    response = STUB_RESPONSE
            s.sendto(p.answer(response), addr)
            print '%s -> %s' % (p.domain, response)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt'
        s.close()
