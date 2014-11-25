from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print self.path
        print self.origin
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("Welcome!")
        return

def run(port, origin):
    try:
        server = HTTPServer(("",port),HttpHandler)
        print "Started server on %d" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        server.socket.close()
