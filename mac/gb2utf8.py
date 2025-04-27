#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert file from gbk/gb2312/gb18030 to utf-8 encoding, could easily convert
all files under a folder from gbk/gb2312/gb18030 to utf-8 encoding.
"""

import os
import sys
import subprocess
import uuid

TEMP_FILE = str(uuid.uuid1())


def conv(file):
    with open(TEMP_FILE, 'wb') as output:
        rtn = subprocess.call(
            ['iconv', '-f', 'gb18030', '-t', 'utf8', '-c', file],
            stdout=output)
        if rtn == 0:
            # os.remove(file)
            os.rename(TEMP_FILE, file)


def main():
    if len(sys.argv) <= 1:
        print("""

        Usage:

            cn2utf8.py xxx.txt
              - convert all the files

            cn2utf8.py *
              - convert all the files

        """)
        sys.exit(1)

    files = sys.argv[1:]

    for file in files:
        conv(file)

    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)


main()
