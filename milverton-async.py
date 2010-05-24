#!/usr/bin/env python

import logging
import select
import socket
import asyncore

l2r_data = ""
r2l_data = ""

def print_data(data, prefix):
    "Displays the data being sent in a proper fashion"
    for i in "".join(data).split("\n"):
        print "         %s %s"%(prefix,i)

class RemoteSocket(asyncore.dispatcher):
    def __init__(self, raddr):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(raddr)

    def handle_connect(self):
        logging.info("Connected to remote endpoint")

    def handle_close(self):
        self.close()

    def handle_read(self):
        global r2l_data
        data = self.recv(8192)
        r2l_data += data
        print_data(data, "<")

    def handle_write(self):
        global l2r_data
        sent = self.send(l2r_data)
        l2r_data = l2r_data[sent:]
        
class ProxyHandler(asyncore.dispatcher):
    def writeable(self):
        global r2l_data
        return r2l_data
    
    def handle_close(self):
        self.close()

    def handle_read(self):
        global l2r_data
        data = self.recv(8192)
        l2r_data += data
        print_data(data, ">")

    def handle_write(self):
        global r2l_data
        sent = self.send(r2l_data)
        r2l_data = r2l_data[sent:]

class ProxyServer(asyncore.dispatcher):
    def __init__(self, lport, name, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("localhost", int(lport)))
        self.listen(1)
        self.raddr = (name,port)

    def handle_accept(self):
        client_info = self.accept()
        logging.info("Client connection received from %s"%str(client_info[1]))
        ProxyHandler(sock = client_info[0])
        RemoteSocket(self.raddr)
        self.handle_close()

    def handle_close(self):
        pass

def run_server(lport, name, port):
    logging.info("Server started")
    ProxyServer(lport, name, port)
    asyncore.loop()

def main(lport, remote):
    logging.basicConfig(format = "%(levelname)-15s : %(message)s", level = logging.DEBUG)
    addr = remote.split(":")
    run_server(int(lport), addr[0], int(addr[1]))

if __name__ == "__main__":
    import sys
    lport, remote = sys.argv[1:]
    try:
        sys.exit(main(lport, remote))
    except KeyboardInterrupt:
        logging.info("Shuting down")


