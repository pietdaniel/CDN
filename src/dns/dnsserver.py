#!/usr/bin/python
import socket, sys

class Query:
    def __init__(self, data):
        self.data = data
        self.domain=''

        # parse out domain
        opcode = (ord(data[2]) >> 3) & 15
        if opcode == 0:
            cursor = 12
            length = ord(data[cursor])
            while length!=0:
                self.domain+=data[cursor+1:cursor+length+1]+'.'
                cursor+=length+1
                length=ord(data[cursor])

    def answer(self, ip):
        packet=''
        if self.domain:
            packet+=self.data[:2] + "\x81\x80"
            # q/a counts
            packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'
            # original dns q
            packet+=self.data[12:len(self.data)-11]
            # point to domain name
            packet+='\xc0\x0c'
            # response type, ttl, length
            packet+='\x00\x01\x00\x01\x00\x00\x00\x4c\x00\x04'
            # ip bytes
            packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.')))
        return packet


def run(port, name):
    STUB_RESPONSE = '192.168.1.5'

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('',port))
    except Exception, e:
        print 'failed to create socket %s' % e
        sys.exit(1)

    print 'Running dns server'

    try:
        while 1:
            data, addr = s.recvfrom(1024)
            p=Query(data)
            s.sendto(p.answer(STUB_RESPONSE), addr)
            print '%s -> %s' % (p.domain, addr)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt'
        s.close()

