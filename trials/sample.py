#!/usr/bin/env python

import select
import socket

def printlist(data, prefix):
    "Simple printer with a prefix"
    print 20 * "="
    for i in data:
        print prefix, i.strip()
    print 20 * "="

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
    original = sock.readlines()
    printval = []
    # gzbody = False
    # body = False
    # for i in original:
    #     if i.startswith("Content-Encoding:") and i.split(":")[-1].strip() == "gzip":
    #         gzbody = True
    #     if i == "\r\n":
    #         body = True
    #         continue
    #     if body:
    #         print "Writing!"
    #         fp.write(i)
    # fp.close()
    # raise SystemExit
    return original, printval

def send_response(response, sock):
    for i in response:
        sock.send(i)
        
def run_server(lsock, rsock):
    while True:
        lsock.listen(1)
        conn,addr = lsock.accept()
        # conn.setblocking(False)
        # rsock.setblocking(False)
        ls_file = conn.makefile("r+")
        print "reading request"
        request = read_request(ls_file)
        printlist(request, "> ")
        print "sending request"
        send_request(request, rsock)
        rs_file = rsock.makefile()
        print "reading reponse"
        response,pval = read_response(rs_file)
        printlist(response, "< ")
        print "sending reponse"
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


