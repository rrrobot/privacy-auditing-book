#!/usr/bin/env python3

import mmap,struct
def validate_jpeg(fn):
    print(fn)
    f = open(fn,"rb")
    #data = mmap.mmap(f.fileno(),0,mmap.MAP_SHARED,mmap.PROT_READ)
    data = f.read()
    pos = 0
    while pos+2 <= len(data):
        print("  {:6}: {:02X} {:02X}".format(pos,data[pos],data[pos+1]))
        if data[pos] != 0xFF:
            print("{} No Marker FF @ loc {}  ({} found)".format(fn,pos,data[pos]))
            return
        marker = data[pos+1]

        # Decode the fixed-size markers
        if marker==0xD8:  # SOI
            pos += 2;
            continue

        if (marker >= 0xD0 and marker <= 0xD8): # RSTn
            pos += 2;
            continue
        
        if marker==0xD9: # EOI
            extra = len(data)-(pos+2)
            if extra: print("  EXTRA BYTES: {}".format(extra))
            return       # validated!

        # Decode the SOS segment
        if marker==0xDA: # Found SOS; scan for the EOI
            eoi_loc = data.find(b'\xFF\xD9',pos)
            if eoi_loc>0:
                pos = eoi_loc;
                continue 
            print("  NO EOI")
            return

        # Get the length, add it, then loop
        try:
            segment_len = struct.unpack('>H',data[pos+2:pos+4])[0]
            if marker==0xFE:
                print(" COMMENT: {}".format(data[pos+4:pos+2+segment_len]))
            # Additional decoding could go here
            pos += 2 + segment_len
        except struct.error:
            break               # end of file?
    print("  {:6}: EOF".format(pos)) # end of file


if __name__=="__main__":
    import argparse,os,mmap

    parser = argparse.ArgumentParser(description="Search and process JPEGs in local file system")
    parser.add_argument("path",nargs="+",help="Path to search")
    args = parser.parse_args()

    def is_jpeg_fn(fn):
        return os.path.splitext(fn)[1].lower() in ['.jpg','.jpeg']

    file_count = 0
    byte_count = 0
    for fn in args.path:
        if os.path.isdir(fn):
            for (dirpath, dirnames, filenames) in os.walk(fn):
                for name in filter(is_jpeg_fn,filenames):
                    file_count += 1
                    byte_count += os.path.getsize(os.path.join(dirpath,name))
                    validate_jpeg(os.path.join(dirpath,name))
            print("files: {:,} bytes: {:,}  average size: {:,}".format(file_count,byte_count,byte_count/file_count))
        else:
            validate_jpeg(fn)

