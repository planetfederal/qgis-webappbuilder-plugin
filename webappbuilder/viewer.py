from future import standard_library
standard_library.install_aliases()
from builtins import str
# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import http.server
import socketserver
import os
import webbrowser
import threading
import time

PORT = 8000

server = None

def openWebApp(folder):
    global server
    if server is None:
        os.chdir(folder)
        server = socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler)
        thread = threading.Thread(target = server.serve_forever)
        thread.daemon = True
        thread.start()
        time.sleep(1000)
        webbrowser.open_new("http://127.0.0.1:" + str(PORT))

def shutdown():
    global server
    if server:
        server.shutdown()

        server = None
