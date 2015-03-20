
 #!/usr/bin/python

"""
Save this file as server.py
>>> python server.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python server.py
Serving on localhost:8000

You can use this to test GET and POST methods.

"""

import SimpleHTTPServer
import SocketServer
import logging
import cgi

import sys
import urlparse
import unicodedata

if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(s):
        """Respond to a POST request."""

        # Extract and print the contents of the POST
        length = int(s.headers['Content-Length'])
        post_data = urlparse.parse_qs(s.rfile.read(length).decode('utf-8'))
        
        s.send_header("Content-type", "text/html")
        print post_data["word"][0].encode('ascii', 'ignore')

        s.end_headers()
        s.wfile.write("Thanks in body" + "\n")

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)
httpd.allow_reuse_address = True

print "@rochacbruno Python http server version 0.1 (for testing purposes only)"
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()
