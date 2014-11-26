from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import sys



class HttpHandler(BaseHTTPRequestHandler):

    def make_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        request = "http://" + self.origin + ":8080" + self.path
        try:
            response = self.cache[self.path]
            # cache hit
            #print "Hit"
            self.make_headers(200)
            self.wfile.write(response)
        except KeyError as e:
            # cache miss
            #print "Miss"
            try:
                response = urllib2.urlopen(request)
                self.make_headers(200)
                data = response.read()
                if sys.getsizeof(bytes(self.cache)) > 9000000:
                    self.cache = {}
                self.cache[self.path] = data
            except:
                self.make_headers(404)
                data = "404"
            self.wfile.write(data)

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
