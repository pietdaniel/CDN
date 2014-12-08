import socket, sys, os, re
from query import Query
import src.dns.lib.location as location
import src.lib.messenger as messenger
import src.dns.lib.database as database

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

            latency_response = messenger.recieve_latency_response(p.domain)
            if latency_response:
                print latency_response
                database.upsert_latency(latency=latency_response[1],\
                        ip=latency_response[0], server=addr[0])

                #database.get_latency(ip=latency_response[0], server=addr[0])

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
    db_result = database.get_latencies(ip=ip_address)
    if db_result and len(db_result) > 0:
        min_latency = 1000000
        min_server = None
        for result in db_result:
            if result[3] < min_latency:
                min_latency = result[3]
                min_server = result[2]
        return min_server

    closest = location.get_closest(ip_address)
    if closest:
        response = closest.values()[0][0]
    return response

