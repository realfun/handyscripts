#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMAP test, tcp/ip, not ssl
#     Zhongfang Ren, realfun@gmail.com, Wednesday, February 29, 2012, 14:44:19
# http://tools.ietf.org/html/rfc3501

import socket
from threading import Thread, Event
import select

import sys, os, re, fcntl
import traceback
import getopt
import time
import readline


# make stdin a non-blocking file
# from: http://stackoverflow.com/a/1810703/93571
fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

class IMAPClient(Thread):
    def __init__(self, server, port):
        Thread.__init__(self)
        self.server = server
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, port))
        self.running = True
        self._event = Event()
        self._event.clear()
        #print "Socket Connected to: ", server, port

    def stop(self):
        self.running = False

    def is_alive(self):
        return self.running

    def run(self):
        try:
            buff = ''
            skip = 0
            while self.running:
                #non-block receiving
                socks,_,_ = select.select([self.sock], [], [], 0.01)
                if not socks: continue

                #sock = socks[0]
                temp = self.sock.recv(1024)
                if not temp: #socket closed, exit
                    break
                #handling recieved buffs, NOT assuming buff ends with \r\n
                buff += temp
                pos = 0
                while pos != -1:
                    #jump over literal strings
                    if skip:
                        print buff[:skip]
                        if len(buff) > skip:
                            buff = buff[skip:]
                            skip = 0
                        else:
                            skip -= len(buff)
                            buff = ''
                            break
                    #look for new literal string start
                    pos = buff.find('\n')
                    line = buff[:pos]
                    print line
                    m = re.match(r'\{(\d+)\}$', line)
                    #handle literal string start {###}, see rfc3501 for literal format
                    if m:
                        assert skip == 0, "Wrong format in Literal string"
                        skip = int(m.group(1))
                        continue
                    #handle TAGGED response
                    if hasattr(self, 'tag_to_wait') and buff.startswith(self.tag_to_wait):
                        self._event.set()
                    #go to next line
                    buff = buff[pos+1:]
                    pos = buff.find('\n')
        except socket.error:
            pass
        #print "SOCKET WAS TERMINATED!"
        self.running = False
        self._event.set()

    def wait_for_response(self):
        self._event.wait(30) #timeout after 30 seconds?
        self._event.clear()

    def send_cmd_and_wait_for_response(self, line):
        #print 1111, repr(line)
        if self.running:
            self._event.clear()
            self.send_cmd(line)
            self.wait_for_response()

    def send_cmd(self, line):
        self.tag_to_wait = line.split()[0] + ' '
        if self.running:
            self.sock.send(line + "\r\n")

#------------------------------------------------------
# main function start here
def usage():
    print """
       imapin - take an imap command input file, send to imap server, print rsp result on screen
       Usage:
           imapin server port
           imapin path_to_input_file server port [optional_xymlogin_payload]

       Input file exmaple1:
           login qe_renzf_01 Yahoo!
           select inbox
           list "" *
           logout

       Input file exmaple2:
           AUTHENTICATE XYMLOGIN <<xymloginPayload>>
           select inbox
           list "" *
           logout
    """

if len(sys.argv) not in (3, 4, 5, 6):
    usage()
    sys.exit(0)

if len(sys.argv) == 3:
    client = IMAPClient(sys.argv[1], int(sys.argv[2]))
    client.start()
    HISTORY_FILE = os.path.expanduser('~/imap.py.input_history')
    if os.path.exists(HISTORY_FILE):
        for l in open(HISTORY_FILE, "r").read().split('\n'):
            readline.add_history(l.strip())
    f_imap_in = open(HISTORY_FILE, "a")
    try:
        while client.is_alive():
            #try: line = sys.stdin.readline().strip() #NON block reading
            #except: continue
            line = raw_input()
            readline.add_history(line)
            print >>f_imap_in, line
            client.send_cmd_and_wait_for_response(line)
    except socket.error, msg:
        print >>sys.stderr, msg
    except KeyboardInterrupt, msg:
        client.stop()
        print >>sys.stderr, msg
    f_imap_in.close()
    sys.exit(0)

path_to_input_file, server, port = sys.argv[1:4]
commands = [l.strip() for l in open(path_to_input_file).read().split('\n') if l.strip() and not l.strip().startswith('--')]

client = IMAPClient(server, int(port))
client.start()
time.sleep(1)#wait for response first

#print sys.argv
show_input = False
if len(sys.argv) >= 5:
    payload = sys.argv[4]
    if len(sys.argv) == 6:
        show_input = True

num = 0
for cmd in commands:
    pos = cmd.lower().find(" xymlogin")
    if pos != -1:
        cmd = cmd[:pos + len(" xymlogin")] + ' ' + payload
    if not re.match(r'^\d+\s\w+', cmd):
        cmd = str(num) + ' ' + cmd
    num += 1
    if show_input:
        print cmd
    client.send_cmd_and_wait_for_response(cmd)

client.stop()

