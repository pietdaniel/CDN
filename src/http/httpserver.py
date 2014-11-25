from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("Welcome!")
        return

def main():
    try:
        server = HTTPServer(("",PORT),GetHandler)
        print "Started server on %d" % PORT
        server.serve_forever()
    except KeyboardInterrupt:
        print "Keyboard Interrupt"
        server.socket.close()
main()
