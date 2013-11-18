#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# expanded json view for compact json file
# Usage:
#
#    cat a.json | jsonview.py
#
#    jsonview a.json
#
# Frank Ren ( realfun AT gmail DOT com)
#

import json

import sys

if len(sys.argv) <= 1:
    raw = ''.join(sys.stdin.readlines())
else:
    with open(sys.argv[1], 'rb') as f:
        raw = f.read()

obj = json.loads(raw)
print json.dumps(obj, indent=2)
