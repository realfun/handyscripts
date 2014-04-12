#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Convert file from gbk/gb2312/gb18030 to utf-8 encoding, could easily convert all
files under a folder from gbk/gb2312/gb18030 to utf-8 encoding.
"""

import os
import sys
import subprocess
import uuid

if len(sys.argv) <= 1:
    print """

    Usage:

        gb2utf8.py xxx.txt
          - convert all the files

        gb2utf8.py *
          - convert all the files

    """
    sys.exit(1)

files = sys.argv[1:]

temp_file = str(uuid.uuid1())

def conv(f):
    with open(temp_file, 'wb') as output:
        rtn = subprocess.call(['iconv', '-f', 'gb18030', '-t', 'utf8', f], stdout=output)
        if rtn == 0:
            # os.remove(f)
            os.rename(temp_file, f)

for f in files:
    conv(f)

if os.path.exists(temp_file):
    os.remove(temp_file)

