#!/usr/bin/env python

import select
import socket

def printlist(data, prefix):
    "Simple printer with a prefix"
    for i in data:
        print prefix, i
    

def read_request(sock):
    "Read an HTTP request from the local socket"
    retval = []
    while True:
        line = sock.readline()
        retval.append(line)
        if line == "\r\n":
            return retval

def send_request(request, sock):
    "Sends the request to the remote end"
    for i in request:
        sock.send(i)

def read_response(sock):
    retval = []
    while True:
        # r,w,x = None, None, None
        # print "selecting"
        # r,w,x, = select.select([sock],[],[],5)
        # print "selected"
        # if r:
        line = sock.readline()
        print "'%s'"%line.strip()
        retval.append(line)
        r,w,x = None, None, None
        print "selecting"
        r,w,x, = select.select([sock],[],[],5)
        print "selected"
        print r,w,x
        # else:
        #     break
    return retval

def send_response(response, sock):
    for i in response:
        sock.send(i)
        
def run_server(lsock, rsock):
    lsock.listen(1)
    conn,addr = lsock.accept()
    # conn.setblocking(False)
    # rsock.setblocking(False)
    ls_file = conn.makefile("r+")
    while True:
        request = read_request(ls_file)
        printlist(request, "> ")
        send_request(request, rsock)
        rs_file = rsock.makefile()
        response = read_response(rs_file)
        printlist(response, "< ")
        send_response(response, conn)

def main(lport, remote):
    lsock = socket.socket()
    lsock.bind(("localhost", int(lport)))
    addr = remote.split(":")
    rsock = socket.socket()
    rsock.connect((addr[0], int(addr[1])))
    run_server(lsock, rsock)
    
               
    


if __name__ == "__main__":
    import sys
    lport, remote = sys.argv[1:]
    sys.exit(main(lport, remote))


