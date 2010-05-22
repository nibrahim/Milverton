#!/usr/bin/env python

import select
import socket
import threading


def local_to_remote(lsock, rsock):
    print "Starting sending thread"
    vals = True
    p = []
    while vals:
        vals = lsock.recv(100)
        rsock.send(vals)
        p.append(vals)
    for i in "".join(p).split("\n"):
        print "> %s"%i

def remote_to_local(lsock, rsock):
    print "Starting retrieval thread"
    vals = True
    p = []
    while vals:
        vals = rsock.recv(100)
        lsock.send(vals)
        p.append(vals)
        r,w,x = [None]*3
        r, w, x = select.select([rsock],[],[], 1)
        if not r:
            break
    for i in "".join(p).split("\n"):
        print "< %s"%i        
    
def spawn_worker_thread(lsock, rsock):
    l2r = threading.Thread(group = None, target = local_to_remote, args = (lsock, rsock))
    r2l = threading.Thread(group = None, target = remote_to_local, args = (lsock, rsock))
    l2r.start()
    r2l.start()

def run_server(lsock, name, port):
    print "Server started"
    while True:
        lsock.listen(1)
        rsock = socket.socket()
        rsock.connect((name, port))
        conn,addr = lsock.accept()
        spawn_worker_thread(conn, rsock)

def main(lport, remote):
    lsock = socket.socket()
    lsock.bind(("localhost", int(lport)))
    addr = remote.split(":")
    rsock = socket.socket()
    run_server(lsock, addr[0], int(addr[1]))
    

if __name__ == "__main__":
    import sys
    lport, remote = sys.argv[1:]
    sys.exit(main(lport, remote))


