import struct
buf = b'\xde\xad\xbe\xef'
val = struct.unpack('<L',buf)[0]
print(buf,'=',val)

