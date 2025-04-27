#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Recently I start to write an ico file maker
#   this script helps on analyze the file header
#
# Usage:
#   head xxx.ico    - output 16 bytes
#   head xxx.ico 32 - output 32 bytes
#
import sys
f = open(sys.argv[1], "rb")
L = 16
if len(sys.argv) >= 3:
  L = int(sys.argv[2])
bytes = f.read(L)
for i in range(0, len(bytes), 8):
  print bytes[i:i+8]
xbytes = ["%02x" % ord(b) for b in bytes]
print
for i in range(0, len(bytes), 8):
  print "x " + " ".join(xbytes[i:i+8])

def to_bits(b):
  bs = []
  while b:
    bs.append(b&1)
    b>>=1
  bs = map(str, bs)
  bs.reverse()
  return "".join(bs).zfill(8)

bits = [to_bits(ord(b)) for b in bytes]
print
for i in range(0, len(bytes), 8):
  print "b " + " ".join(bits[i:i+8])


