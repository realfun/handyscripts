#! /usr/bin/env python
# -*- coding: utf-8 -*-

print """
       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       !!                                               !!
       !! Flatten files of current folder, recursively. !!
       !! .eg. moves all files under all sub-folders to !!
       !! current folder.                               !!
       !!                                               !!
       !!    NOTICE! this might MESS UP your files!     !!
       !!                                               !!
       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

secret = raw_input("Enter 123abc to continue:")
if secret != "123abc":
    print "you Entered " + secret, ", WRONG answer!"
    print "Aborted!!!"
    import sys
    sys.exit()

import os
from os.path import join, getsize
for root, dirs, files in os.walk('.'):
    if root == ".": continue
    for file in files:
        cmd = 'mv "' + join(root,file) + '" "' + file + '"'
        print cmd
        os.system(cmd)

for dir in os.listdir('.'):
    if not os.path.isdir(dir): continue
    cmd = "rm -rf " + dir
    print cmd
    os.system(cmd)

