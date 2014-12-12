from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2
import sys

class MyRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)              
        result.status = code  
        print "CODE:" 
        print code                              
        return result   

    http_error_302 = http_error_303 = http_error_307 = http_error_301

class HttpHandler(BaseHTTPRequestHandler):
    def make_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type','text/html')
        self.end_headers()

    def do_GET(self):
        request = "http://" + self.origin + ":8080" + self.path
        opener = urllib2.build_opener(MyRedirectHandler())
        urllib2.install_opener(opener)
        try:
            response = self.cache[self.path]
            # cache hit
            print "Hit"
            self.make_headers(response.code)
            self.wfile.write(response)
            self.cacheObjects.remove(self.path)
            self.cacheObjects.insert(0, self.path)
        except KeyError as e:
            # cache miss
            print "Miss"
            try:
                response = urllib2.urlopen(request)
                print response.code
                self.make_headers(response.code)
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
