#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Find Synology server in current router, assume it is one of 192.168.1.*
#

import socket
import urllib2
port = 80 # port number is a number, not string

def is_synology_server(address):
    url = 'http://' + address
    try:
        s = urllib2.urlopen(url).read()
        return s.lower().find('synology') >= 0
    except urllib2.URLError, e:
        return False

for i in range(0, 100):
    s = socket.socket()
    s.settimeout(0.1) #100ms timeout
    address = '192.168.1.' + str(100 + i)
    try:
        s.connect((address, port))
        #if we can connect then that is one possible server
        if is_synology_server(address):
            print address
            break #if you have multiple servers you can remove this line
    except Exception, e:
        continue

