import subprocess, re

def send(message, ip):
    command = "dig @%s %s" % (ip, message.get_domain())
    p = subprocess.Popen(\
            command, shell=True, universal_newlines=True,\
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def receive(domain):
    pass

def is_message(domain):
    pass

class message:
    def get_domain(self):
        raise Exception("Unimplemented %s" % self)

class ping_request(message):
    def get_domain(self):
        return "{ping"

class ping_response(message):
    def get_domain(self):
        return "{pong"

class update_request(message):
    def __init__(self, ip, server, latency):
        self.ip = ip
        self.server = server
        self.latency = latency

    def get_domain(self):
        domain = "{uq%s:%s:%s" % (self.ip, self.server, self.latency)
        return domain

class trace_request(message):
    def __init__(self, ip):
        self.ip = ip

    def get_domain(self):
        return "{tq%s" % self.ip

class trace_response(message):
    def __init__(self, ip, server, latency):
        self.ip = ip
        self.server = server
        self.latency = latency

    def get_domain(self):
        return "{ts%s:%s:%s" % (self.ip, self.server, self.latency)
