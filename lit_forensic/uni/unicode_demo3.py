#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-
#

import unicodedata
encodings=['latin1','utf-8','utf-16 le','utf-16 be','utf-32 le','utf-32 be']
nn     = unicodedata.normalize("NFC","ñ")
print(type(nn),unicodedata.name(nn))
for encoding in encodings:
  print("{:9}: ".format(encoding),end="")
  for ch in nn.encode(encoding):
      print("{:02x} ".format(ch),end="")
  print()

