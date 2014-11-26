from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import sys



class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = "http://" + self.origin + ":8080" + self.path

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        try:
            response = self.cache[self.path]
            # cache hit
            print "Hit"
            self.wfile.write(response)
        except KeyError as e:
            # cache miss
            print "Miss"
            response = urllib2.urlopen(request)
            data = response.read()
            self.cache[self.path] = data
            print sys.getsizeof(self.cache)
            self.wfile.write(self.cache[self.path])
        return

def run(port, origin):
    try:
        handler = HttpHandler
        handler.origin = origin

        handler.cache = {}

        server = HTTPServer(("",port),handler)
        print "Started server at ", server.socket.getsockname()
        server.serve_forever()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        server.socket.close()
