#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Find Synology server in current router, assume it is one of 192.168.1.*
#

import socket
import urllib.request
import urllib.error


PORT = 80  # port number is a number, not string


def is_synology_server(address):
    url = 'http://' + address
    try:
        with urllib.request.urlopen(url) as file:
            html = file.read()
            return html.lower().find('synology') >= 0
    except urllib.error.HTTPError:
        return False


def main():
    for i in range(0, 100):
        sock = socket.socket()
        sock.settimeout(0.1)  # 100ms timeout
        address = '192.168.1.' + str(100 + i)
        try:
            sock.connect((address, PORT))
            # if we can connect then that is one possible server
            if is_synology_server(address):
                print(address)
                break  # if you have multiple servers you can remove this line
        except socket.error:
            continue


main()
