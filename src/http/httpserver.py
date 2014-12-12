from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import sys

class NoRedirectHandler(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        print response
        return response


class HttpHandler(BaseHTTPRequestHandler):

    def make_headers(self, response):
        self.send_response(response.code)
        self.send_header('Location', response.info().get('Location'))
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        request = "http://" + self.origin + ":8080" + self.path
        opener = urllib2.build_opener(NoRedirectHandler())
        urllib2.install_opener(opener)
        try:
            response = self.cache[self.path]
            # cache hit
            self.make_headers(response)
            self.wfile.write(response.read())
            self.cacheObjects.remove(self.path)
            self.cacheObjects.insert(0, self.path)
        except KeyError as e:
            # cache miss
            try:
                response = opener.open(request)
                self.make_headers(response)
                if sys.getsizeof(bytes(self.cache)) > 9000000:
                    del self.cache[self.cacheObjects.pop()]
                self.cache[self.path] = response
                self.cacheObjects.insert(0, self.path)
            except urllib2.HTTPError as e:
                self.make_headers(404)
                data = e.read()
            self.wfile.write(response.read())
        

def run(port, origin):
    try:
        handler = HttpHandler
        handler.origin = origin

        handler.cache = {}
        handler.cacheObjects = []

        server = HTTPServer(("",port),handler)
        print "Started server at ", server.socket.getsockname()
        server.serve_forever()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        server.socket.close()
