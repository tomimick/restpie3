#!/usr/bin/python
# -*- coding: utf-8 -*-

# mule1.py: independent worker process
#   - a TCP server as an example

import time
import socketserver

import logging
log = logging.getLogger("mule")


# example from https://docs.python.org/3/library/socketserver.html
class MyTCPServer(socketserver.BaseRequestHandler):
    """Simplest TCP server that echoes back the message."""

    def handle(self):
        self.data = self.request.recv(1024).strip()
        log.info(f"got data: {self.data}")
        self.request.sendall(self.data.upper()+b"\n")


def main():
    """Mule main function"""

    HOST = "0.0.0.0"
    PORT = 9999

    log.info(f"example mule worker started, listening on TCP port {PORT}")

    # create a TCP server
    with socketserver.TCPServer((HOST, PORT), MyTCPServer) as server:
        server.serve_forever()

    # never reached in this example
    # if you return from a worker, uwsgi will automatically restart
    log.info("mule end")


if __name__ == '__main__':
    main()

