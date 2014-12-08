from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import sys, time, heapq
import src.lib.scamper as scamper
import src.lib.messenger as messenger
from multiprocessing import Process, Queue
from Queue import PriorityQueue

class HttpHandler(BaseHTTPRequestHandler):
    def make_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        if "X-Latency-Check" in self.headers:
            ip = self.headers['X-Latency-Check']
            print 'Recieved Lookup Request for ip %s' % ip
            self.lookups.put(ip)
            self.wfile.write("200")
        else:
            request = "http://" + self.origin + ":8080" + self.path
            try:
                response = self.cache[self.path]
                # cache hit
                print "Hit"
                self.make_headers(200)
                self.wfile.write(response)
                self.cacheObjects.remove(self.path)
                self.cacheObjects.insert(0, self.path)
            except KeyError as e:
                # cache miss
                print "Miss"
                try:
                    response = urllib2.urlopen(request)
                    self.make_headers(200)
                    data = response.read()
                    print sys.getsizeof(bytes(self.cache))
                    if sys.getsizeof(bytes(self.cache)) > 8000000:
                        print "PURGING"
                        del self.cache[self.cacheObjects.pop()]
                    self.cache[self.path] = data
                    self.cacheObjects.insert(0, self.path)
                except urllib2.HTTPError as e:
                    self.make_headers(404)
                    data = e.read()
                self.wfile.write(data)

def lookup_daemon(queue, config):
    while True:
        start = time.time()
        ip = queue.get()
        print 'Attempting to get latency of ip: %s' % ip
        results = scamper.trace(ip)
        if results:
            print 'Recieved latency of %s' % str(results[1])
            #messenger.send_latency_response(results[1], results[0], config.cdn, config.port)
            # TODO change
            messenger.send_latency_response(results[1], results[0], "localhost", 55543)
        end = time.time()
        if end - start < 1:
            time.sleep(end - start)

def run(port, origin, config):
    try:
        lookup_queue = Queue()

        reader_p = Process(target=lookup_daemon, args=((lookup_queue),(config)))
        reader_p.daemon = True
        reader_p.start()

        handler = HttpHandler
        handler.origin = origin

        handler.cache = {}
        handler.cacheObjects = []

        handler.lookups = lookup_queue

        server = HTTPServer(("",port),handler)
        print "Started server at ", server.socket.getsockname()
        server.serve_forever()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        server.socket.close()
