#!/usr/bin/env python3.2
# -*- coding: utf-8 -*-
#

import unicodedata,sys

encodings=['mac roman','latin1','utf-8','utf-16 le','utf-16 be','utf-32 le','utf-32 be']
nn     = unicodedata.normalize("NFC",u"ñ")

print(type(nn),unicodedata.name(nn))
for encoding in encodings:
  line = "%9s: " % format(encoding)
  for ch in nn.encode(encoding):
    line += "%02x " % ch
  print(line)

