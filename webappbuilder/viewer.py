import SimpleHTTPServer
import SocketServer
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
        server = SocketServer.TCPServer(("", PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)
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

