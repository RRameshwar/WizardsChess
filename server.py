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
import time
import cgi

import urlparse


class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Respond to a POST request."""
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        print("======= POST VALUES =======")
        print form['message'].value
        for item in form.list:
            print(item)
        print("\n")

        self.send_header("Content-type", "text/html")
        self.end_headers()

        time.sleep(5)
        self.wfile.write("Thanks in body" + "\n")


Handler = ServerHandler

INTERFACE = ""
PORT = 8000
httpd = SocketServer.TCPServer((INTERFACE, PORT), Handler)
httpd.allow_reuse_address = True

print "Serving at: http://%(interface)s:%(port)s" % dict(interface=INTERFACE or "localhost", port=PORT)
httpd.serve_forever()
