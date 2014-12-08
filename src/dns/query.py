#!/usr/bin/python
import socket, sys, os, re

VALID_IP_REGEX = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

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
            packet+=self.data[12:len(self.data)]
            # point to domain name
            packet+='\xc0\x0c'

            # response type, ttl, length
            packet+='\x00\x01\x00\x01\x00\x00\x00\x4c\x00\x04'
            # ip bytes
            try:
                packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.')))
            except AttributeError as e:
                print ip
                raise e
        return packet

    def question(self, hostname):
        process = os.popen('dig %s +nocomments\
                +noquestion +noauthority +noadditional +nostats' % hostname)
        response = process.read()
        process.close()
        for line in response.split("\n"):
            try:
                comment = line.index(';')
                line = line[0:comment]
            except ValueError as e:
                pass
            for i in line.split("\t"):
                a = re.match(VALID_IP_REGEX, i)
                if a:
                    return a.group(0)
        return False
