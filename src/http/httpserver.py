from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import sys

class NoRedirectHandler(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        print response
        return response


class HttpHandler(BaseHTTPRequestHandler):

    def make_headers(self, info):
        self.send_header(info)
        self.end_headers()

    def do_GET(self):
        request = "http://" + self.origin + ":8080" + self.path
        opener = urllib2.build_opener(NoRedirectHandler())
        urllib2.install_opener(opener)
        try:
            response = self.cache[self.path]
            # cache hit
            print "Hit"
            #self.make_headers(response.code)
            self.wfile.write(response)
            self.cacheObjects.remove(self.path)
            self.cacheObjects.insert(0, self.path)
        except KeyError as e:
            # cache miss
            print "Miss"
            try:
                response = opener.open(request)
                self.headers = response.info()
                data = response.read()
                print sys.getsizeof(bytes(self.cache))
                if sys.getsizeof(bytes(self.cache)) > 9000000:
                    del self.cache[self.cacheObjects.pop()]
                self.cache[self.path] = data
                self.cacheObjects.insert(0, self.path)
            except urllib2.HTTPError as e:
                self.make_headers(404)
                data = e.read()
            self.wfile.write(data)
        

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
