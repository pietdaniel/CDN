from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib2

site_origin


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        request = "http://" + site_origin + ":8080" + self.path
        print request
        response = urllib2.urlopen(request)
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(response.read())
        return

def run(port, origin):
    site_origin = origin
    print origin
    print site_origin
    try:
        server = HTTPServer(("",port),HttpHandler)
        print "Started server at ", server.socket.getsockname()
        server.serve_forever()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        server.socket.close()
