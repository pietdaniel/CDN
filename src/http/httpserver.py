from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2, requests
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
            print "Hit"
            self.make_headers(200)
            self.wfile.write(response)
            self.cacheObjects.remove(self.path)
            self.cacheObjects.insert(0, self.path)
        except KeyError as e:
            # cache miss
            print "Miss"
            try:
                response = requests.get(request, allow_redirects=False)
                self.make_headers(response.status_code)
                data = response.content
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
