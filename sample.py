#!/usr/bin/env python

import select
import socket
import threading
import SocketServer

class HTTPDebugHandler(SocketServer.StreamRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def local_to_remote(self):
        while True:
            r, w, x = None, None, None
            r, w, x = select.select([self.rfile],[],[])
            if r:
                data = self.rfile.readline()
                print "> %s"%data
                self.server.rsock.write(data)
            
    def remote_to_local(self):
        while True:
            r, w, x = None, None, None
            r, w, x = select.select([self.server.rsock],[],[])
            if r:
                data = self.server.rsock.readline()
                print "< %s"%data
                self.wfile.write(data)
    
    def handle(self):
        print "Received connection"
        l2r = threading.Thread(group = None, target = self.local_to_remote)
        r2l = threading.Thread(group = None, target = self.remote_to_local)
        l2r.start()
        r2l.start()
        l2r.join()


class HTTPDebug(SocketServer.TCPServer):
    def __init__(self, local_addr, remote_addr):
        self._rsock = socket.socket()
        self._rsock.connect(remote_addr)
        self.rsock = self._rsock.makefile("r+")
        SocketServer.TCPServer.__init__(self, local_addr, HTTPDebugHandler)


if __name__ == "__main__":
    import sys
    HOST, PORT = sys.argv[1:]
    
    # Create the server, binding to localhost on port 9999
    server = HTTPDebug((HOST, int(PORT)), ("www.google.com", 80))

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print "Starting server on %s port %s"%(HOST, PORT)
    server.serve_forever()
